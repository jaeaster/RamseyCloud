#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include "../include/io.h"
#include "../include/cliqueCounter.h"
#include "../include/MatrixAgent2.h"
#include "../include/solver.h"
#include "../include/CliqueAnalyzer.h"
#include "../include/Actions.h"
#include "../include/network.h"

#define highest true


int main(int argc, char** argv) {

    //Initializing whole matrix with random values
    unsigned int seed = (unsigned int) (TIME_SEED ? time(NULL) : SEED);
    srand(seed);
    printf("SEED: %i\n", seed);

    //One time inits:
    cliqueCountInit();
    initTupleChecker();
    initActions();
    cliqueCountInit();
    init_conn();

    //Initializing matrix:
    for (int i = 0; i < M_SIZE; i++) {
        for(int j = i + 1; j < M_SIZE; j++){
            int val = rand() % 2;
            matrix[i][j] = val;
            matrix[j][i] = val;
        }
    }
    for(int i=0; i < M_SIZE; i++){
        matrix[i][i] = 0;
    }

    //Starting solving:
    int size;
    if(NETWORK_DOWN) {
        size = 337;
        if(highest) size = getHighestFileSize();
        readFromFile(size, matrix);
    } else {
        size = request_matrix();
    }
    size++;
    beginSolving(size);

    return 0;
}
