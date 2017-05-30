//
// Created by jesper on 5/20/17.
//

#include <stdio.h>
#include <pthread.h>
#include "../include/MatrixAgent.h"
#include "../include/time.h"
#include "../include/CliqueAnalyzer.h"
#include "../include/io.h"
#include "../include/prints.h"
#include "../include/Actions.h"


bool solveAll(Cliques *cliques, short depth, int maxDepth, int maxWidth);

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
TupleClique* tryToClean(int size, short* clique, short depth){
    if(!isClique(clique)){
        printf("Solved ");
        return NULL;
    }else {
        TupleClique* tupleCliques = allocateTupleCliques();
        analCliqueFull(size, tupleCliques, clique);
        if (tupleCliques[0].cliques.count == 0) {
            printf("Clean ");
            doAction(tupleCliques[0].a, tupleCliques[0].b, depth, 0, 0);
            freeTupleCliques(tupleCliques);
            return NULL;
        } else {
            printf("Dirty ");
            return tupleCliques;
        }
    }
}

//void slaveTupleReceiver(){
//    //1. Read i (and possibly clique, if no clique, calculate it).
//    //2. Use solveAll on the list of clique.
//    //3. Report back to its master true or false. If true, send the action list in actions.c (not counting actions received earlier from master).
//    //Paralell: Listen to master if to stop (others found a solution). A stop signal could just be that a master performed an action.
//
//    //Stop or complete. Rollback all changes made while solving i (master will broadcast the changes to be made (several may have solved it)). Return.
//}
//
////If computer has a list of slaves use this one.

bool solveDirtyCliqueNetwork(TupleClique *tuples, short depth, int maxDepth, int maxWidth){
    SlaveSolution solution;
    initSlaveSolution(&solution);
    int slavefds[NUM_SLAVES];
    for(int i = 0; i < NUM_SLAVES; i++) {
        slavefds[i] = startSlave(i, &tuples[i], parents, maxDepth, maxWidth);
    }
    waitForSlaveSolution(&solution);

    if(solution.count == 0){
        return false;
    }else{
        for(short i = 0; i < solution.count; i++){
            doAction(solution.tuples[i].a, solution.tuples[i].b, depth, i, solution.tuples[i].cost);
        }
    }
    freeSlaveSolution(&solution);
    return false;
}

bool solveDirtyClique(TupleClique *tuples, short depth, int maxDepth, int maxWidth){

    //Going through tuples until solution.
    bool solved;
    for(short i=0; i < maxWidth; i++){

        printTuple(depth); printf("%i", i);
        if(doesSetsIntersect(&tuples[i].cliques, parents)){
            printf("Intersect with a parent.\n");
            continue;
        }
        printf("\n");

        //Making the change that makes the i cliques.
        doAction(tuples[i].a, tuples[i].b, depth, i, tuples[i].cliques.count);
        solved = solveAll(&tuples[i].cliques, depth + 1, maxDepth, maxWidth);

        if(solved) return true;

        //Rollback:
        rollbackAction();
    }
    return false;
}

bool solveAll(Cliques *cliques, short depth, int maxDepth, int maxWidth){
    int c = 0;
    int clean = 0;
    int increasedIteration = -1;
    while(c < cliques->count){

        //If max width or max depth was increased to solve a dirty, hard clique, then reset it for the next.
        if(increasedIteration != -1 && increasedIteration != c){
            printf("Resetting max depth and width.");
            maxDepth = mMaxDepth;
            maxWidth = mMaxWidth;
            increasedIteration = -1;
        }

        bool hasSolvedClique;
        printDepth2(depth); printf("%i: ", c);

        short* clique = cliques->data[c];
        TupleClique* tupleCliques = tryToClean(mSize, clique, depth);

        //1. Either clean/solved, maxDepth or expanding.
        if(tupleCliques == NULL){
            hasSolvedClique = true;
            printInfo(c, clean, cliques->count-1); printf("\n");
        }else if(depth == maxDepth) {
            hasSolvedClique = false;
            printf(". (Max depth)\n");
        }else{
            //Need to clean the dirty:
            printInfo(c, clean, cliques->count); printf("\n");

            //Adding this clique as a parent.
            prepareToAdd(parents);
            parents->data[parents->count++] = clique;

            if(depth <= PARALELL_DEPTH){
                hasSolvedClique = solveDirtyCliqueNetwork(tupleCliques, depth, maxDepth, maxWidth);
            }else{
                hasSolvedClique = solveDirtyClique(tupleCliques, depth, maxDepth, maxWidth);
            }

            //Remove parent:
            parents->count--;
        }


        //2. Handling results:
        if(hasSolvedClique){
            clean++;
        }else if(depth != 0){
            //Undoing all actions done at this depth.
            rollbackToDepth(depth);
            freeTupleCliques(tupleCliques);
            return false;
        }else{
            //Could not solve this clique. Increase depth/width for this iteration.
            printf("*Could not solve dirty. Increasing depth/width temporarily and trying again*\n");
            maxDepth+=MAX_DEPTH_INC;
            maxWidth+=MAX_WIDTH_INC;
            if(maxWidth > N_TUPLES) maxWidth = N_TUPLES;

            increasedIteration = c;
            freeTupleCliques(tupleCliques);
            continue;
        }

        //3. Getting ready for next iteration:
        c++;
        if(tupleCliques != NULL) freeTupleCliques(tupleCliques);
    }

    return true;
}

void beginSolving(int initSize){
    mSize = initSize;

    Cliques cliques;
    initCliqueList(&cliques, TEN_SIZE);
    initCliqueList(parents, 200);

    int iteration = 0;
    time_t startTime = time(NULL);

    while(mSize <= M_SIZE){

        resetCliqueList(&cliques);
        printf("Counting cliques for size %i...\n", mSize);
        cliqueCountAllT(mSize, &cliques);

        if(cliques.count == 0){
            long timeUsed = time(NULL) - startTime;
            printf("-------------- COMPLETED SIZE %i in %lim %lis --------------- \n", mSize, timeUsed/60, timeUsed % 60);
            writeToFile(mSize, matrix);
            printf("\n");

            //Resetting and incrementing size:
            mSize += SIZE_JUMP;
            resetActions();
            mMaxDepth = INIT_MAX_DEPTH;
            mMaxWidth = INIT_MAX_WIDTH;
            iteration = 0;
            startTime = time(NULL);
            continue;
        }

        //Working the data:
        printf("--------------- It: %i, Size: %i, 10-cliques: %i MaxDepth: %i, MaxWidth: %i -------------------- \n", iteration, mSize, cliques.count, mMaxDepth, mMaxWidth);
        solveAll(&cliques, 0, mMaxDepth, mMaxWidth);
        printAllActions(true);
        iteration++;
        mMaxDepth += MAX_DEPTH_INC;
        mMaxWidth += MAX_WIDTH_INC;
        if(mMaxWidth > N_TUPLES) mMaxWidth = N_TUPLES;
    }
}
