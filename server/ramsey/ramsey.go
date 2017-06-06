package ramsey

import(
  "net"
  "fmt"
  "strings"
  "bufio"
  "strconv"
  "os"
  "log"
  "time"
  "github.com/easterandjay/RamseyCloud/server"
)

const (
  LOG_FILE = "ramsey_log"
)

type RamseyServer struct {
  gossipConn net.Conn
  clients map[string]server.ClientInfo
  ip string
  port string
  log *log.Logger
  clientChan chan bool
  matrix string
  matrixIsCounterExample bool
  high int
  lowestCliqueCount int
  slaves map[string]net.Conn
}

func getGossipIP() string {
  ip := fmt.Sprintf("%s:%s", server.GossipIP, server.GossipPort)
  return ip
}

func New(port string) *RamseyServer {
  file, err := os.OpenFile(LOG_FILE, os.O_CREATE|os.O_WRONLY|os.O_APPEND, 0666)
  server.CheckError(err)
  rs := &RamseyServer{
    matrixIsCounterExample: true,
    lowestCliqueCount: -1,
    clients: make(map[string]server.ClientInfo),
    port: fmt.Sprintf("%s", port),
    log: log.New(file, "LOG: ", log.Ldate|log.Ltime|log.Lshortfile),
    clientChan: make(chan bool, server.MAX_CLIENTS),
  }
  rs.RegisterWithGossip()
  return rs
}

func (rs *RamseyServer) GetIP() string {
  name, err := os.Hostname()
  if err != nil {
    rs.Log("Hostname Retrieval Error: %v\n", err)
    return "-1"
  }
  addrs, err := net.LookupHost(name)
  if err != nil {
    rs.Log("IP Address Retrieval Error: %v\n", err)
    return "-1"
  }
  for _, a := range addrs {
    return a
  }
  return "-1"
}

func (rs *RamseyServer) GetPort() string {
  return rs.port
}

func (rs *RamseyServer) GetClients() map[string]server.ClientInfo {
  return rs.clients
}

func (rs *RamseyServer) SetClient(ipPort string, conn net.Conn, clockSpeed int) {
  rs.clients[ipPort] = server.ClientInfo {
    conn,
    clockSpeed,
    time.Now().Unix(),
  }
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
  // rs.log.Printf(message, a...)
  fmt.Printf(message, a...)
}

func (rs *RamseyServer) ProcessSuccess(conn net.Conn, body string) {
  split := strings.SplitN(body, "\n", 2)
  n := split[0]
  nInt, _ := strconv.Atoi(n)
  if(nInt >= rs.high) {
    rs.Log("Received new counter example from client\n")
    rs.Log(rs.matrix)
    for _, client := range rs.clients {
      rs.SendMatrixACK(client.Conn)
    }
    // matrix := split[1][:len(split[1])-4]
    // msg := fmt.Sprintf("%d\n%d\n%s\nEND\n", server.SUCCESS, nInt, matrix)
    // rs.gossipConn.write([]byte(msg))
    // rs.Log("Waiting for Gossip Server to verify and reach consensus")
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
      rs.SendMatrixACK(client.Conn)
    }
  } else {
    rs.SendMatrixACK(conn)
  }
}

func (rs *RamseyServer) ProcessStateQuery(conn net.Conn) {
  rs.Log("Sending STATE_QUERY Response\n")
  rs.SendMatrixACK(conn)
}

func (rs *RamseyServer) ProcessStateSync(conn net.Conn, body string) {
  split := strings.SplitN(body, "\n", 2)
  syncType, data = split[0], split[1]
  if syncType == "SLAVE" {
    rs.slaves[data] = nil
  }
}

func (rs *RamseyServer) ProcessClientRegister(conn net.Conn) {
  // noop
  return
}

func (rs *RamseyServer) ProcessRamseyRegister(conn net.Conn) {
  // noop
  return
}

func (rs *RamseyServer) ProcessMatrixAck(conn net.Conn, body string) {
  // Ramsey processes Matrix ACK from Gossip
  split := strings.SplitN(body, "\n", 2)
  gossipHigh, err := strconv.Atoi(split[0])
  server.CheckError(err)
  if rs.high <= gossipHigh {
    rs.high = gossipHigh
    rs.matrix = split[1][:len(split[1])-4]
    rs.matrixIsCounterExample = true
    for _, client := range rs.clients {
      rs.SendMatrixACK(client)
    }
  }
}

func (rs *RamseyServer) ProcessSlaveRegister(conn net.Conn, body string) {
  addr := strings.Split(conn.RemoteAddr().String(), ":")[0]
  rs.slaves[addr] = conn
  rs.Log("Registering new slave with address: %s\n", addr)
}

func (rs *RamseyServer) ProcessSlaveRequest(conn net.Conn, body string) {
  rs.Log("Processing Slave Request\n")
  n, _ := strconv.Atoi(strings.Split(body, "\n")[0])
  slaves := make([]string, 0, 10)
  resp := fmt.Sprintf("%d\n%d\n", server.SLAVE_ACK, n)
  for i := 0; i < n; i++ {
    // Get n random slaves
    for addr := range rs.slaves {
      slaves = append(slaves,addr) 
      resp += addr + "\n"   
      break
    }
  }
  resp += "END\n"
  conn.Write([]byte(resp))
  rs.Log("Sent response:\n%s", resp)
  for _, slave := range slaves {
    delete(rs.slaves, slave)
  }
  rs.Log("Unregistered slaves")
}

func (rs *RamseyServer) ProcessSlaveUnregister(conn net.Conn, body string) {
  addr := strings.Split(conn.RemoteAddr().String(), ":")[0]
  delete(rs.slaves, addr)
  rs.Log("Unregistering slave with address: %s\n", addr)
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

func (rs *RamseyServer) RegisterWithGossip() {
  gossipIP := getGossipIP()
  rs.Log("Connecting to gossip at %s\n", gossipIP)
  conn, err := net.Dial("tcp", gossipIP)
  for err != nil {
    rs.Log("Error connecting to gossip: %v\n", err)
    rs.Log("Reconnecting to gossip\n")
    gossipIP := getGossipIP()
    conn, err = net.Dial("tcp", gossipIP)
  }
  rs.Log("Connected to gossip!\n")
  rs.gossipConn = conn
  fmt.Fprintf(conn, "%d\n%s\nEND\n", server.RAMSEY_REGISTER, rs.GetIP())
  scanner := bufio.NewScanner(conn)
  resp, closed := server.RecvMsg(scanner)
  if closed {
    fmt.Println("Gossip down!")
  }
  split := strings.SplitN(resp, "\n", 2)
  rs.Log("Processing Matrix\n")
  rs.ProcessMatrixAck(conn, split[1])
}
