//
// Created by jesper on 5/18/17.
//

#include <stdlib.h>
#include <stdio.h>
#include <stdbool.h>
#include "../include/tuples.h"
#include "../include/constants.h"

void resetTupleList(ShortList *tupleList){
    tupleList->length = 0;
    tupleList->number = 0;
}
void initTupleList(ShortList *tupleList, int tupleInitCapacity){
    tupleList->cap = tupleInitCapacity*3;
    tupleList->data = (short *) malloc(sizeof(short) * tupleList->cap);
    resetTupleList(tupleList);
};

void addToTupleList(ShortList *list, short a, short b, short cost){
    if(list->length == list->cap){
        list->cap *= 2;
        list->data = (short*) realloc(list->data, sizeof(short)*list->cap);
        if(list->data == NULL) printf("ERROR: Memory allocation failure for size: %i\n", list->cap);
    }
    list->data[list->length++] = a;
    list->data[list->length++] = b;
    list->data[list->length++] = cost;
    list->number++;
}

bool isTupleInSet(short nodeA, short nodeB, ShortList *list){
    for(int i=0; i < list->length; i+=3){
        if(nodeA == list->data[i] && nodeB == list->data[i+1]) return true;
    }
    return false;
}

bool areTuplesInSet(short *tuples, ShortList *list){
    for(int i=0; i < N_TUPLES*3; i+=2){
        if(isTupleInSet(tuples[i], tuples[i+1], list)) return true;
    }
    return false;
}

void printTupleList(char *name, ShortList *list){
    printf("%s (%i/%i): [", name, list->length/3, list->number);
    for(int i = 0; i < list->length; i+=3){
        printf("(%i->%i, %i), ", list->data[i], list->data[i+1], list->data[i+2]);
    }
    printf("]\n");
}

void initPrevDirty(PrevDirty *list){
    list->cap = PREV_DIRTY_SIZE;
    list->end = 0;
    list->start = 0;
    list->data = (ShortList*) malloc(sizeof(ShortList)*list->cap);
    for(int i=0; i < list->cap; i++){
        ShortList subList;
        initTupleList(&subList, PREV_DIRTY_SUB_SIZE);
        list->data[i] = subList;
    }
}
void addNewIteration(PrevDirty *list){
    if(list->end == list->cap){
        int oldCap = list->cap;
        list->cap += 10; //Increment by 10
        list->data = (ShortList*) realloc(list->data, sizeof(ShortList)*list->cap);
        for(int i=oldCap; i < list->cap; i++){
            ShortList subList;
            initTupleList(&subList, PREV_DIRTY_SUB_SIZE);
            list->data[i] = subList;
        }
    }
    list->end++;
}
void resetPrevDirty(PrevDirty *list){
    for(int i=0; i < list->end; i++){
        list->data[i].length = 0;
        list->data[i].number = 0;
    }
    list->end = 0;
    list->start = 0;
}
void addToPrevDirty(PrevDirty *list, short a, short b, short cost){
    addToTupleList(&list->data[list->end - 1], a, b, cost);
}
void deleteFirstPrevDirty(PrevDirty *list){
    list->start++;
}
bool isInPrevDirty(PrevDirty *list, ShortList *dirty){
    for(int i=list->start; i < list->end; i++){

        bool equal = true;
        ShortList prevDirty = list->data[i];
        if(prevDirty.length != dirty->length) continue;

        for(int k=0; k < prevDirty.length; k+=3){
            if(!isTupleInSet(prevDirty.data[k], prevDirty.data[k+1], dirty)){
                equal = false;
                break;
            }
        }
        if(equal) return true;
    }
    return false;
}
