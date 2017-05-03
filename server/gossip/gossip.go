package gossip

import (
  "net"
  "net/http"
  "fmt"
  "bufio"
  "io/ioutil"
  "strings"
  "strconv"
  "os"
  "log"
  "github.com/EasterAndJay/cloud/s3util"
)

const (
  LOG_FILE = "gossip_log"
  MAX_CLIENTS = 1000
)

// type Server interface {
//   ProcessImprovedExample(string)
//   ProcessCounterExample(string)
//   SendMatrixACK(net.Conn)

// }

type GossipServer struct {
  Servers map[string]net.Conn
  ServerList []string
  IP string
  Port string
  log *log.Logger
  Buck *s3util.Bucket
  BuckName string
  BuckPrefix string
  Matrix string
  MatrixIsCounterExample bool
  High int
  LowestCliqueCount int
}

func New(
 awsCredFile string,
 awsProfile string,
 awsRegion string,
 port string,
 bucket string,
 prefix string) *GossipServer {
  file, err := os.OpenFile(LOG_FILE, os.O_CREATE|os.O_WRONLY|os.O_APPEND, 0666)
  checkError(err)
  resp, err := http.Get("http://myexternalip.com/raw")
  checkError(err)
  defer resp.Body.Close()
  bodyBytes, err := ioutil.ReadAll(resp.Body)
  checkError(err)
  buck := s3util.NewBucket(awsCredFile, awsProfile, awsRegion)
  matrix, high := buck.FindHighestMatrix(bucket, prefix)
  return GossipServer{
    Servers: make(map[string]net.Conn),
    ServerList: make([]string, 0),
    IP: string(bodyBytes)[:len(bodyBytes) - 1],
    Port: port,
    log: log.New(file, "LOG: ", log.Ldate|log.Ltime|log.Lshortfile),
    Buck: buck,
    BuckName: bucket,
    BuckPrefix: prefix,
    Matrix: matrix,
    MatrixIsCounterExample: true,
    High: high,
    LowestCliqueCount: -1,
  }
}

func (gs *RamseyServer) Run() {
  gs.Log("Launching server at %s%s\n", gs.IP, gs.Port)
  ln, _ := net.Listen("tcp", gs.Port)
  for {
    conn, err := ln.Accept()
    if err != nil {
      gs.Log("Failed connection - %s\n", err.Error())
      continue
    }
    ipPort := conn.RemoteAddr().String()
    gs.Servers[ipPort] = conn
    gs.Log("New connection from: %s\n", ipPort)
    gs.Log("Total active workers: %d\n", len(gs.Servers))
    go gs.ProcessConn(conn)
  }
}

func (gs *GossipServer) ProcessConn(conn net.Conn) {
  defer gs.cleanupConn(conn)
  ipPort := conn.RemoteAddr().String()
  scanner := bufio.NewScanner(conn)
  for {
    gs.Log("Waiting for message from %s\n", ipPort)
    msg, closed := RecvMsg(scanner)
    if(closed) {
      return
    }
    split := strings.SplitN(msg, "\n", 2)
    messageType, body := split[0], split[1]
    gs.Log("Message Type Received: %s\n", messageType)
    intMessageType, _ := strconv.Atoi(messageType)
    switch(intMessageType) {
    case SUCCESS:
      update := gs.ProcessCounterExample(body)
      if update {
        for _, server := range gs.Servers {
          gs.SendMatrixACK(server)
        }
      } else {
        gs.SendMatrixACK(conn)
      }
    case STATE_QUERY:
      gs.Log("Sending STATE_QUERY Response\n")
      gs.SendMatrixACK(conn)
    case IMPROVEMENT:
      update := gs.ProcessImprovedExample(body)
      if update {
        for _, server := range gs.Servers {
          gs.SendMatrixACK(server)
        }
      } else {
        gs.SendMatrixACK(conn)
      }
    case REGISTER_CLIENT:
      gs.SendServerList(conn)
    case REGISTER_RAMSEY:
      gs.RegisterRamsey(conn)
      gs.SendMatrixACK(conn)
    default:
      content := scanner.Text()
      conn.Write([]byte("Content received: " + content + "\n"))
    }
  }
}

func (gs *GossipServer) SendServerList(conn net.Conn) {
  resp := fmt.Sprintf("%s\n%d\n%sEND\n", strconv.Itoa(ACK), strings.Join(gs.ServerList, "\n"))
  conn.Write([]byte(resp))
}

func (gs *GossipServer) RegisterRamsey(conn net.Conn) {
  ipPort := conn.RemoteAddr().String()
  gs.Servers[ipPort] = conn
  gs.ServerList = append(gs.ServerList, ipPort)
}

func (gs *GossipServer) GossipImprovedConsensus(n int, cliques int, matrix string) {
  return true
}

func (gs *GossipServer) GossipSuccessConsensus(n int, cliques int, matrix string) {
  return true
}

func (gs *GossipServer) ProcessImprovedExample(body string) bool {
  split := strings.SplitN(body, "\n", 3)
  numCliques, _ := strconv.Atoi(split[0])
  n, matrix := split[1], split[2][:len(split[1])-4]
  nInt, _ := strconv.Atoi(n)
  if(nInt > gs.High && numCliques < gs.LowestCliqueCount) {
    if(gs.GossipImprovedConsensus(nInt, numCliques, matrix)) {
      gs.Matrix = matrix
      gs.MatrixIsCounterExample = false
      gs.LowestCliqueCount = numCliques
      gs.Log("Found better matrix with clique count: %d\n", numCliques)
      return true
    }
  }
  return false
}

func (gs *GossipServer) ProcessCounterExample(body string) bool {
  split := strings.SplitN(body, "\n", 2)
  n, matrix := split[0], split[1][:len(split[1])-4]
  nInt, _ := strconv.Atoi(n)
  if(nInt >= gs.High) {
    if(gs.GossipSuccessConsensus(nInt, numCliques, matrix)) {
      gs.Matrix = matrix
      gs.MatrixIsCounterExample = true
      gs.High = nInt
      gs.Log("Found new Counter example!\n")
      gs.Log(gs.Matrix)
      gs.Buck.Upload([]byte(gs.Matrix), gs.BuckName, gs.BuckPrefix + n)
      return true
    }
  }
  return false
}

func (gs *GossipServer) SendMatrixACK(conn net.Conn) {
  var n int
  if gs.MatrixIsCounterExample {
    n = gs.High
  } else {
    n = gs.LowestCliqueCount
  }
  resp := fmt.Sprintf("%s\n%d\n%sEND\n", strconv.Itoa(ACK), n, gs.Matrix)
  conn.Write([]byte(resp))
}

func (gs *GossipServer) cleanupConn(conn net.Conn) {
  ipPort := conn.RemoteAddr().String()
  conn.Close()
  gs.Log("Closing connection to %s\n", ipPort)
  delete(gs.Servers, ipPort)
  gs.Log("Total active workers: %d\n", len(gs.Servers))
  <- gs.clientChan
}

func RecvMsg(scanner *bufio.Scanner) (string, bool) {
  msg := ""
  for scanner.Scan() {
    line := scanner.Text()
    msg += line + "\n"
    if line == "END" {
      return msg, false
    }
  }
  return msg, true
}

func checkError(err error) {
  file, err := os.OpenFile(LOG_FILE, os.O_CREATE|os.O_WRONLY|os.O_APPEND, 0666)
  if err != nil {
    fmt.Fprintf(file, "Fatal Error: %s\n", err.Error())
    os.Exit(1)
  }
}