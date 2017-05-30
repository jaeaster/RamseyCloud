#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include "../include/io.h"
#include "../include/cliqueCounter.h"
#include "../include/MatrixAgent.h"
#include "../include/CliqueAnalyzer.h"
#include "../include/Actions.h"
#include "../include/network.h"

#define highest true

int mMaxDepth = INIT_MAX_DEPTH;
int mMaxWidth = INIT_MAX_WIDTH;
int mSize;
Cliques parentsMem;
Cliques* parents = &parentsMem;

void slaveInit(TupleClique *tc, int *maxDepth, int *maxWidth) {
    // Register with ramsey server
    int sockfd = init_conn(RAMSEY_HOSTNAME, RAMSEY_PORT);
    registerSlave(sockfd);
    // Wait for a master to contact it
    int masterfd = listenForStartMessage(tc, maxDepth, maxWidth);
    // tc, parents, maxdepth, maxwidth now have correct values
    // Start working
    
}

void masterInit() {

    //Initializing whole matrix with random values
    unsigned int seed = (unsigned int) (TIME_SEED ? time(NULL) : SEED);
    srand(seed);
    printf("SEED: %i\n", seed);

    //Initializing matrix:
    for (int i = 0; i < M_SIZE; i++) {
        for(int j = i + 1; j < M_SIZE; j++){
            int val = rand() % 2;
            matrix[i][j] = val;
            matrix[j][i] = val;
        }
        matrix[i][i] = 0;
    }
    int size;
    if(NETWORK_DOWN) {
        size = 337;
        if(highest) size = getHighestFileSize();
        readFromFile(size, matrix);
    } else {
        int sockfd = init_conn(RAMSEY_HOSTNAME, RAMSEY_PORT);
        size = request_matrix(sockfd);
        requestSlaves(sockfd, NUM_SLAVES);
    }

    //TODO: SEND MATRIX.

    //Starting solving:
    size++;
    beginSolving(size);
}

int main(int argc, char** argv) {

    if (argc < 2 || argc > 3) {
        printf("Arguments must be <port> <opt: master, def:false>");
        exit(0);
    }

    TupleClique tc;
    int maxDepth;
    int maxWidth;
    int port = atoi(argv[1]);
    bool master = (bool) (argc == 3 ? atoi(argv[2]) : 0);

    printf("---------------\n STARTED. port:%i, master:%i \n ----------------\n", port, master);

    //One time initializations:
    cliqueCountInit();
    initTupleChecker();
    initActions();

    if(master){
        masterInit();
    }else{
        slaveInit(&tc, &maxDepth, &maxWidth);
    }
    return 0;
}
