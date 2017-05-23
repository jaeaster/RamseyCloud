//
// Created by jesper on 5/22/17.
//

#include "CliqueAnalyzer.h"

#ifndef RAMSEYC_ROLLBACKER_H
#define RAMSEYC_ROLLBACKER_H

void initActions();
void resetActions();

void doAction(Tuple *tuple, int depth);
void rollbackAction();
void rollbackToDepth(int depth);

#endif //RAMSEYC_ROLLBACKER_H
