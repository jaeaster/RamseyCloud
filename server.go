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
  OBJECT_PATHNAME = "counterexamples/"
  TIMEOUT = "5s"
  REGION = "us-west-1"
  AWS_PROFILE = "jonathan"
  BUCKET = "cs293b"
  AWS_CREDS_FILE = "/.aws/credentials"
  HOME = "HOME"
  PORT = ":57339"
)

var buck *s3util.Bucket

func main() {
  buck = s3util.NewBucket(os.Getenv(HOME) + AWS_CREDS_FILE, AWS_PROFILE, REGION)
  fmt.Println("Launching server...")
  ln, _ := net.Listen("tcp", PORT)
  for {
    conn, _ := ln.Accept()
    fmt.Printf("New connection from: %s\n", conn.RemoteAddr().String())
    go processConn(conn)
  }
}

func processConn(conn net.Conn) {
  scanner := bufio.NewScanner(conn)
  for {
    fmt.Println("loop running")
    _ = scanner.Scan()
    messageType := scanner.Text()
    fmt.Printf("Message Type Received: %s\n", messageType)
    _ = scanner.Scan()
    switch(messageType) {
    case "SUCCESS":
      n := scanner.Text()
      nInt, _ := strconv.Atoi(n)
      matrix := readMatrix(scanner, nInt)
      buck.Upload([]byte(matrix), BUCKET, OBJECT_PATHNAME + n)
      conn.Write([]byte(n + " Counterexample Saved!\n"))
      break;
    default:
      content := scanner.Text()
      conn.Write([]byte("Content received: " + content + "\n"))
      break;
    }
  }
}

func readMatrix(scanner *bufio.Scanner, n int) string {
  matrix := ""
  for i := 0; i < n; i++ {
    fmt.Println("Read matrix line")
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