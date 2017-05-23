//
// Created by jesper on 5/20/17.
//

#include <pthread.h>
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include "../include/cliqueCounter.h"
#include "../include/CliqueAnalyzer.h"
#include "../include/io.h"
#include "../include/solver.h"
#include "../include/prints.h"
#include "../include/Actions.h"

bool solveAll(int size, Cliques *cliques, Cliques *parents, int depth, int maxDepth, int maxWidth);


/* HELPERS */

bool isClique(short *clique){
    int v = matrix[clique[1]][clique[2]];
    for(int i = 1; i < 11; i++){
        for(int j = i + 1; j < 11; j++){
            if(v != matrix[clique[i]][clique[j]]){
                return false;
            }
        }
    }
    return true;
}


/************ SOLVERS *****************/

//Returns null if success. If not null, the array must be cleaned.
Tuple* tryToClean(int size, short* clique, int depth){
    if(!isClique(clique)){
        printf("Solved ");
        return NULL;
    }else {
        Tuple* tuples = allocateTupleArray(N_TUPLES);
        analClique(size, tuples, clique);
        if (tuples[0].cost == 0) {
            printf("Clean ");
            doAction(&tuples[0], depth);
            free(tuples);
            return NULL;
        } else {
            printf("Dirty ");
            return tuples;
        }
    }
}

bool solveDirtyClique(int size, Tuple *tuples, Cliques *subCliques, Cliques *parents, int depth, int maxDepth, int maxWidth){

    //Going through tuples until solution.
    bool solved;
    for(int i=0; i < maxWidth; i++){

        resetCliqueList(subCliques);
        findSubCliques(size, subCliques, tuples[i]);
        printTuple(depth); printf("%i: %i(%i) clique(s)", i, tuples[i].cost, subCliques->count);
        if(doesSetsIntersect(subCliques, parents)){
            printf("Intersect with a parent.\n");
            continue;
        }
        printf("\n");

        //Making the change.
        doAction(&tuples[i], depth);
        solved = solveAll(size, subCliques, parents, depth + 1, maxDepth, maxWidth);

        if(solved) return true;
        rollbackAction();
    }
    return false;
}

bool solveAll(int size, Cliques *cliques, Cliques *parents, int depth, int maxDepth, int maxWidth){

    //Creating a list to hold sub-data:
    Cliques subCliques;
    initCliqueList(&subCliques, 20);

    int c = 0;
    int clean = 0;
    while(c < cliques->count){
        bool hasSolvedClique;
        printDepth2(depth); printf("%i: ", c);

        short* clique = cliques->data[c];
        Tuple* tuples = tryToClean(size, clique, depth);

        //1. Either clean/solved, maxDepth or expanding.

        if(tuples == NULL){
            hasSolvedClique = true;
            printInfo(c, clean, cliques->count); printf("\n");
        }else if(depth == maxDepth) {
            hasSolvedClique = false;
            printf(". (Max depth)\n");
        }else{
            //Need to clean the dirty:
            printInfo(c, clean, cliques->count); printf("\n");

            //Adding this clique as a parent.
            prepareToAdd(parents);
            parents->data[parents->count++] = clique;

            hasSolvedClique = solveDirtyClique(size, tuples, &subCliques, parents, depth, maxDepth, maxWidth);

            //Remove parent:
            parents->count--;
        }


        //2. Handling results:

        if(hasSolvedClique){
            clean++;
        }else if(depth != 0){
            //Undoing all actions done at this depth.
            rollbackToDepth(depth);
            freeInfo(&subCliques);
            return false;
        }else{
            //Could not solve this clique. Leave it.
            printf("*Could not solve dirty*\n");
        }

        //3. Getting ready for next iteration:
        c++;
        if(tuples != NULL) free(tuples);
    }

    freeInfo(&subCliques);
    return true;
}
