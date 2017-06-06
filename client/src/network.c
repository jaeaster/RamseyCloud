#include "../include/network.h"

int init_conn(char *hostname, char* port) {
  int errno;
  struct sockaddr_in host;

  host.sin_family = AF_INET;
  host.sin_port = htons(atoi(port));
  inet_aton(hostname, (struct in_addr *)&(host.sin_addr.s_addr));
  // Open socket on client
  int sockfd = socket(AF_INET, SOCK_STREAM, 0);
  if(sockfd < 0) {
    perror("internal error creating socket\n");
    exit(0);
  }
  printf("Establishing connection with server\n");
  // Establish connection with server
  errno = connect(sockfd, (struct sockaddr *)&host, sizeof(struct sockaddr_in));
  printf("Connection established\n");
  if(errno < 0) {
    perror("internal error connecting to server\n");
    exit(0);
  }
  return sockfd;
}

void send_matrix(int sockfd, int n, MessageType mt) {
  printf("Sending Matrix of size %d to server %s\n", n, RAMSEY_HOSTNAME);
  int i, j, total_size;
  char buf[MSS];
  char *offset = buf;
  char msg[3];
  char nstr[4];
  sprintf(msg, "%d", mt);
  sprintf(nstr, "%d", n);
  int size = strlen(msg);
  total_size = size;
  printf("Beginning creation of message header\n");
  memcpy(offset, msg, size);
  offset += size;
  total_size += size;
  memcpy(offset, NEWLN, 1);
  offset += 1;
  total_size += 1;
  size = strlen(nstr);
  memcpy(offset, nstr, size);
  offset += size;
  total_size += size;
  printf("Finished message header\n");
  write(STDOUT_FILENO, buf, total_size);
  for(i = 0; i < n; i++) {
    total_size += n + 1;
    if(total_size >= MSS) {
      printf("Sending packet of size %d\n", total_size-(n+1));
      write(STDOUT_FILENO, buf, total_size-(n+1));
      send(sockfd, buf, total_size-(n+1), 0);
      memset(buf, 0, MSS);
      offset = buf;
      total_size = 0;
    }
    for(j = 0; j < n; j++) {
      offset[j] = matrix[i][j] + '0';
    }
    printf("Wrote row %d of matrix to buffer\n", i);
    offset += n;
    *offset = '\n';
    offset++;
  }
  total_size += 4;
  if(total_size >= MSS) {
    printf("Sending packet of size %d\n", total_size-4);
    write(STDOUT_FILENO, buf, total_size-4);
    send(sockfd, buf, total_size-4, 0);
    memset(buf, 0, MSS);
    offset = buf;
    total_size = 4;
  }
  memcpy(buf, ENDLN, 4);
  printf("Sending packet of size %d\n", total_size);
  write(STDOUT_FILENO, buf, total_size);
  send(sockfd, buf, total_size, 0);
  printf("Successfully sent matrix!\n");
}

int recv_matrix(int sockfd) {
  char payload[MAX_PAYLOAD];
  char *p;
  int i, j, z, n;
  i = j = z = 0;
  recv_payload(sockfd, payload);
  p = strtok(payload, "\n");
  printf("Beginning to parse matrix into memory\n");
  while(p != NULL) {
    z++;
    if(z == 2) {
      n = atoi(p);
      printf("Matrix is of size %d\n", n);
    }
    if(z > 2) {
      for(j = 0; j < n; j++) {
        matrix[i][j] = p[j] - '0';
      }
      i++;
    }
    p = strtok(NULL, "\n");
  }
  printf("Matrix Successfully parsed into memory\n");
  return n;
}

int request_matrix(int sockfd) {
  char msg[12];
  float clockSpeed = get_cpu_clock_speed();
  MessageType mt = STATE_QUERY;
  sprintf(msg, "%d\n%4.0f\nEND\n",(int)mt, clockSpeed);
  send(sockfd, msg, 12, 0);
  return recv_matrix(sockfd);
}

