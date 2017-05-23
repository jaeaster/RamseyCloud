//
// Created by jesper on 5/19/17.
//

#ifndef RAMSEYC_BRON_H
#define RAMSEYC_BRON_H

#include "constants.h"

int serial(int size, int matrix[M_SIZE][M_SIZE]);
void runbk(int size, int matrix[M_SIZE][M_SIZE], CliqueInfo *info);

#endif //RAMSEYC_BRON_H
