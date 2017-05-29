//
// Created by jesper on 5/22/17.
//

#include "CliqueAnalyzer.h"

#ifndef RAMSEYC_ROLLBACKER_H
#define RAMSEYC_ROLLBACKER_H

void initActions();
void resetActions();

void doAction(short a, short b, short depth, short tupleI, int tupleCost);
void doActionTuple(TupleClique *tuple, short depth, short tupleI);

void rollbackAction();
void rollbackToDepth(int depth);

void printAllActions(bool skipClean);

#endif //RAMSEYC_ROLLBACKER_H
