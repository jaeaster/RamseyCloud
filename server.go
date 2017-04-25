package main

import(
  "net"
  "fmt"
  "bufio"
  "os"
  "strconv"
  "strings"
  "github.com/EasterAndJay/cloud/s3util"
)

const (
  SUCCESS = iota
  ACK
  STATE_QUERY
)

const (
  OBJECT_PATHNAME = "counterexamples/"
  TIMEOUT = "5s"
  REGION = "us-west-1"
  AWS_PROFILE = "jonathan"
  BUCKET = "cs293b"
  AWS_CREDS_FILE = "/.aws/credentials"
  HOME = "HOME"
  PORT = ":57339"
)

type RamseyServer struct {
  Buck *s3util.Bucket
  Matrix string
  High int
  Clients []net.Conn
}

func NewRamseyServer(awsCredFile string, awsProfile string, awsRegion string) *RamseyServer {
  buck := s3util.NewBucket(awsCredFile, awsProfile, awsRegion)
  bucket := BUCKET
  prefix := OBJECT_PATHNAME
  matrix, high := buck.FindHighestMatrix(bucket, prefix)
  rs := &RamseyServer{
    Buck: buck,
    Matrix: matrix,
    High: high,
    Clients: make([]net.Conn, 0, 10),
  }
  return rs
}

func (rs *RamseyServer) run() {
  fmt.Println("Launching server...")
  ln, _ := net.Listen("tcp", PORT)
  for {
    conn, _ := ln.Accept()
    rs.Clients = append(rs.Clients, conn)
    fmt.Printf("New connection from: %s\n", conn.RemoteAddr().String())
    go rs.ProcessConn(conn)
  }
}

func RecvMsg(scanner *bufio.Scanner) (string, bool) {
  msg := ""
  for scanner.Scan() {
    line := scanner.Text()
    fmt.Println(line)
    msg += line + "\n"
    if line == "END" {
      return msg, false
    }
  }
  return msg, true
}


func (rs *RamseyServer) ProcessConn(conn net.Conn) {
  defer conn.Close()
  scanner := bufio.NewScanner(conn)
  for {
    fmt.Println("Waiting for message")
    msg, closed := RecvMsg(scanner)
    if(closed) {
      fmt.Printf("Closing connection to %s\n", conn.RemoteAddr().String())
      return
    }
    split := strings.SplitN(msg, "\n", 2)
    messageType, body := split[0], split[1]
    fmt.Printf("Message Type Received: %s\n", messageType)
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
      fmt.Println("Sending STATE_QUERY Response")
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
    rs.Buck.Upload([]byte(rs.Matrix), BUCKET, OBJECT_PATHNAME + n)
    return true
  }
  return false
}

func (rs *RamseyServer) SendMatrixACK(conn net.Conn) {
  resp := fmt.Sprintf("%s\n%d\n%sEND\n", strconv.Itoa(ACK), rs.High, rs.Matrix)
  fmt.Println(resp)
  conn.Write([]byte(resp))
}

func registerGossip(gossipIP string) {
  // Get my IP
  // Send to Gossip instance
}

func checkError(err error) {
  if err != nil {
    fmt.Fprintf(os.Stderr, "Fatal Error: %s", err.Error())
    os.Exit(1)
  }
}

func main() {
  rs := NewRamseyServer(os.Getenv(HOME) + AWS_CREDS_FILE, AWS_PROFILE, REGION)
  rs.run()
}