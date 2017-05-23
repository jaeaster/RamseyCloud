#ifndef CLIQUECOUNTER_H
#define CLIQUECOUNTER_H

#include "constants.h"
#include <stdbool.h>

typedef struct {
    short **data;
    int ten_capacity;
    int count;
} Cliques;

void initCliqueList(Cliques *info, int capacity);
void resetCliqueList(Cliques *info);
void freeInfo(Cliques *info);
void prepareToAdd(Cliques *info);
short* getLast(Cliques *info);

bool areCliquesEqual(short* c1, short* c2);
bool doesSetsIntersect(Cliques *s1, Cliques *s2);

void cliqueCountAll(int size, int g[][M_SIZE], Cliques *info);
int cliqueCount10(int size, int g[][M_SIZE]);

void cliqueCountInit();
void cliqueCountAllT(int size, Cliques *info);


#endif