void recv_payload(int sockfd, char *payload) {
  int nBytes;
  char *tmp = payload;
  char buf[MAX_RECV];
  printf("Receiving Payload from Server\n");
  while((nBytes = recv(sockfd, buf, MAX_RECV, 0)) > 0) {
    memcpy(tmp, buf, nBytes);
    tmp += nBytes;
    if(strstr(buf, "END") != NULL) {
      break;
    }
    memset(buf, 0, MAX_RECV);
  }
  printf("Received Payload from Server\n");
  *tmp = '\0';
  printf("%s\n", payload);
}

float get_cpu_clock_speed() {
  FILE* fp;
  char buffer[10000];
  size_t bytes_read;
  char* match;
  float clock_speed;

  fp = fopen("/proc/cpuinfo", "r");
  bytes_read = fread(buffer, 1, sizeof(buffer), fp);
  fclose(fp);
  if(bytes_read == 0 || bytes_read == sizeof(buffer)) {
    return 0;
  }
  buffer[bytes_read] = '\0';
  match = strstr(buffer, "cpu MHz");
  if(match == NULL) {
    return 0;
  }
  sscanf(match, "cpu MHz : %f", &clock_speed);
  return clock_speed;
}

int registerSlave() {
  char msg[7];
  int sockfd = init_conn(RAMSEY_HOSTNAME, RAMSEY_PORT);
  MessageType mt = SLAVE_REGISTER;
  sprintf(msg, "%d\nEND\n", (int)mt);
  send(sockfd, msg, 7, 0);
  int n = recv_matrix(sockfd);
  close(sockfd);
  return n;
}

void requestSlaves(int sockfd, int n) {
  char msg[11];
  char payload[1024];
  char *p;
  int nSlaves;
  int z = 0;
  MessageType mt = SLAVE_REQUEST;
  sprintf(msg, "%d\n%d\nEND\n", (int)mt, (int)n);
  send(sockfd, msg, 11, 0);
  recv_payload(sockfd, payload);
  p = strtok(payload, "\n");
  while(p != NULL) {
    z++;
    if(z == 2) {
      nSlaves = atoi(p);
      printf("Received %d slave ip addresses\n", nSlaves);
    }
    if(z > 2 && z+3 < nSlaves) {
      memcpy(slaves[z - 3], p, strlen(p));
    }
    p = strtok(NULL, "\n");
  }
}

void unregisterSlave() {
  char msg[7];
  MessageType mt = SLAVE_UNREGISTER;
  sprintf(msg, "%d\nEND\n", (int)mt);
  send(sockfd, msg, 7, 0);
  return;
}

void recvStartMessage(int sockfd, TupleClique *tc, int *md, int *mw) {
  int nBytes, maxDepth, maxWidth, a, b, n, i, j, z;
  char tmpbuf[5 * sizeof(int)];
  char buf[MAX_RECV];
  printf("Receiving start message from master\n");
  nBytes = recv(sockfd, tmpbuf, 5 * sizeof(int), 0);
  if(nBytes <= 0) {
    perror("Error receiving start message");
  }
  memcpy(&maxDepth, tmpbuf, sizeof(int));
  memcpy(&maxWidth, tmpbuf+sizeof(int), sizeof(int));
  memcpy(&a, tmpbuf + 2 * sizeof(int), sizeof(int));
  memcpy(&b, tmpbuf + 3 * sizeof(int), sizeof(int));
  memcpy(&n, tmpbuf + 4 * sizeof(int), sizeof(int));
  maxDepth = ntohs(maxDepth);
  maxWidth = ntohs(maxWidth);
  a = ntohs(a);
  b = ntohs(b);
  n = ntohs(n);
  parents->count = n;
  parents->data = (short **)malloc(sizeof(short *) * n);
  for(i = 0; i < n; i++) {
    parents->data[i] = (short *)malloc(sizeof(short) * 11);
  }
  i = j = 0;
  while((nBytes = recv(sockfd, buf, MAX_RECV, 0)) > 0) {
    for(z = 0; z < nBytes; z += sizeof(int), j++) {
      if(j == 11) {
        j = 0;
        i++;
      }
      memcpy(&parents->data[i][j], buf + z, sizeof(short));
      parents->data[i][j] = (short)ntohs(parents->data[i][j]);
    }
    memset(buf, 0, MAX_RECV);
  }
  tc->a = (short)a;
  tc->b = (short)b;
  *md = maxDepth;
  *mw = maxWidth;
  printf("Received start message from master\n");
}

