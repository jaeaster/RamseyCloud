//
// Created by jesper on 5/21/17.
//

#include "../include/prints.h"
#include "../include/cliqueCounter.h"
#include <stdio.h>

void printDepth2(int depth){
    for(int i=0; i < depth % 40; i++) printf("---");
    printf("[%i]", depth);
}

void printTuple(int depth){
    for(int i=0; i < depth % 40; i++) printf("---");
    printf("-[%i]T", depth);
}

void printInfo(int c, int clean, int nCliques){
    printf("R: %i. C: %i/%i ", nCliques-c, clean, c);
}

void printClique(short* clique){
    printf("[");
    for(int i=1; i < 10; i++){
        printf("%i, ", clique[i]);
    }
    printf("%i](%i)", clique[10], clique[0]);
}
