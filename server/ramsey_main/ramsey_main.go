package main

import(
  "github.com/easterandjay/RamseyCloud/server/ramsey"
  "github.com/easterandjay/RamseyCloud/server"
)

const (
  PORT = "57339"
)

func main() {
  rs := ramsey.New(PORT)
  server.Run(rs)
}