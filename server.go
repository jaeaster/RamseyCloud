package main

import(
  "net"
  "fmt"
  "bufio"
  "strings"
  "github.com/aws/aws-sdk-go/aws"
  "github.com/aws/aws-sdk-go/aws/awsutil"
  "github.com/aws/aws-sdk-go/aws/awserr"
  "github.com/aws/aws-sdk-go/aws/request"
  "github.com/aws/aws-sdk-go/service/s3"
  "github.com/aws/aws-sdk-go/aws/session"
  "github.com/aws/aws-sdk-go/aws/credentials"
)

const (
  BUCKET = "cs293b"
  OBJECT_PATHNAME = "counterexamples/"
  TIMEOUT = "5s"
  REGION = "eucalyptus"
  AWS_CREDS_FILE = "/.aws/credentials"
  HOME = "HOME"
  AWS_PROFILE = "nomads"
  ENDPOINT = "eucalyptus.cloud.eci.ucsb.edu"
  PORT = ":57339"
)

func main() {
  svc := newS3(os.Getenv(HOME) + AWS_CREDS_FILE, AWS_PROFILE, REGION, ENDPOINT)
  fmt.Println("Launching server...")
  ln, _ := net.Listen("tcp", PORT)
  for {
    conn, _ := ln.Accept()
    go processConn(conn)
  }
}

func processConn(conn TCPConn) {
  scanner := bufio.NewScanner(conn)
  for {
    messageType, _ := scanner.Text()
    _ := scanner.Scan()
    fmt.Print("Message Type Received:", messageType)
    switch(messageType) {
    case "SUCCESS":
      n := scanner.Text()
      _ := scanner.Scan()
      example := scanner.Bytes()
      svc.upload(example, BUCKET, OBJECT_PATHNAME + n)
      storeExample(example)
      conn.Write([]byte(n + " Counterexample Saved!\n"))
      break;
    default:
      break;
    }
  }
}


func newS3(credFile string, profile string, region string, endpoint string) *s3.S3{
  creds := credentials.NewSharedCredentials(credFile, profile)
  sess := session.Must(session.NewSession(&aws.Config{
    Region: aws.String(region),
    Endpoint: endpoint,
    Credentials: creds,
  }))
  svc := s3.New(sess)
  return svc
}

func (svc *s3.S3) upload(data []byte, bucket string, dstPath string) {
  ctx := context.Background()
  var cancelFn func()
  timeout, err := time.ParseDuration(TIMEOUT)
  if err != nil {
    fmt.Println(err)
    os.Exit(1)
  }
  if timeout > 0 {
    ctx, cancelFn = context.WithTimeout(ctx, timeout)
  }
  defer cancelFn()

  resp, err := svc.PutObjectWithContext(ctx, &s3.PutObjectInput{
    Bucket: aws.String(bucket),
    Key:    aws.String(dstPath),
    Body:   data,
    ContentLength: aws.Int64(len(data)),
  })
  if err != nil {
    if aerr, ok := err.(awserr.Error); ok && aerr.Code() == request.CanceledErrorCode {
      fmt.Fprintf(os.Stderr, "Upload canceled due to timeout, %v\n", err)
    } else {
      fmt.Fprintf(os.Stderr, "Failed to upload object, %v\n", err)
    }
    os.Exit(1)
  }

  fmt.Printf("Response %s", awsutil.StringValue(resp))
}

func registerGossip(gossipIP string) {
  // Get my IP
  // Send to Gossip instance
}