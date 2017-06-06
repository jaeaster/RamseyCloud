package gossip

import (
  "net"
  // "net/http"
  "net/smtp"
  "fmt"
  "strings"
  "strconv"
  "os"
  "log"
  "time"
  "github.com/easterandjay/RamseyCloud/s3util"
  "github.com/easterandjay/RamseyCloud/server"
)

const (
  LOG_FILE = "gossip_log"
)

type GossipServer struct {
  clients map[string]server.ClientInfo
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
    clients: make(map[string]server.ClientInfo),
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
    gs.Log("Hostname Retrieval Error: %v\n", err)
    return "-1"
  }
  addrs, err := net.LookupHost(name)
  if err != nil {
    gs.Log("IP Address Retrieval Error: %v\n", err)
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

func (gs *GossipServer) GetClients() map[string]server.ClientInfo {
  return gs.clients
}

func (gs *GossipServer) SetClient(ipPort string, conn net.Conn, clockSpeed int) {
  gs.clients[ipPort] = server.ClientInfo {
    conn,
    clockSpeed,
    time.Now().Unix(),
  }
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
  if nInt >= gs.high {
    if gs.GossipSuccessConsensus(nInt, matrix) {
      gs.Log("Found new Counter example!\n")
      gs.Log(gs.matrix)
      gs.storeMatrix([]byte(gs.matrix), n)
      gs.Log("Updating Ramsey Servers with up to Date Counterexample")
      for _, client := range gs.clients {
        gs.SendMatrixACK(client.Conn)
      }
    } else {
      // gs.SendMatrixACK(conn)
    }
  } else {
    // gs.SendMatrixACK(conn)
  }
}

func (gs *GossipServer) storeMatrix(matrix []byte, n string) {
  gs.buck.Upload(matrix, gs.buckName, gs.buckPrefix + n)
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
        gs.SendMatrixACK(client.Conn)
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

func (gs *GossipServer) ProcessStateSync(conn net.Conn, body string) {
  split := strings.SplitN(body, "\n", 2)
  syncType, data := split[0], split[1]
  if syncType == "MATRIX" {
    split = strings.SplitN(data, "\n", 2)
    n, err := strconv.Atoi(split[0])
    matrix := split[1][:len(split[1])-4]
    if n, err := strconv.Atoi(data[0]); n > gs.high {
      gs.matrix = matrix
      gs.high = n
      gs.matrixIsCounterExample = true
    }
  }
}

func (gs *GossipServer) ProcessClientRegister(conn net.Conn) {
  gs.SendServerList(conn)
}

func (gs *GossipServer) ProcessRamseyRegister(conn net.Conn) {
  gs.Log("Registering ramsey\n")
  gs.RegisterRamsey(conn)
  gs.SendMatrixACK(conn)
}

func (gs *GossipServer) ProcessMatrixAck(conn net.Conn, body string) {
  // noop
  return
}

func (gs *GossipServer) ProcessSlaveRegister(conn net.Conn, body string) {
  // noop
  return
}

func (gs *GossipServer) ProcessSlaveRequest(conn net.Conn, body string) {
  // noop
  return
}

func (gs *GossipServer) ProcessSlaveUnregister(conn net.Conn, body string) {
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
  gs.SetClient(ipPort, conn, 0)
  gs.serverList = append(gs.serverList, ipPort)
}

func (gs *GossipServer) GossipImprovedConsensus(n int, cliques int, matrix string) bool {
  return true
}

func (gs *GossipServer) GossipSuccessConsensus(n int, matrix string) bool {
  return true
  // highMatrix, high := gs.GossipQueryHighest()
  // gs.matrixIsCounterExample = true
  // if n > high {
  //   gs.matrix = matrix
  //   gs.high = n
  //   return true
  // } else {
  //   gs.matrix = highMatrix
  //   gs.high = high
  //   return false
  // }
}

func (gs *GossipServer) GossipQueryHighest() (matrix string, n int) {
  return gs.buck.FindHighestMatrix(gs.buckName, gs.buckPrefix)
}

func sendemail(n int) {
  gmail_user := "ramseyrikk@gmail.com"
  gmail_pwd := "bangiversary"
  hostname := "smtp.gmail.com"
  port := ":587"
  recipients := []string{
    "jonathaneasterman@gmail.com",
    "oliver.damsgaard@gmail.com",
    "kristoffer.alvern@hotmail.com",
  }
  auth := smtp.PlainAuth("", gmail_user, gmail_pwd, hostname)
  msg := []byte("To: Cloud Nomas\r\n" +
          "Subject: New Counterexample\r\n\r\n" +
          "New matrix of size " + strconv.Itoa(n) + " found!\r\n")
  err := smtp.SendMail(hostname+port, auth, gmail_user, recipients, msg)
  if err != nil {
    log.Fatal(err)
  }
}
>>>>>>> master
