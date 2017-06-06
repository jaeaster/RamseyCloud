package server

import(
  "net"
  "bufio"
  "strings"
  "strconv"
  "os"
  "time"
  "fmt"
)

const (
  LOG_FILE = "error_log"
)

const (
  SUCCESS = iota
  IMPROVEMENT
  STATE_QUERY
  CLIENT_REGISTER
  RAMSEY_REGISTER
  MATRIX_ACK
  SERVER_LIST_ACK
)

const (
  MAX_CLIENTS = 1000
)

var GossipIP string = os.Getenv("GOSSIP_SERVICE_SERVICE_HOST")
var GossipPort string = os.Getenv("GOSSIP_SERVICE_SERVICE_PORT")

type ClientInfo struct {
  Conn net.Conn
  ClockSpeed int
  StartTime int64
}

type Server interface {
  GetIP() string
  GetPort() string
  GetClients() map[string]ClientInfo
  SetClient(string, net.Conn, int)
  RemoveClient(string)
  IncrementClientChannel()
  DecrementClientChannel()
  Log(string, ...interface{})
  ProcessSuccess(net.Conn, string)
  ProcessImprovement(net.Conn, string)
  ProcessStateQuery(net.Conn)
  ProcessClientRegister(net.Conn)
  ProcessRamseyRegister(net.Conn)
  ProcessMatrixAck(net.Conn, string)
  SendMatrixACK(net.Conn)
}

func Run(s Server) {
  s.Log("Launching server at %s%s\n", s.GetIP(), s.GetPort())
  ln, err := net.Listen("tcp", fmt.Sprintf(":%s", s.GetPort()))
  if err != nil {
    fmt.Printf( "Fatal Error: %s\n", err.Error())
    os.Exit(1)
  }
  for {
    conn, err := ln.Accept()
    if err != nil {
      s.Log("Failed connection - %s\n", err.Error())
      continue
    }
    go ProcessConn(s, conn)
    s.IncrementClientChannel()
  }
}

func ProcessConn(s Server, conn net.Conn) {
  defer CleanupConn(s, conn)
  ipPort := conn.RemoteAddr().String()
  scanner := bufio.NewScanner(conn)
  for {
    s.Log("Waiting for message from %s\n", ipPort)
    msg, closed := RecvMsg(scanner)
    if(closed) {
      return
    }
    split := strings.SplitN(msg, "\n", 2)
    messageType, body := split[0], split[1]
    s.Log("Message Type Received: %s\n", messageType)
    intMessageType, _ := strconv.Atoi(messageType)
    switch(intMessageType) {
    case SUCCESS:
      s.ProcessSuccess(conn, body)
    case IMPROVEMENT:
      s.ProcessImprovement(conn, body)
    case STATE_QUERY:
      clockSpeed, err := strconv.Atoi(strings.Split(body, "\n")[0]);
      if err != nil {
        clockSpeed = 0
      }
      s.SetClient(ipPort, conn, clockSpeed)
      s.Log("New connection from: %s\n", ipPort)
      s.Log("Total active clients: %d\n", len(s.GetClients()))
      s.ProcessStateQuery(conn)
    case CLIENT_REGISTER:
      s.ProcessClientRegister(conn)
    case RAMSEY_REGISTER:
      s.ProcessRamseyRegister(conn)
    case MATRIX_ACK:
      s.ProcessMatrixAck(conn, body)
    default:
      content := scanner.Text()
      conn.Write([]byte("Content received: " + content + "\n"))
    }
  }
}

func CleanupConn(s Server, conn net.Conn) {
  ipPort := conn.RemoteAddr().String()
  client := s.GetClients()[ipPort]
  dur := time.Now().Unix() - client.StartTime
  cycles := dur * int64(client.ClockSpeed)
  conn.Close()
  s.Log("Closing connection to %s\nCPU CYCLES USED: %d000000\n", ipPort, cycles)
  s.RemoveClient(ipPort)
  s.DecrementClientChannel()
  s.Log("Total active clients: %d\n", len(s.GetClients()))
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

func CheckError(err error) {
  // file, err := os.OpenFile(LOG_FILE, os.O_CREATE|os.O_WRONLY|os.O_APPEND, 0666)
  if err != nil {
    fmt.Printf("Fatal Error: %s\n", err.Error())
    os.Exit(1)
  }
}
