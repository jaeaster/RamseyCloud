#ifndef DECLARATIONS_H
#define DECLARATIONS_H

#define TEN_SIZE 5000
#define NINE_SIZE 100000

typedef struct {
  int count5, count6, count7, count8, count9, count10;
  int **ten_cliques, **nine_cliques;
  int ten_size, nine_size;
} CliqueInfo;

/* clique_count.c declarations */
int CliqueCount10(int *g,int gsize);
void CliqueCountAll(int *g, int gsize, CliqueInfo *info);

/* tuple_worker.c declarations */
int find_dirty_edges(int* tuple, int** color_set_list, int length);
int proceed_check(int* tuple, int* set_i, int* set_j);
int in_set(int *x, int len, int match);
void set_diff(int *x, int lenx, int *y, int leny, int *diff);
void set_sym_diff(int *x, int lenx, int *y, int leny, int *diff);

/* More declarations */


#endif