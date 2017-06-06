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
    short a;
    short b;
    Cliques cliques;
} TupleClique;

Tuple* allocateTupleArray();

void initTupleChecker();
void analClique(int size, Tuple* tupleArray, short* clique);
void findSubCliques(int size, Cliques *subCliqueInfo, Tuple tuple);

void analCliqueFull(int size, TupleClique* tupleCliques, short *clique);

TupleClique *allocateTupleCliques();
void resetTupleCliques(TupleClique *tupleClique);
void freeTupleCliques(TupleClique *tupleCliques);



#endif //RAMSEYC_CLIQUEANALYZER_H
