//
// Created by jesper on 5/16/17.
//
#include <stdio.h>
#include <dirent.h>
#include <string.h>
#include <stdlib.h>
#include "../include/io.h"

char nameHolder[100];
void generateFileName(int size){
    sprintf(nameHolder,"%sramsey-%03i.txt", RESULT_PATH, size);
}

void writeToFile(int size, int m[][M_SIZE]){
    generateFileName(size);
    FILE *fp = fopen(nameHolder, "w");
    if(!fp) printf("ERROR: Failed to open file for writing: %s\n",nameHolder);

    for(int i=0; i < size; i++){
        for(int j=0; j < size; j++){
            fprintf(fp, "%i", m[i][j]);
        }
        fprintf(fp, "\n");
    }

    fclose(fp);
    printf("File saved successfully to %s\n", nameHolder);
}
void readFromFile(int size, int m[][M_SIZE]){
    generateFileName(size);
    FILE *fp = fopen(nameHolder, "r");
    if(!fp) printf("ERROR: Failed to open file for reading: %s\n", nameHolder);

    for(int i=0; i < size; i++){
        for(int j=0; j < size; j++){
            fscanf(fp, "%1d", &m[i][j]);
        }
    }
    fclose(fp);
    printf("File with size %i read\n", size);
}
int getHighestFileSize(){

    DIR *dir;
    struct dirent *ent;
    if ((dir = opendir (RESULT_PATH)) == NULL){
        printf("ERROR: Could not open dir %s\n", RESULT_PATH);
        return -1;
    }

    int highestSize = 0;

    // Go through all files:
    while ((ent = readdir (dir)) != NULL) {
        char *str = strdup(ent->d_name);  // We own str's memory now.
        char *token;
        token = strtok(str, "-");
        if(token == NULL || strcmp(token, "ramsey")){
            free(str);
            continue;
        }
        token = strtok(NULL, ".");
        if(token == NULL){
            free(str);
            continue;
        }
        int size = atoi(token);
        if(size > highestSize){
            highestSize = size;
        }
        free(str);
    }
    closedir(dir);

    if(highestSize == 0){
        printf("ERROR: Could not find any ramsey files in dir %s\n", RESULT_PATH);
        return -1;
    }
    return highestSize;
}
