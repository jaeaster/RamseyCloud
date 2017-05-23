//
// Created by jesper on 5/22/17.
//

#include <stdlib.h>
#include "../include/Actions.h"
#include "../include/CliqueAnalyzer.h"
#include <stdio.h>

#define INIT_CAP 50

typedef struct{
    short a;
    short b;
    int depth;
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

void doAction(Tuple *tuple, int depth){
    flipEdge(tuple->a, tuple->b);

    if(count == capacity){
        capacity *= 2;
        actions = realloc(actions, sizeof(Action)*capacity);
    }

    actions[count].a = tuple->a;
    actions[count].b = tuple->b;
    actions[count++].depth = depth;
    //printf("Action: (%i->%i), depth:%i \n", tuple->a, tuple->b, depth);
}
void rollbackAction(){
    if(count == 0){
        printf("Actions: No action to rollback.\n");
        exit(0);
        return;
    }
    count--;
    flipEdge(actions[count].a, actions[count].b);
    //printf("Rollback: (%i->%i), depth:%i \n", actions[count].tuple.a, actions[count].tuple.b, actions[count].depth);
}

void rollbackToDepth(int depth){
    //printf("Rolling back to depth: %i \n", depth);
    while(actions[count-1].depth >= depth && count > 0){
        rollbackAction();
    }
    //printf("--DONE--\n");
}
