package gossip

import (
  "net"
  
)

type GossipServer struct {
  Servers []net.Conn
  IP string
  Port string
}