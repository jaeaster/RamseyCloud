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
)

const LOG_FILE = "log"

type RamseyServer struct {
  Buck *s3util.Bucket
  BuckName string
  BuckPrefix string
  Matrix string
  High int
  Clients []net.Conn
  IP string
  Port string
  log *log.Logger
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
  buck := s3util.NewBucket(awsCredFile, awsProfile, awsRegion)
  matrix, high := buck.FindHighestMatrix(bucket, prefix)
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
    High: high,
    Clients: make([]net.Conn, 0, 10),
    IP: string(bodyBytes)[:len(bodyBytes) - 1],
    Port: fmt.Sprintf(":%s", port),
    log: log.New(file, "LOG: ", log.Ldate|log.Ltime|log.Lshortfile),
  }
  return rs
}

func (rs *RamseyServer) Run() {
  rs.Log("Launching server at %s%s\n", rs.IP, rs.Port)
  ln, _ := net.Listen("tcp", rs.Port)
  for {
    conn, _ := ln.Accept()
    rs.Clients = append(rs.Clients, conn)
    rs.Log("New connection from: %s\n", conn.RemoteAddr().String())
    go rs.ProcessConn(conn)
  }
}


func (rs *RamseyServer) ProcessConn(conn net.Conn) {
  defer conn.Close()
  scanner := bufio.NewScanner(conn)
  for {
    rs.Log("Waiting for message from %s\n", conn.RemoteAddr().String())
    msg, closed := rs.RecvMsg(scanner)
    if(closed) {
      rs.Log("Closing connection to %s\n", conn.RemoteAddr().String())
      return
    }
    split := strings.SplitN(msg, "\n", 2)
    messageType, body := split[0], split[1]
    rs.Log("Message Type Received: %s\n", messageType)
    intMessageType, _ := strconv.Atoi(messageType)
    switch(intMessageType) {
    case SUCCESS:
      update := rs.ProcessMatrixResult(body)
      if update {
        for _, client := range rs.Clients {
          rs.SendMatrixACK(client)
        }
      } else {
        rs.SendMatrixACK(conn)
      }
      break;
    case STATE_QUERY:
      rs.Log("Sending STATE_QUERY Response\n")
      rs.SendMatrixACK(conn)
    default:
      content := scanner.Text()
      conn.Write([]byte("Content received: " + content + "\n"))
      break;
    }
  }
}

func (rs *RamseyServer) ProcessMatrixResult(body string) bool {
  split := strings.SplitN(body, "\n", 2)
  n := split[0]
  nInt, _ := strconv.Atoi(n)
  if(nInt >= rs.High) {
    rs.Matrix = split[1][:len(split[1])-4]
    rs.High = nInt
    rs.Buck.Upload([]byte(rs.Matrix), rs.BuckName, rs.BuckPrefix + n)
    return true
  }
  return false
}

func (rs *RamseyServer) SendMatrixACK(conn net.Conn) {
  resp := fmt.Sprintf("%s\n%d\n%sEND\n", strconv.Itoa(ACK), rs.High, rs.Matrix)
  rs.Log(resp)
  conn.Write([]byte(resp))
}

func (rs *RamseyServer) RecvMsg(scanner *bufio.Scanner) (string, bool) {
  msg := ""
  for scanner.Scan() {
    line := scanner.Text()
    rs.Log(line)
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
  if err != nil {
    fmt.Fprintf(os.Stderr, "Fatal Error: %s\n", err.Error())
    os.Exit(1)
  }
}