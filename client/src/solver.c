//
// Created by jesper on 5/21/17.
//

#include <stdbool.h>
#include <time.h>
#include <stdio.h>
#include "../include/cliqueCounter.h"
#include "../include/MatrixAgent2.h"
#include "../include/CliqueAnalyzer.h"
#include "../include/io.h"
#include "../include/prints.h"
#include "../include/Actions.h"

/* SOLVING ALL SIZES */

void beginSolving(const int initSize){
    int size = initSize;
    int maxDepth = INIT_MAX_DEPTH;
    int maxWidth = INIT_MAX_WIDTH;

    Cliques cliques, parents;
    initCliqueList(&cliques, TEN_SIZE);
    initCliqueList(&parents, 200);

    int iteration = 0;
    time_t startTime = time(NULL);

    while(size <= M_SIZE){

        resetCliqueList(&cliques);
        printf("Counting cliques for size %i...\n", size);
        cliqueCountAllT(size, &cliques);

        if(cliques.count == 0){
            long timeUsed = time(NULL) - startTime;
            printf("-------------- COMPLETED SIZE %i in %lim %lis --------------- \n", size, timeUsed/60, timeUsed % 60);
            writeToFile(size, matrix);
            printf("\n");

            //Resetting and incrementing size:
            size += SIZE_JUMP;
            resetActions();
            maxDepth = INIT_MAX_DEPTH;
            maxWidth = INIT_MAX_WIDTH;
            iteration = 0;
            startTime = time(NULL);
            continue;
        }

        //Working the data:
        printf("--------------- It: %i, Size: %i, 10-cliques: %i MaxDepth: %i, MaxWidth: %i -------------------- \n", iteration, size, cliques.count, maxDepth, maxWidth);
        solveAll(size, &cliques, &parents, 0, maxDepth, maxWidth);
        iteration++;
        maxDepth += MAX_DEPTH_INC;
        maxWidth += MAX_WIDTH_INC;
    }
}
