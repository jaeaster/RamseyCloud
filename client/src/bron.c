//
// Created by jesper on 5/19/17.
//

#include "../include/constants.h"
#include "../include/cliqueCounter.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct{
    int length;
    int cap;
    int* data;
}List;

void List_init(List *list){
    list->length = 0;
    list->cap = 100;
    list->data = malloc(sizeof(int)*list->cap);
}

void List_append(List *list, int val){
    if(list->length == list->cap){
        list->cap *= 2;
        list->data = realloc(list->data, sizeof(int)*list->cap);
    }
    list->data[list->length++] = val;
}
void List_removeLast(List *list){
    list->length--;
}

void List_copy(List* newList, List *oldList){
    newList->length = oldList->length;
    newList->cap = oldList->cap;
    size_t size = sizeof(int)*newList->cap;
    newList->data = malloc(size);
    memcpy(newList->data, oldList->data, size);
}

void List_removeIndex(List *list, int index){
    if (list->length==1){
        free(list->data);
        list->data = NULL;
    } else {
        for(int i = index; i < list->length-1;i++){
            list->data[i] = list->data[i+1];
        }
    }
    list->length--;
}

int List_clear(List *list){
    free(list->data);
    list->data = NULL;
    list->length = 0;
    list->cap = 0;
    return 0;
}

void List_print(List *list){
    if(list->length == 0){
        printf("Empty\n");
    }else{
        for(int i=0; i < list->length; i++){
            printf("%i ", list->data[i]);
        }
        printf("\n");
    }
}

void bk(int size, int m[M_SIZE][M_SIZE], List *R, List*P, List*X, int depth, Cliques *info){
    //printf("--- depth %i ---------\n", depth);
    //printf("R: "); List_print(R);
    //printf("P: "); List_print(P);
    //printf("X: "); List_print(X);


    if((P->length == 0 && X->length == 0) || depth == 10){
        if(depth == 10){
            info->count++;
            //printf("MAX:"); List_print(R);
        }
        return;
    }

    List newP, newX;
    List_init(&newP);
    List_init(&newX);

    while(P->length > 0){
        int v = P->data[P->length - 1];

        //printf("P-l= %i, v = %i\n", P->length, v);

        newP.length = 0; //Resetting
        newX.length = 0; //Resetting

        //Calculating new X and P:
        for(int i=0; i < size; i++){
            if(m[v][i] != 1 || i==v) continue;
            for(int j=0; j < P->length; j++){
                if(P->data[j] == i){
                    List_append(&newP, i);
                }
            }
            for(int j=0; j < X->length; j++){
                if(X->data[j] == i){
                    List_append(&newX, i);
                }
            }
        }


        //Running recursively:
        List_append(R, v);
        bk(size, m, R, &newP, &newX, depth+1, info);
        List_removeLast(R);

        //After:
        List_removeLast(P);
        List_append(X, v);
    }
    List_clear(&newP);
    List_clear(&newX);
}

void runbk(int size, int matrix[M_SIZE][M_SIZE], Cliques *info){
    List R, P, X;
    List_init(&R);
    List_init(&P);
    List_init(&X);

    for(int v = size-1; v >= 0; v--){
        List_append(&P, v);
    }
    bk(size, matrix, &R, &P, &X, 0, info);
}
