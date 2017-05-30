
# Start from a Debian image with the latest version of Go installed
# and a workspace (GOPATH) configured at /go.
FROM golang
COPY ./server/gossip_main/.aws /home/.aws
# Copy the local package files to the container's workspace.
ADD . /go/src/github.com/easterandjay/RamseyCloud

# Build the outyet command inside the container.
# (You may fetch or manage dependencies here,
# either manually or with a tool like "godep".)
RUN go get -d ./...
RUN go install github.com/easterandjay/RamseyCloud/server/gossip_main

# Run the outyet command by default when the container starts.
ENTRYPOINT /go/bin/gossip_main

# Document that the service listens on port 8080.
EXPOSE 33957