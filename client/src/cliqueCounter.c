#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <pthread.h>
#include "../include/cliqueCounter.h"

void initCliqueList(Cliques *info, int capacity){
    info->count = 0;
    info->ten_capacity = capacity;
    info->data = (short **) malloc(sizeof(short *) * TEN_SIZE);
    for (int i = 0; i < info->ten_capacity; i++) {
        info->data[i] = (short *) malloc(sizeof(short) * 11);
    }
}
void resetCliqueList(Cliques *info){
    info->count = 0;
}
void freeInfo(Cliques *info){
    for(int i = 0; i < info->ten_capacity; i++){
        free(info->data[i]);
        info->data[i] = NULL;
    }
    free(info->data);
    info->data = NULL;
}

short* getLast(Cliques *info){
    return info->data[info->count - 1];
}

bool areCliquesEqual(short* c1, short* c2){
    for(int i=0; i < 11; i++){
        if(c1[i] != c2[i]){
            return false;
        }
    }
    return true;
}
bool doesSetsIntersect(Cliques *s1, Cliques *s2){
    for(int i=0; i < s1->count; i++){
        for(int j=0; j < s2->count; j++){
            if(areCliquesEqual(s1->data[i], s2->data[j])){
                return true;
            }
        }
    }
    return false;
}

//Increases memory if needed before an add.
void prepareToAdd(Cliques *info){
    if (info->count < info->ten_capacity) return;
    int newSize = info->ten_capacity*2;
    info->data = (short**) realloc(info->data, sizeof(short*)*newSize);
    if(info->data == NULL){
        printf("ERROR: Memory allocation failure for size: %i \n", info->ten_capacity);
        return;
    }
    for(int i = info->ten_capacity; i < newSize; i++){
        info->data[i] = (short *) malloc(sizeof(short) * 11);
    }
    info->ten_capacity = newSize;
}


pthread_t tid[M_SIZE];
Cliques infos[M_SIZE];
int threadArg[M_SIZE];
int mSize;

