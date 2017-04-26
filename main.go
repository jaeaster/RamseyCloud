package main

import(
  // "github.com/EasterAndJay/cloud/server/gossip"
  "os"
  "github.com/EasterAndJay/cloud/server/ramsey"
)

const (
  OBJECT_PATHNAME = "counterexamples/"
  TIMEOUT = "5s"
  REGION = "us-west-1"
  AWS_PROFILE = "jonathan"
  BUCKET = "cs293b"
  AWS_CREDS_FILE = "/.aws/credentials"
  HOME = "HOME"
  PORT = "57339"
)

func main() {
  rs := ramsey.New(
    os.Getenv(HOME) + AWS_CREDS_FILE,
    AWS_PROFILE,
    REGION,
    PORT,
    BUCKET,
    OBJECT_PATHNAME,
  )
  rs.Run()
}