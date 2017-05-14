#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "declarations.h"

int main(int argc, char** argv) {
  int i;
  int matrix_size = atoi(argv[1]);
  int matrix[matrix_size * matrix_size];
  CliqueInfo info = { 0, 0, 0, 0, 0, 0, NULL, NULL, TEN_SIZE, NINE_SIZE };
  info.ten_cliques = (int **)malloc(sizeof(int*) * TEN_SIZE);
  info.nine_cliques = (int **)malloc(sizeof(int*) * NINE_SIZE);
  for(i = 0; i < TEN_SIZE; i++) {
    info.ten_cliques[i] = (int *)malloc(sizeof(int) * 10);
  }
  for(i = 0; i < NINE_SIZE; i++) {
    info.nine_cliques[i] = (int *)malloc(sizeof(int) * 9);
  }
  for(i = 0; i < matrix_size*matrix_size; i++) {
    matrix[i] = argv[2][i] - '0';
  }
  CliqueCountAll(matrix, matrix_size, &info);
  return 0;
}