void * cliqueCountT(void *arg){
    short j, k, l, m, n, o, p, q, r;
    short i = *((short*) arg);
    Cliques *info = &infos[i];
    int size = mSize - 10;

    for (j = i + 1; j < size + 2; j++) {
        for (k = j + 1; k < size + 3; k++) {
            short ij = matrix[i][j];
            if ((ij != matrix[i][k]) ||
                (ij != matrix[j][k])) continue;

            for (l = k + 1; l < size + 4; l++) {
                if ((ij != matrix[i][l]) ||
                    (ij != matrix[j][l]) ||
                    (ij != matrix[k][l])) continue;

                for (m = l + 1; m < size + 5; m++) {
                    if ((ij != matrix[i][m]) ||
                        (ij != matrix[j][m]) ||
                        (ij != matrix[k][m]) ||
                        (ij != matrix[l][m])) continue;

                    for (n = m + 1; n < size + 6; n++) {
                        if ((ij != matrix[i][n]) ||
                            (ij != matrix[j][n]) ||
                            (ij != matrix[k][n]) ||
                            (ij != matrix[l][n]) ||
                            (ij != matrix[m][n])) continue;

                        for (o = n + 1; o < size + 7; o++) {
                            if ((ij != matrix[i][o]) ||
                                (ij != matrix[j][o]) ||
                                (ij != matrix[k][o]) ||
                                (ij != matrix[l][o]) ||
                                (ij != matrix[m][o]) ||
                                (ij != matrix[n][o])) continue;

                            for (p = o + 1; p < size + 8; p++) {
                                if ((ij != matrix[i][p]) ||
                                    (ij != matrix[j][p]) ||
                                    (ij != matrix[k][p]) ||
                                    (ij != matrix[l][p]) ||
                                    (ij != matrix[m][p]) ||
                                    (ij != matrix[n][p]) ||
                                    (ij != matrix[o][p])) continue;

                                for (q = p + 1; q < size + 9; q++) {
                                    if ((ij != matrix[i][q]) ||
                                        (ij != matrix[j][q]) ||
                                        (ij != matrix[k][q]) ||
                                        (ij != matrix[l][q]) ||
                                        (ij != matrix[m][q]) ||
                                        (ij != matrix[n][q]) ||
                                        (ij != matrix[o][q]) ||
                                        (ij != matrix[p][q])) continue;

                                    for (r = q + 1; r < size + 10; r++) {
                                        if ((ij != matrix[i][r]) ||
                                            (ij != matrix[j][r]) ||
                                            (ij != matrix[k][r]) ||
                                            (ij != matrix[l][r]) ||
                                            (ij != matrix[m][r]) ||
                                            (ij != matrix[n][r]) ||
                                            (ij != matrix[o][r]) ||
                                            (ij != matrix[p][r]) ||
                                            (ij != matrix[q][r])) continue;

                                        if (info->ten_capacity == 0){
                                            //For use by cliqueCount10.
                                            info->count++;
                                            continue;
                                        }

                                        prepareToAdd(info);
                                        int c = info->count;
                                        info->data[c][0] = ij;
                                        info->data[c][1] = i;
                                        info->data[c][2] = j;
                                        info->data[c][3] = k;
                                        info->data[c][4] = l;
                                        info->data[c][5] = m;
                                        info->data[c][6] = n;
                                        info->data[c][7] = o;
                                        info->data[c][8] = p;
                                        info->data[c][9] = q;
                                        info->data[c][10] = r;
                                        info->count++;
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    return NULL;
}
void cliqueCountInit(){
    for(int i=0; i < M_SIZE; i++){
        threadArg[i] = i;
        initCliqueList(&infos[i], 1000);
    }
}

void cliqueCountAllT(int size, Cliques *info){
    mSize = size;
    int iSize = size - 10 + 1;
    for(int i = 0; i < iSize; i++){
        resetCliqueList(&infos[i]);
        pthread_create(&tid[i], NULL, cliqueCountT, (void*)(threadArg+i));
    }
    for(int i=0; i < iSize; i++){
        pthread_join(tid[i], NULL);
    }
    for(int i=0; i < iSize; i++){
        for(int j=0; j < infos[i].count; j++){
            prepareToAdd(info);
            int c = info->count;
            for(int k=0; k < 11; k++){
                info->data[c][k] = infos[i].data[j][k];
            }
            info->count++;
        }
    }
}


void cliqueCountAll(int size, int g[M_SIZE][M_SIZE], Cliques *info) {
    short i, j, k, l, m, n, o, p, q, r;
    size = size - 10;

    for (i = 0; i < size + 1; i++) {
        for (j = i + 1; j < size + 2; j++) {
            for (k = j + 1; k < size + 3; k++) {
                short ij = g[i][j];
                if ((ij != g[i][k]) ||
                    (ij != g[j][k])) continue;

                for (l = k + 1; l < size + 4; l++) {
                    if ((ij != g[i][l]) ||
                        (ij != g[j][l]) ||
                        (ij != g[k][l])) continue;

                    for (m = l + 1; m < size + 5; m++) {
                        if ((ij != g[i][m]) ||
                            (ij != g[j][m]) ||
                            (ij != g[k][m]) ||
                            (ij != g[l][m])) continue;

                        for (n = m + 1; n < size + 6; n++) {
                            if ((ij != g[i][n]) ||
                                (ij != g[j][n]) ||
                                (ij != g[k][n]) ||
                                (ij != g[l][n]) ||
                                (ij != g[m][n])) continue;

                            for (o = n + 1; o < size + 7; o++) {
                                if ((ij != g[i][o]) ||
                                    (ij != g[j][o]) ||
                                    (ij != g[k][o]) ||
                                    (ij != g[l][o]) ||
                                    (ij != g[m][o]) ||
                                    (ij != g[n][o])) continue;

                                for (p = o + 1; p < size + 8; p++) {
                                    if ((ij != g[i][p]) ||
                                        (ij != g[j][p]) ||
                                        (ij != g[k][p]) ||
                                        (ij != g[l][p]) ||
                                        (ij != g[m][p]) ||
                                        (ij != g[n][p]) ||
                                        (ij != g[o][p])) continue;

                                    for (q = p + 1; q < size + 9; q++) {
                                        if ((ij != g[i][q]) ||
                                            (ij != g[j][q]) ||
                                            (ij != g[k][q]) ||
                                            (ij != g[l][q]) ||
                                            (ij != g[m][q]) ||
                                            (ij != g[n][q]) ||
                                            (ij != g[o][q]) ||
                                            (ij != g[p][q])) continue;

                                        for (r = q + 1; r < size + 10; r++) {
                                            if ((ij != g[i][r]) ||
                                                (ij != g[j][r]) ||
                                                (ij != g[k][r]) ||
                                                (ij != g[l][r]) ||
                                                (ij != g[m][r]) ||
                                                (ij != g[n][r]) ||
                                                (ij != g[o][r]) ||
                                                (ij != g[p][r]) ||
                                                (ij != g[q][r])) continue;

                                            if (info->ten_capacity == 0){
                                                //For use by cliqueCount10.
                                                info->count++;
                                                continue;
                                            }

                                            prepareToAdd(info);
                                            int c = info->count;
                                            info->data[c][0] = ij;
                                            info->data[c][1] = i;
                                            info->data[c][2] = j;
                                            info->data[c][3] = k;
                                            info->data[c][4] = l;
                                            info->data[c][5] = m;
                                            info->data[c][6] = n;
                                            info->data[c][7] = o;
                                            info->data[c][8] = p;
                                            info->data[c][9] = q;
                                            info->data[c][10] = r;
                                            info->count++;
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}

int cliqueCount10(int size, int g[M_SIZE][M_SIZE]) {
    Cliques info;
    info.ten_capacity = 0;
    info.count = 0;
    cliqueCountAll(size, g, &info);
    return info.count;
}
