//
// Created by jesper on 5/21/17.
//

#ifndef RAMSEYC_SOLVER_H
#define RAMSEYC_SOLVER_H

#include "cliqueCounter.h"

void beginSolving(const int initSize);
bool solveThatShit(int size, Cliques *cliques, Cliques *parents, int depth, int maxDepth);

#endif //RAMSEYC_SOLVER_H
