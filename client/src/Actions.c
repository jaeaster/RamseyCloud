//
// Created by jesper on 5/22/17.
//

#include <stdlib.h>
#include <stdio.h>
#include "../include/Actions.h"
#include "../include/prints.h"
#include "../include/CliqueAnalyzer.h"
#include "../include/cliqueCounter.h"

#define INIT_CAP 50

typedef struct{
    short a;
    short b;
    short tupleI;
    int tupleCost;
    short depth;
} Action;

int count;
int capacity;
Action* actions;

void flipEdge(short a, short b){
    matrix[a][b] = (matrix[a][b] + 1) % 2;
    matrix[b][a] = (matrix[b][a] + 1) % 2;
}

void initActions(){
    actions = malloc(sizeof(Action)*INIT_CAP);
    capacity = INIT_CAP;
    count = 0;
}
void resetActions(){
    count = 0;
}

void doAction(short a, short b, short depth, short tupleI, int tupleCost){
    flipEdge(a, b);

    if(count == capacity){
        capacity *= 2;
        actions = realloc(actions, sizeof(Action)*capacity);
    }

    actions[count].a = a;
    actions[count].b = b;
    actions[count].tupleI = tupleI;
    actions[count].tupleCost = tupleCost;
    actions[count++].depth = depth;
    //printf("Action: (%i->%i), depth:%i \n", i->a, i->b, depth);
}
void doActionTuple(TupleClique *tuple, short depth, short tupleI){
    doAction(tuple->a, tuple->b, depth, tupleI, tuple->cliques.count);
}

void rollbackAction(){
    if(count == 0){
        printf("Actions: No action to rollback.\n");
        exit(0);
        return;
    }
    count--;
    flipEdge(actions[count].a, actions[count].b);
    //printf("Rollback: (%i->%i), depth:%i \n", actions[count].i.a, actions[count].i.b, actions[count].depth);
}

void rollbackToDepth(int depth){
    //printf("Rolling back to depth: %i \n", depth);
    while(actions[count-1].depth >= depth && count > 0){
        rollbackAction();
    }
    //printf("--DONE--\n");
}


/* STAT HELPER */
int* allAndZero(int l){
    int* arr = malloc(sizeof(int)*(l));
    for(int i = 0; i < l; i++)
        arr[i] = 0;
    return arr;
}
void printArrShare(const char* name, int*arr, int length, int c){
    printf("%s: [", name);
    for(int i=0; i < length; i++)
        printf("%i: %.1f%%, ", i, ((float) arr[i])*100/c);
    printf("]\n");
}


void printAllActions(bool skipClean){
    int maxDepth = 0;
    int maxTuple = 0;
    int maxCost = 0;
    printf("----- ACTIONS: ---------");
    for(int i=0; i < count; i++){
        Action ac = actions[i];
        if(ac.depth > maxDepth) maxDepth = ac.depth;
        if(ac.tupleI > maxTuple) maxTuple = ac.tupleI;
        if(ac.tupleCost > maxCost) maxCost = ac.tupleCost;

        if(skipClean && (i+1 != count && actions[i+1].depth == 0)) continue;
        printTuple(ac.depth); printf("%i, c:%i (%i->%i)\n", ac.tupleI, ac.tupleCost, ac.a, ac.b);
    }

    maxDepth++; maxCost++; maxTuple++;

    int* depthArr = allAndZero(maxDepth);
    int* tupleArr = allAndZero(maxTuple);
    int* costArr = allAndZero(maxCost);

    int** depthTupleMatrix = malloc(sizeof(int*)*(maxDepth));
    for(int i = 0; i < maxDepth; i++){
        depthTupleMatrix[i] = allAndZero(maxTuple);
    }

    for(int i=0; i < count; i++){
        Action ac = actions[i];
        depthArr[ac.depth]++;
        tupleArr[ac.tupleI]++;
        costArr[ac.tupleCost]++;
        depthTupleMatrix[ac.depth][ac.tupleI]++;
    }

    printArrShare("Depth", depthArr, maxDepth, count);
    printArrShare("Tuple", tupleArr, maxTuple, count);
    printArrShare("Cost ", costArr, maxCost, count);

    printf("--Depth vs Tuple--\n");
    for(int i=0; i < maxDepth; i++){
        printf("%i:[", i);
        for(int j=0; j < maxTuple; j++)
            printf("%i: %3i, ", j, depthTupleMatrix[i][j]);
        printf("]\n");
    }

    //Freeing memory.
    for(int i=0; i < maxDepth; i++){
        free(depthTupleMatrix[i]);
    }
    free(depthTupleMatrix);
    free(depthArr);
    free(tupleArr);
    free(costArr);
}
