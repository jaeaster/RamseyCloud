#ifndef NETWORK_H
#define NETWORK_H

#define MSS 65535
#define MAX_RECV 1024
#define MAX_PAYLOAD 640000
#define HOSTNAME "100.111.111.111"
#define PORT "80"
#define NEWLN "\n"
#define ENDLN "END\n"
#define NETWORK_DOWN 0

#include <sys/socket.h>
#include <arpa/inet.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include "constants.h"

typedef enum {
    SUCCESS,
    IMPROVEMENT,
    STATE_QUERY,
    CLIENT_REGISTER,
    RAMSEY_REGISTER,
    MATRIX_ACK,
    SERVER_LIST_ACK
} MessageType;

int sockfd;

void init_conn();
void recv_matrix();
void send_matrix(int n, MessageType mt);
void recv_payload(char *payload);
void request_matrix();
void query_server_for_highest();

#endif