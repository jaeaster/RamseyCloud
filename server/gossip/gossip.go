package gossip

import (
  "net"
  "fmt"
  "strings"
  "strconv"
  "os"
  "log"
  "github.com/easterandjay/RamseyCloud/s3util"
  "github.com/easterandjay/RamseyCloud/server"
)

const (
  LOG_FILE = "gossip_log"
)

type GossipServer struct {
  clients map[string]net.Conn
  serverList []string
  ip string
  port string
  log *log.Logger
  clientChan chan bool
  matrix string
  matrixIsCounterExample bool
  high int
  lowestCliqueCount int
  buck *s3util.Bucket
  buckName string
  buckPrefix string
}

func New(
 awsCredFile string,
 awsProfile string,
 awsRegion string,
 port string,
 bucket string,
 prefix string) *GossipServer {
  file, err := os.OpenFile(LOG_FILE, os.O_CREATE|os.O_WRONLY|os.O_APPEND, 0666)
  server.CheckError(err)
  buck := s3util.NewBucket(awsCredFile, awsProfile, awsRegion)
  matrix, high := buck.FindHighestMatrix(bucket, prefix)
  return &GossipServer{
    clients: make(map[string]net.Conn),
    serverList: make([]string, 0),
    port: port,
    log: log.New(file, "LOG: ", log.Ldate|log.Ltime|log.Lshortfile),
    buck: buck,
    buckName: bucket,
    buckPrefix: prefix,
    matrix: matrix,
    matrixIsCounterExample: true,
    high: high,
    lowestCliqueCount: -1,
  }
}

func (gs *GossipServer) GetIP() string {
  name, err := os.Hostname()
  if err != nil {
    fmt.Printf("Hostname Retrieval Error: %v\n", err)
    return "-1"
  }
  addrs, err := net.LookupHost(name)
  if err != nil {
    fmt.Printf("IP Address Retrieval Error: %v\n", err)
    return "-1"
  }
  for _, a := range addrs {
    return a
  }
  return "-1"
}

func (gs *GossipServer) GetPort() string {
  return gs.port
}

func (gs *GossipServer) GetClients() map[string]net.Conn {
  return gs.clients
}

func (gs *GossipServer) SetClient(ipPort string, conn net.Conn) {
  gs.clients[ipPort] = conn
}

func (gs *GossipServer) RemoveClient(ipPort string) {
  delete(gs.clients, ipPort)
}

func (gs *GossipServer) IncrementClientChannel() {
  gs.clientChan <- true
}

func (gs *GossipServer) DecrementClientChannel() {
  <- gs.clientChan
}

func (gs *GossipServer) Log(message string, a ...interface{}) {
  // gs.log.Printf(message, a...)
  fmt.Printf(message, a...)
}

func (gs *GossipServer) ProcessSuccess(conn net.Conn, body string) {
  split := strings.SplitN(body, "\n", 2)
  n, matrix := split[0], split[1][:len(split[1])-4]
  nInt, _ := strconv.Atoi(n)
  if(nInt >= gs.high) {
    if(gs.GossipSuccessConsensus(nInt, matrix)) {
      gs.matrix = matrix
      gs.matrixIsCounterExample = true
      gs.high = nInt
      gs.Log("Found new Counter example!\n")
      gs.Log(gs.matrix)
      gs.buck.Upload([]byte(gs.matrix), gs.buckName, gs.buckPrefix + n)
      for _, client := range gs.clients {
        gs.SendMatrixACK(client)
      }
    } else {
      // do something?
    }
  } else {
    gs.SendMatrixACK(conn)
  }
}

func (gs *GossipServer) ProcessImprovement(conn net.Conn, body string) {
  split := strings.SplitN(body, "\n", 3)
  numCliques, _ := strconv.Atoi(split[0])
  n, matrix := split[1], split[2][:len(split[1])-4]
  nInt, _ := strconv.Atoi(n)
  if(nInt > gs.high && numCliques < gs.lowestCliqueCount) {
    if(gs.GossipImprovedConsensus(nInt, numCliques, matrix)) {
      gs.matrix = matrix
      gs.matrixIsCounterExample = false
      gs.lowestCliqueCount = numCliques
      gs.Log("Found better matrix with clique count: %d\n", numCliques)
      for _, client := range gs.clients {
        gs.SendMatrixACK(client)
      }
    } else {
      // do something?
    }
  } else {
    gs.SendMatrixACK(conn)
  }
}

func (gs *GossipServer) ProcessStateQuery(conn net.Conn) {
  gs.SendMatrixACK(conn)
}

func (gs *GossipServer) ProcessClientRegister(conn net.Conn) {
  gs.SendServerList(conn)
}

func (gs *GossipServer) ProcessRamseyRegister(conn net.Conn) {
  fmt.Printf("Registering ramsey\n")
  gs.RegisterRamsey(conn)
  gs.SendMatrixACK(conn)
}

func (gs *GossipServer) ProcessMatrixAck(conn net.Conn, body string) {
  // noop
  return
}

func (gs *GossipServer) SendMatrixACK(conn net.Conn) {
  var n int
  if gs.matrixIsCounterExample {
    n = gs.high
  } else {
    n = gs.lowestCliqueCount
  }
  resp := fmt.Sprintf("%s\n%d\n%sEND\n", strconv.Itoa(server.MATRIX_ACK), n, gs.matrix)
  conn.Write([]byte(resp))
}

func (gs *GossipServer) SendServerList(conn net.Conn) {
  resp := fmt.Sprintf("%s\n%d\n%sEND\n", strconv.Itoa(server.SERVER_LIST_ACK), strings.Join(gs.serverList, "\n"))
  conn.Write([]byte(resp))
}

func (gs *GossipServer) RegisterRamsey(conn net.Conn) {
  ipPort := conn.RemoteAddr().String()
  gs.clients[ipPort] = conn
  gs.serverList = append(gs.serverList, ipPort)
}

func (gs *GossipServer) GossipImprovedConsensus(n int, cliques int, matrix string) bool {
  return true
}

func (gs *GossipServer) GossipSuccessConsensus(n int, matrix string) bool {
  return true
}