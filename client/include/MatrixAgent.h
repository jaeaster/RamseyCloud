//
// Created by jesper on 5/20/17.
//

#ifndef RAMSEYC_MATRIXAGENT_H
#define RAMSEYC_MATRIXAGENT_H
#include "constants.h"
#include "cliqueCounter.h"
#include "network.h"
extern int mMaxDepth;
extern int mMaxWidth;
extern int mSize;
extern Cliques* parents;


void beginSolving(int initSize);

#endif //RAMSEYC_MATRIXAGENT_H
