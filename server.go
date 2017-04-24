package main

import(
  "net"
  "fmt"
  "bufio"
  "os"
  "strconv"
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



func (rs *RamseyServer) ProcessConn(conn net.Conn) {
  defer conn.Close()
  scanner := bufio.NewScanner(conn)
  for {
    fmt.Println("loop running")
    mas := scanner.Scan()
    if(!mas) {
      fmt.Printf("Closing connection to %s\n", conn.RemoteAddr().String())
      return
    }
    messageType := scanner.Text()
    fmt.Printf("Message Type Received: %s\n", messageType)
    _ = scanner.Scan()
    intMessageType, _ := strconv.Atoi(messageType)
    switch(intMessageType) {
    case SUCCESS:
      rs.ProcessMatrixResult(scanner)
      rs.SendMatrixACK(conn)
      break;
    case STATE_QUERY:
      rs.SendMatrixACK(conn)
    default:
      content := scanner.Text()
      conn.Write([]byte("Content received: " + content + "\n"))
      break;
    }
  }
}

func (rs *RamseyServer) ProcessMatrixResult(scanner *bufio.Scanner) {
  n := scanner.Text()
  nInt, _ := strconv.Atoi(n)
  if(nInt >= rs.High) {
    rs.Matrix = readMatrix(scanner, nInt)
    rs.High = nInt
    rs.Buck.Upload([]byte(rs.Matrix), BUCKET, OBJECT_PATHNAME + n)
  }
}

func (rs *RamseyServer) SendMatrixACK(conn *net.Conn) {
  resp := fmt.Sprintf("%s\n%d\n%s", strconv.Itoa(ACK), rs.High, rs.Matrix)
  fmt.Println(resp)
  conn.Write([]byte(resp))
}

func readMatrix(scanner *bufio.Scanner, n int) string {
  matrix := ""
  for i := 0; i < n; i++ {
    _ = scanner.Scan()
    matrixLine := scanner.Text()
    matrix += matrixLine + "\n"
  }
  return matrix
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