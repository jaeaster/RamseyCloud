#include "../include/network.h"

void init_conn() {
  int errno;
  struct sockaddr_in host;

  host.sin_family = AF_INET;
  host.sin_port = htons(atoi(PORT));
  inet_aton(HOSTNAME, (struct in_addr *)&(host.sin_addr.s_addr));

  // Open socket on client
  sockfd = socket(AF_INET, SOCK_STREAM, 0);
  if(sockfd < 0) {
    perror("internal error creating socket\n");
    exit(0);
  }

  // Establish connection with server
  errno = connect(sockfd, (struct sockaddr *)&host, sizeof(struct sockaddr_in));
  
  if(errno < 0) {
    perror("internal error connecting to server\n");
    exit(0);
  }
}

void send_matrix(int n, MessageType mt) {
  printf("Sending Matrix of size %d to server %s\n", n, HOSTNAME);
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

int recv_matrix() {
  char payload[MAX_PAYLOAD];
  char *p;
  int i, j, z, n;
  i = j = z = 0;
  recv_payload(payload);
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

int request_matrix() {
  char msg[12];
  float clockSpeed = get_cpu_clock_speed();
  MessageType mt = STATE_QUERY;
  sprintf(msg, "%d\n%4.0f\nEND\n",(int)mt, clockSpeed);
  send(sockfd, msg, 12, 0);
  return recv_matrix();
}

void recv_payload(char *payload) {
  int nBytes, size;
  char buf[MAX_RECV];
  size = 0;
  printf("Receiving Payload from Server\n");
  while((nBytes = recv(sockfd, buf, MAX_RECV, 0)) > 0) {
    memcpy(payload, buf, nBytes);
    memset(buf, 0, MAX_RECV);
    size += nBytes;
  }
  printf("Received Payload from Server\n");
  payload[size] = '\0';
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