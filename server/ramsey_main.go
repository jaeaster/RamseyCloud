package main

import(
  "github.com/EasterAndJay/cloud/server/ramsey"
  "github.com/EasterAndJay/cloud/server"
)

const (
  PORT = "57339"
  GOSSIP_IP = "128.111.192.123"
)

func main() {
  rs := ramsey.New(PORT)
  rs.RegisterWithGossip(GOSSIP_IP)
  server.Run(rs)
}