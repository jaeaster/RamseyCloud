package ramsey

import(
  "net"
  "net/http"
  "fmt"
  "bufio"
  "io/ioutil"
  "strings"
  "strconv"
  "os"
  "log"
  "github.com/EasterAndJay/cloud/server"
)

const (
  LOG_FILE = "ramsey_log"
)

type RamseyServer struct {
  gossipConn net.Conn
  clients map[string]net.Conn
  ip string
  port string
  log *log.Logger
  clientChan chan bool
  matrix string
  matrixIsCounterExample bool
  high int
  lowestCliqueCount int
}

func New(port string) *RamseyServer {
  file, err := os.OpenFile(LOG_FILE, os.O_CREATE|os.O_WRONLY|os.O_APPEND, 0666)
  server.CheckError(err)
  resp, err := http.Get("http://myexternalip.com/raw")
  server.CheckError(err)
  defer resp.Body.Close()
  bodyBytes, err := ioutil.ReadAll(resp.Body)
  server.CheckError(err)
  rs := &RamseyServer{
    matrixIsCounterExample: true,
    lowestCliqueCount: -1,
    clients: make(map[string]net.Conn),
    ip: string(bodyBytes)[:len(bodyBytes) - 1],
    port: fmt.Sprintf(":%s", port),
    log: log.New(file, "LOG: ", log.Ldate|log.Ltime|log.Lshortfile),
    clientChan: make(chan bool, server.MAX_CLIENTS),
  }
  return rs
}

func (rs *RamseyServer) GetIP() string {
  return rs.ip
}

func (rs *RamseyServer) GetPort() string {
  return rs.port
}

func (rs *RamseyServer) GetClients() map[string]net.Conn {
  return rs.clients
}

func (rs *RamseyServer) SetClient(ipPort string, conn net.Conn) {
  rs.clients[ipPort] = conn
}

func (rs *RamseyServer) RemoveClient(ipPort string) {
  delete(rs.clients, ipPort)
}

func (rs *RamseyServer) IncrementClientChannel() {
  rs.clientChan <- true
}

func (rs *RamseyServer) DecrementClientChannel() {
  <- rs.clientChan
}

func (rs *RamseyServer) Log(message string, a ...interface{}) {
  rs.log.Printf(message, a...)
}


func (rs *RamseyServer) ProcessSuccess(conn net.Conn, body string) {
  split := strings.SplitN(body, "\n", 2)
  n := split[0]
  nInt, _ := strconv.Atoi(n)
  if(nInt >= rs.high) {
    rs.matrix = split[1][:len(split[1])-4]
    rs.matrixIsCounterExample = true
    rs.high = nInt
    rs.Log("Found new Counter example!\n")
    rs.Log(rs.matrix)
    for _, client := range rs.clients {
      rs.SendMatrixACK(client)
    }
  } else {
    rs.SendMatrixACK(conn)
  }
}

func (rs *RamseyServer) ProcessImprovement(conn net.Conn, body string) {
  split := strings.SplitN(body, "\n", 3)
  numCliques, _ := strconv.Atoi(split[0])
  n := split[1]
  nInt, _ := strconv.Atoi(n)
  if(nInt > rs.high && numCliques < rs.lowestCliqueCount) {
    rs.matrix = split[2][:len(split[1])-4]
    rs.matrixIsCounterExample = false
    rs.lowestCliqueCount = numCliques
    rs.Log("Found better matrix with clique count: %d\n", numCliques)
    for _, client := range rs.clients {
      rs.SendMatrixACK(client)
    }
  } else {
    rs.SendMatrixACK(conn)
  }
}

func (rs *RamseyServer) ProcessStateQuery(conn net.Conn) {
  rs.Log("Sending STATE_QUERY Response\n")
  rs.SendMatrixACK(conn)
}

func (rs *RamseyServer) ProcessClientRegister(conn net.Conn) {
  // noop
  return
}

func (rs *RamseyServer) ProcessRamseyRegister(conn net.Conn) {
  // noop
  return
}

func (rs *RamseyServer) ProcessMatrixAck(conn net.Conn) {
  // Ramsey processes Matrick ACK from Gossip
  return
}

func (rs *RamseyServer) SendMatrixACK(conn net.Conn) {
  var n int
  if rs.matrixIsCounterExample {
    n = rs.high
  } else {
    n = rs.lowestCliqueCount
  }
  resp := fmt.Sprintf("%s\n%d\n%sEND\n", strconv.Itoa(server.MATRIX_ACK), n, rs.matrix)
  conn.Write([]byte(resp))
}

func (rs *RamseyServer) RegisterWithGossip(gossipIP string) {
  // Get my IP
  conn, err := net.Dial("tcp", gossipIP)
  for err != nil {
    conn, err = net.Dial("tcp", gossipIP)
  }
  rs.gossipConn = conn
  fmt.Fprintf(conn, "RAMSEY_REGISTER\n%s\nEND\n", rs.GetIP())
  scanner := bufio.NewScanner(conn)
  resp, closed := server.RecvMsg(scanner)
  if closed {
    fmt.Println("Gossip down!")
  }

  split := strings.SplitN(resp, "\n", 3)
  rs.high, err = strconv.Atoi(split[1])
  server.CheckError(err)
  rs.matrix = split[2][:len(split[2])-4]
}
