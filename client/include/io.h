//
// Created by jesper on 5/16/17.
//

#ifndef RAMSEYC_IO_H
#define RAMSEYC_IO_H

#include "constants.h"

void writeToFile(int size, int m[][M_SIZE]);
void readFromFile(int size, int m[][M_SIZE]);
int getHighestFileSize();

#endif //RAMSEYC_IO_H
