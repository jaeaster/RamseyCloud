package main

import(
  "os"
  "github.com/easterandjay/RamseyCloud/server"
  "github.com/easterandjay/RamseyCloud/server/gossip"
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
    "/home" + AWS_CREDS_FILE,
    AWS_PROFILE,
    REGION,
    PORT,
    BUCKET,
    OBJECT_PATHNAME,
  )
  server.Run(gs)
}