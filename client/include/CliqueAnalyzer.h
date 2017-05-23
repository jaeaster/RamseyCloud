//
// Created by jesper on 5/21/17.
//

#ifndef RAMSEYC_CLIQUEANALYZER_H
#define RAMSEYC_CLIQUEANALYZER_H

#include <stdbool.h>
#include "cliqueCounter.h"

typedef struct{
    short a;
    short b;
    int cost;
} Tuple;

typedef struct{
    int cap;
    int count;
    Tuple *data;
} TupleList;

Tuple* allocateTupleArray(int size);

void initTupleList(TupleList *list, int capacity);
void preAddTupleList(TupleList *list);
void freeTupleList(TupleList *list);

void initTupleChecker();
void analClique(int size, Tuple* tupleArray, short* clique);
void findSubCliques(int size, Cliques *subCliqueInfo, Tuple tuple);


#endif //RAMSEYC_CLIQUEANALYZER_H
