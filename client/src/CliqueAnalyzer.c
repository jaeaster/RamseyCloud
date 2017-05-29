//
// Created by jesper on 5/21/17.
//
#include <pthread.h>
#include <stdlib.h>
#include <stdio.h>
#include "../include/CliqueAnalyzer.h"
#include "../include/constants.h"
#include "../include/cliqueCounter.h"

#define N_TUPLES 45

int threadArg[N_TUPLES];
pthread_t tid[N_TUPLES];
int subM[N_TUPLES][M_SIZE][M_SIZE];
short tuples[N_TUPLES][2];
short subSet[N_TUPLES][M_SIZE];
Tuple* resultTuple;
TupleClique* resultTupleClique;
int mSize;

void initTupleChecker(){
    for(int i=0; i < N_TUPLES; i++) threadArg[i] = i;
}

Tuple* allocateTupleArray(){
    return malloc(sizeof(Tuple)*N_TUPLES);
}


/* --------------------TUPLE-CLIQUE---------------- */

TupleClique *allocateTupleCliques(){
    TupleClique* tupleCliques = malloc(sizeof(TupleClique)*N_TUPLES);
    for(int i=0; i < N_TUPLES; i++){
        initCliqueList(&tupleCliques[i].cliques, SUB_TEN_SIZE);
    }
    return tupleCliques;
}
void resetTupleCliques(TupleClique *tupleCliques){
    for(int i=0; i < N_TUPLES; i++){
        resetCliqueList(&tupleCliques[i].cliques);
    }
}
void freeTupleCliques(TupleClique *tupleCliques){
    for(int i=0; i < N_TUPLES; i++){
        freeCliqueList(&tupleCliques[i].cliques);
    }
    free(tupleCliques);
}

/* ---------------LOGIC--------------------*/

int tupleCmp(const void * a, const void * b){
    return ((Tuple*)a)->cost - ((Tuple*)b)->cost;
}

int tupleCliqueCmp(const void *a, const void *b){
    return ((TupleClique*) a)->cliques.count - ((TupleClique*) b)->cliques.count;
}

bool stillAClique2(){
    int v = matrix[tuples[0][0]][tuples[0][1]];
    for(int i=1; i < N_TUPLES; i++){
        if(v != matrix[tuples[i][0]][tuples[i][1]]){
            return false;
        }
    }
    return true;
}
void fillTuples2(short *clique){
    int c = 0;
    for(int i = 1; i < 11; i++){
        for(int j = i + 1; j < 11; j++){
            tuples[c][0] = clique[i];
            tuples[c++][1] = clique[j];
        }
    }
}

void convertSubCliques(int k, Cliques *subCliqueInfo){
    for(int i=0; i < subCliqueInfo->count; i++){
        short* clique = subCliqueInfo->data[i];
        for(int j=1; j < 11; j++){
            clique[j] = subSet[k][clique[j]];
        }
    }
}

int fillSubMatrix2(int k, short nodeA, short nodeB){
    int invColor = (matrix[nodeA][nodeB] + 1) % 2;

    //CREATING SUBSET IN ASCENDING ORDER:

    if(nodeA > nodeB){
        short temp = nodeA;
        nodeA = nodeB;
        nodeB = temp;
    }

    int ca, cb;

    subSet[k][1] = nodeB;

    int c = 0;
    for(short i = 0; i < nodeA; i++)
        if(matrix[nodeA][i] == invColor && matrix[nodeA][i] == matrix[nodeB][i])
            subSet[k][c++] = i;

    ca = c;
    subSet[k][c++] = nodeA;

    for(short i = nodeA; i < nodeB; i++)
        if(matrix[nodeA][i] == invColor && matrix[nodeA][i] == matrix[nodeB][i])
            subSet[k][c++] = i;

    cb = c;
    subSet[k][c++] = nodeB;

    for(short i = nodeB; i < mSize; i++)
        if(matrix[nodeA][i] == invColor && matrix[nodeA][i] == matrix[nodeB][i])
            subSet[k][c++] = i;


    //CREATING MATRIX FROM SUBSET:
    for(int i = 0; i < c - 1; i++){
        for(int j = i + 1; j < c; j++){
            subM[k][i][j] = matrix[subSet[k][i]][subSet[k][j]];
            subM[k][j][i] = matrix[subSet[k][i]][subSet[k][j]];
        }
    }

    //INVERTING EDGE
    subM[k][ca][cb] = invColor;
    subM[k][cb][ca] = invColor;

    return c;
}

void findSubCliques(int size, Cliques *subCliqueInfo, Tuple tuple){
    mSize = size;
    int k = 0;
    int subSize = fillSubMatrix2(k, tuple.a, tuple.b);
    cliqueCountAll(subSize, subM[k], subCliqueInfo);
    convertSubCliques(k, subCliqueInfo); //Convert sub indexes to correct ones.
}

void *analTuple(void *arg){
    const int k = *((int*) arg);
    short nodeA = tuples[k][0];
    short nodeB = tuples[k][1];
    int subSize = fillSubMatrix2(k, nodeA, nodeB);
    resultTuple[k].a = nodeA;
    resultTuple[k].b = nodeB;
    resultTuple[k].cost = cliqueCount10(subSize, subM[k]);
    return NULL;
}

void *analTupleCliques(void *arg){
    const int k = *((int*) arg);
    short nodeA = tuples[k][0];
    short nodeB = tuples[k][1];
    resultTupleClique[k].a = nodeA;
    resultTupleClique[k].b = nodeB;

    Cliques *pClique = &resultTupleClique[k].cliques;
    int subSize = fillSubMatrix2(k, nodeA, nodeB);
    cliqueCountAll(subSize, subM[k], pClique);
    convertSubCliques(k, pClique);

    return NULL;
}

//Tuple array must be of length 45.
void analClique(int size, Tuple* tupleArray, short* clique){
    mSize = size;
    fillTuples2(clique);
    resultTuple = tupleArray;
    for(int i=0; i < N_TUPLES; i++)
        pthread_create(&tid[i], NULL, analTuple, (void*)(threadArg+i));
    for(int i=0; i < N_TUPLES; i++)
        pthread_join(tid[i], NULL);
    qsort(resultTuple, N_TUPLES, sizeof(Tuple), tupleCmp);
}

void analCliqueFull(int size, TupleClique* tupleCliques, short *clique){
    mSize = size;
    fillTuples2(clique);
    resultTupleClique = tupleCliques;
    for(int i=0; i < N_TUPLES; i++)
        pthread_create(&tid[i], NULL, analTupleCliques, (void*)(threadArg+i));
    for(int i=0; i < N_TUPLES; i++)
        pthread_join(tid[i], NULL);
    qsort(resultTupleClique, N_TUPLES, sizeof(TupleClique), tupleCliqueCmp);
}
