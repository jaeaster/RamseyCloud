#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int find_dirty_edges(int* tuple, int** color_set_list, int length);
int proceed_check(int* tuple, int* set_i, int* set_j);
int in_set(int *x, int len, int match);
void set_diff(int *x, int lenx, int *y, int leny, int *diff);
void set_sym_diff(int *x, int lenx, int *y, int leny, int *diff);


int main(int argc, char** argv) {
  // argv[1] = "1,3" - tuple
  // argv[2] = "1,3,4,5,6,7,8,9|1,12,45,45,665,4534,5000"
  // argv[3] = "2" - length
  int i, j, length, tuple[2], **nine_cliques;
  char *p, *q, *z;
  length = atoi(argv[3]);
  z = strtok(argv[1], ",");
  while(z != NULL) {
    tuple[i] = atoi(z);
    z = strtok(NULL, ",");
    i++;
  }
  nine_cliques = (int **)malloc(sizeof(int *) * length);
  for(i = 0; i < length; i++) {
    nine_cliques[i] = (int *)malloc(sizeof(int) * 9);
  }
  i = j = 0;
  char *end_str;
  p = strtok_r(argv[2], "|", &end_str);
  while(p != NULL) {
    char *end_token;
    q = strtok_r(p, ",", &end_token);
    while(q != NULL) {
      nine_cliques[i][j] = atoi(q);
      q = strtok_r(NULL, ",", &end_token);
      j++;
    }
    p = strtok_r(NULL, "|", &end_str);
    j = 0;
    i++;
  }
  find_dirty_edges(tuple, nine_cliques, length);
  return 0;
}


int find_dirty_edges(int* tuple, int** color_set_list, int length) {
  int i, j, k, *set_i, *set_j, diff[18];
  int cost = 0;
  int proved_dirty = 0;
  for(i = 0; i < length - 1; i++) {
    for(j = i + 1; j < length; j++) {
      set_i = color_set_list[i];
      set_j = color_set_list[j];
      if(proceed_check(tuple, set_i, set_j)) {
        set_sym_diff(set_i, 9, set_j, 9, diff);
        for(k = 0; diff[k] != -1; k++);
        if(k == 2 && in_set(diff, 2, tuple[0]) && in_set(diff, 2, tuple[1])) {
          proved_dirty = 1;
          cost += 1;
        }
      }
    }
  }
  printf("%d:%d:%d:%d\n", tuple[0], tuple[1], proved_dirty, cost);
  return cost;
}

int proceed_check(int* tuple, int* set_i, int* set_j) {
  int a = tuple[0];
  int b = tuple[1];
  if((in_set(set_i, 9, a) && in_set(set_j, 9, b)) || (in_set(set_j, 9, a) && in_set(set_i, 9, b))) {
    return 1;
  } else {
    return 0;
  }
}
 
int in_set(int *x, int len, int match)
{
  int i;
  for (i = 0; i < len; i++) {
    if (x[i] == match)
      return 1;
  }
  return 0;
}
 
/* x - y */
void set_diff(int *x, int lenx, int *y, int leny, int *diff)
{
  int i;
  int pos = 0;
  for (i = 0; i < lenx; i++)
    if (!in_set(y, leny, x[i])) {
      diff[pos] = x[i];
      pos++;
    }
  if(pos < 8) {
    diff[pos] = -1;
  }
  return;
}
 
/* X ^ Y */
void set_sym_diff(int *x, int lenx, int *y, int leny, int *ret_diff)
{
  int diff1[9], diff2[9];

  int i, j;
  set_diff(x, lenx, y, leny, diff1);
  set_diff(y, leny, x, lenx, diff2);
  for(i = 0; diff1[i] != -1; i++) {
    ret_diff[i] = diff1[i];
  }
  for(j = 0; diff2[j] != -1; j++, i++) {
    ret_diff[i] = diff2[j];
  }
  if(i < 17) {
    ret_diff[i] = -1;
  }
  return;
}