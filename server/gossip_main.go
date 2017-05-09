package main

import(
  "os"
  "github.com/EasterAndJay/cloud/server"
  "github.com/EasterAndJay/cloud/server/gossip"
)

const (
  OBJECT_PATHNAME = "counterexamples/"
  REGION = "us-west-1"
  AWS_PROFILE = "jonathan"
  BUCKET = "cs293b"
  AWS_CREDS_FILE = "/.aws/credentials"
  HOME = "HOME"
  PORT = "33957"
)

func main() {
  gs := gossip.New(
    os.Getenv(HOME) + AWS_CREDS_FILE,
    AWS_PROFILE,
    REGION,
    PORT,
    BUCKET,
    OBJECT_PATHNAME,
  )
  server.Run(gs)
}