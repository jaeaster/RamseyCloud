//
// Created by jesper on 5/18/17.
//

#ifndef RAMSEYC_TUPLES_H
#define RAMSEYC_TUPLES_H

typedef struct {
    int length;
    int number;
    int cap;
    short* data; //[a1,b1,cost1,a2,b2,cost2 ...]
} ShortList;

typedef struct {
    int length;
    int cap;
    short** data;
} DirtyTuples;

typedef struct {
    int end;
    int start;
    int cap;
    ShortList* data;
} PrevDirty;

//SlaveSolution:
void initTupleList(ShortList *tupleList, int tupleInitCapacity);
void addToTupleList(ShortList *list, short a, short b, short cost);
void resetTupleList(ShortList *tupleList);

bool isTupleInSet(short nodeA, short nodeB, ShortList *list);
bool areTuplesInSet(short *tuples, ShortList *list);

void printTupleList(char *name, ShortList *list);

//PrevDirty:
void initPrevDirty(PrevDirty *list);
void resetPrevDirty(PrevDirty *list);
void initIteration(PrevDirty *list);
void addToLastPrevDirty(PrevDirty *list, short a, short b, short cost);
void deleteFirstPrevDirty(PrevDirty *list);
bool isInPrevDirty(PrevDirty *list, ShortList *dirty);



#endif //RAMSEYC_TUPLES_H
