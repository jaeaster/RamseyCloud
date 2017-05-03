package ramsey

import(
  "github.com/EasterAndJay/cloud/s3util"
  "net"
  "net/http"
  "fmt"
  "bufio"
  "io/ioutil"
  "strings"
  "strconv"
  "os"
  "log"
)

const (
  SUCCESS = iota
  ACK
  STATE_QUERY
  IMPROVEMENT
  REGISTER
)

const (
  LOG_FILE = "ramsey_log"
  MAX_CLIENTS = 1000
)

type RamseyServer struct {
  Clients map[string]net.Conn
  IP string
  Port string
  log *log.Logger
  clientChan chan bool
}

func (rs *RamseyServer) Log(message string, a ...interface{}) {
  rs.log.Printf(message, a...)
}

func New(
  awsCredFile string,
  awsProfile string,
  awsRegion string,
  port string,
  bucket string,
  prefix string,
) *RamseyServer {
  file, err := os.OpenFile(LOG_FILE, os.O_CREATE|os.O_WRONLY|os.O_APPEND, 0666)
  checkError(err)
  resp, err := http.Get("http://myexternalip.com/raw")
  checkError(err)
  defer resp.Body.Close()
  bodyBytes, err := ioutil.ReadAll(resp.Body)
  checkError(err)
  rs := &RamseyServer{
    Buck: buck,
    BuckName: bucket,
    BuckPrefix: prefix,
    Matrix: matrix,
    MatrixIsCounterExample: true,
    High: high,
    LowestCliqueCount: -1,
    Clients: make(map[string]net.Conn),
    IP: string(bodyBytes)[:len(bodyBytes) - 1],
    Port: fmt.Sprintf(":%s", port),
    log: log.New(file, "LOG: ", log.Ldate|log.Ltime|log.Lshortfile),
    clientChan: make(chan bool, MAX_CLIENTS),
  }
  return rs
}

func (rs *RamseyServer) Run() {
  rs.Log("Launching server at %s%s\n", rs.IP, rs.Port)
  ln, _ := net.Listen("tcp", rs.Port)
  for {
    conn, err := ln.Accept()
    if err != nil {
      rs.Log("Failed connection - %s\n", err.Error())
      continue
    }
    ipPort := conn.RemoteAddr().String()
    rs.Clients[ipPort] = conn
    rs.Log("New connection from: %s\n", ipPort)
    rs.Log("Total active workers: %d\n", len(rs.Clients))
    go rs.ProcessConn(conn)
    rs.clientChan <- true
  }
}

func (rs *RamseyServer) cleanupConn(conn net.Conn) {
  ipPort := conn.RemoteAddr().String()
  conn.Close()
  rs.Log("Closing connection to %s\n", ipPort)
  delete(rs.Clients, ipPort)
  rs.Log("Total active workers: %d\n", len(rs.Clients))
  <- rs.clientChan
}

func (rs *RamseyServer) ProcessConn(conn net.Conn) {
  defer rs.cleanupConn(conn)
  ipPort := conn.RemoteAddr().String()
  scanner := bufio.NewScanner(conn)
  for {
    rs.Log("Waiting for message from %s\n", ipPort)
    msg, closed := RecvMsg(scanner)
    if(closed) {
      return
    }
    split := strings.SplitN(msg, "\n", 2)
    messageType, body := split[0], split[1]
    rs.Log("Message Type Received: %s\n", messageType)
    intMessageType, _ := strconv.Atoi(messageType)
    switch(intMessageType) {
    case SUCCESS:
      update := rs.ProcessCounterExample(body)
      if update {
        for _, client := range rs.Clients {
          rs.SendMatrixACK(client)
        }
      } else {
        rs.SendMatrixACK(conn)
      }
    case STATE_QUERY:
      rs.Log("Sending STATE_QUERY Response\n")
      rs.SendMatrixACK(conn)
    case IMPROVEMENT:
      update := rs.ProcessImprovedExample(body)
      if update {
        for _, client := range rs.Clients {
          rs.SendMatrixACK(client)
        }
      } else {
        rs.SendMatrixACK(conn)
      }
    case ACK:
      break
    default:
      content := scanner.Text()
      conn.Write([]byte("Content received: " + content + "\n"))
    }
  }
}

func (rs *RamseyServer) ProcessImprovedExample(body string) bool {
  split := strings.SplitN(body, "\n", 3)
  numCliques, _ := strconv.Atoi(split[0])
  n := split[1]
  nInt, _ := strconv.Atoi(n)
  if(nInt > rs.High && numCliques < rs.LowestCliqueCount) {
    rs.Matrix = split[2][:len(split[1])-4]
    rs.MatrixIsCounterExample = false
    rs.LowestCliqueCount = numCliques
    rs.Log("Found better matrix with clique count: %d\n", numCliques)
    return true
  }
  return false
}

func (rs *RamseyServer) ProcessCounterExample(body string) bool {
  split := strings.SplitN(body, "\n", 2)
  n := split[0]
  nInt, _ := strconv.Atoi(n)
  if(nInt >= rs.High) {
    rs.Matrix = split[1][:len(split[1])-4]
    rs.MatrixIsCounterExample = true
    rs.High = nInt
    rs.Log("Found new Counter example!\n")
    rs.Log(rs.Matrix)
    rs.Buck.Upload([]byte(rs.Matrix), rs.BuckName, rs.BuckPrefix + n)
    return true
  }
  return false
}

func (rs *RamseyServer) SendMatrixACK(conn net.Conn) {
  var n int
  if rs.MatrixIsCounterExample {
    n = rs.High
  } else {
    n = rs.LowestCliqueCount
  }
  resp := fmt.Sprintf("%s\n%d\n%sEND\n", strconv.Itoa(ACK), n, rs.Matrix)
  conn.Write([]byte(resp))
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

func registerGossip(gossipIP string) {
  // Get my IP
  // Send to Gossip instance
}

func checkError(err error) {
  file, err := os.OpenFile(LOG_FILE, os.O_CREATE|os.O_WRONLY|os.O_APPEND, 0666)
  if err != nil {
    fmt.Fprintf(file, "Fatal Error: %s\n", err.Error())
    os.Exit(1)
  }
}