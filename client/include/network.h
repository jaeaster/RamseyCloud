#ifndef NETWORK_H
#define NETWORK_H

#define MSS 65535
#define MAX_RECV 1024
#define MAX_PAYLOAD 640000
#define RAMSEY_HOSTNAME "169.231.235.98"
#define RAMSEY_PORT "30080"
#define SLAVE_PORT "39393"
#define NEWLN "\n"
#define ENDLN "END\n"
#define NETWORK_DOWN 0

#include <sys/socket.h>
#include <arpa/inet.h>
#include <netdb.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include "constants.h"
#include "CliqueAnalyzer.h"
#include "cliqueCounter.h"

typedef enum {
    SUCCESS,
    IMPROVEMENT,
    STATE_QUERY,
    CLIENT_REGISTER,
    RAMSEY_REGISTER,
    MATRIX_ACK,
    SERVER_LIST_ACK,
    SLAVE_REGISTER,
    SLAVE_REQUEST,
    SLAVE_ACK,
    SLAVE_UNREGISTER
} MessageType;

int slavefd;
int sockfd;
char slaves[NUM_SLAVES][20];
extern int mMaxDepth;
extern int mMaxWidth;
extern int mSize;
extern Cliques* parents;
int init_conn(char *hostname, char *port);
int recv_matrix();
void send_matrix(int sockfd, int n, MessageType mt);
void recv_payload(int sockfd, char *payload);
int request_matrix(int sockfd);
void query_server_for_highest();

typedef struct {
    int count;
    int cap;
    Tuple* tuples; //Ordered solution.
    int i;
} SlaveSolution;


//Pointer to the tupleClique to solve, pointer to the start of parent array.
int registerSlave(int sockfd);
void requestSlaves(int sockfd, int n);
void unregisterSlave();
int listenForStartMessage(TupleClique *tc, int *maxDepth, int *maxWidth);
int startSlave(int tupleID, TupleClique *tupleClique, Cliques* parents, int maxWidth, int maxDepth);
void waitForSlaveSolution(SlaveSolution *solution);

void initSlaveSolution(SlaveSolution *tupleList);
void freeSlaveSolution(SlaveSolution *tupleList);


#endif