int listenForStartMessage(TupleClique *tc, int *maxDepth, int *maxWidth) {
  int slavefd; /* parent socket */
  int childfd; /* child socket */
  int clientlen; /* byte size of client's address */
  int portno;
  struct sockaddr_in serveraddr; /* server's addr */
  struct sockaddr_in clientaddr; /* client addr */
  struct hostent *hostp; /* client host info */
  char *hostaddrp; /* dotted decimal host addr string */
  int optval; /* flag value for setsockopt */

  slavefd = socket(AF_INET, SOCK_STREAM, 0);
  if (slavefd < 0) 
    perror("ERROR opening socket");
  portno = atoi(SLAVE_PORT);
  optval = 1;
  setsockopt(slavefd, SOL_SOCKET, SO_REUSEADDR, 
            (const void *)&optval , sizeof(int));
  bzero((char *) &serveraddr, sizeof(serveraddr));
  serveraddr.sin_family = AF_INET;
  serveraddr.sin_addr.s_addr = htonl(INADDR_ANY);
  serveraddr.sin_port = htons((unsigned short)portno);
  if (bind(slavefd, (struct sockaddr *) &serveraddr, 
     sizeof(serveraddr)) < 0) 
    perror("ERROR on binding");

  if (listen(slavefd, 0) < 0)
    perror("ERROR on listen");
  clientlen = sizeof(clientaddr);

  childfd = accept(slavefd, (struct sockaddr *) &clientaddr, (socklen_t *)&clientlen);
  if (childfd < 0) 
    perror("ERROR on accept");
  /* 
   * gethostbyaddr: determine who sent the message 
   */
  hostp = gethostbyaddr((const char *)&clientaddr.sin_addr.s_addr, 
      sizeof(clientaddr.sin_addr.s_addr), AF_INET);
  if (hostp == NULL)
    perror("ERROR on gethostbyaddr");
  hostaddrp = inet_ntoa(clientaddr.sin_addr);
  if (hostaddrp == NULL)
    perror("ERROR on inet_ntoa\n");
  printf("Slave established connection with %s (%s)\n", 
   hostp->h_name, hostaddrp);
  
  recvStartMessage(childfd, tc, maxDepth, maxWidth);
  close(childfd);
  return slavefd;
}


int startSlave(int tupleID, TupleClique *tupleClique, Cliques* parents, int maxWidth, int maxDepth) {
  int slaveSock = init_conn(slaves[tupleID], SLAVE_PORT);
  int msgSize = sizeof(int) * (5 + (44 * parents->count));
  char startMsg[msgSize];
  int md = htons(maxDepth);
  int mw = htons(maxWidth);
  int tca = htons((int)tupleClique->a);
  int tcb = htons((int)tupleClique->b);
  int count = htons(parents->count);
  memcpy(startMsg, &md, sizeof(int));
  memcpy(startMsg, &mw, sizeof(int));
  memcpy(startMsg, &tca, sizeof(int));
  memcpy(startMsg, &tcb, sizeof(int));
  memcpy(startMsg, &count, sizeof(int));
  int i, j, tmp;
  for(i = 0; i < parents->count; i++) {
    for(j = 0; j < 11; j++) {
      tmp = htons((int)parents->data[j]);
      memcpy(startMsg, &tmp, sizeof(int));
    }
  }
  send(slaveSock, startMsg, msgSize, 0);
  return slaveSock;
}

void waitForSlaveSolution(SlaveSolution *solution) {

}

void initSlaveSolution(SlaveSolution *tupleList) {

}

void freeSlaveSolution(SlaveSolution *tupleList) {

}
