#include <stdio.h>
#include <stdlib.h>
#include "declarations.h"

void CliqueCountAll(int *g,int gsize, CliqueInfo *info) {
  int i, j, k, l, m, n, o, p, q, r;
  int sgsize = 10;
  for(i=0;i < gsize-sgsize+1; i++) {
    for(j=i+1;j < gsize-sgsize+2; j++) {
      for(k=j+1;k < gsize-sgsize+3; k++) { 
        if((g[i*gsize+j] == g[i*gsize+k]) && (g[i*gsize+j] == g[j*gsize+k])) {
          for(l=k+1;l < gsize-sgsize+4; l++) { 
            if((g[i*gsize+j] == g[i*gsize+l]) && (g[i*gsize+j] == g[j*gsize+l]) && (g[i*gsize+j] == g[k*gsize+l])) {
              for(m=l+1;m < gsize-sgsize+5; m++) {
                if((g[i*gsize+j] == g[i*gsize+m]) && (g[i*gsize+j] == g[j*gsize+m]) &&(g[i*gsize+j] == g[k*gsize+m]) && (g[i*gsize+j] == g[l*gsize+m])) {
                  info->count5 += 1;
                  if(sgsize <= 5) {
                    info->count10++;
                  } else {
                    for(n=m+1;n<gsize-sgsize+6;n++) {
                      if ((g[i*gsize+j] == g[i*gsize+n]) && (g[i*gsize+j] == g[j*gsize+n]) &&(g[i*gsize+j] == g[k*gsize+n]) && (g[i*gsize+j] == g[l*gsize+n]) &&(g[i*gsize+j] == g[m*gsize+n])) {
                        info->count6 += 1;
                        if(sgsize <= 6){
                          info->count10++;
                        } else {
                          for(o=n+1;o<gsize-sgsize+7;o++) {
                            if ((g[i*gsize+j] == g[i*gsize+o]) && (g[i*gsize+j] == g[j*gsize+o]) &&(g[i*gsize+j] == g[k*gsize+o]) && (g[i*gsize+j] == g[l*gsize+o]) &&(g[i*gsize+j] == g[m*gsize+o]) &&(g[i*gsize+j] == g[n*gsize+o])) {
                              info->count7 += 1;
                              if(sgsize <= 7) {
                                info->count10++;
                              } else {
                                for(p=o+1;p<gsize-sgsize+8;p++){
                                  if ((g[i*gsize+j] == g[i*gsize+p]) && (g[i*gsize+j] == g[j*gsize+p]) &&(g[i*gsize+j] == g[k*gsize+p]) && (g[i*gsize+j] == g[l*gsize+p]) &&(g[i*gsize+j] == g[m*gsize+p]) &&(g[i*gsize+j] == g[n*gsize+p]) &&(g[i*gsize+j] == g[o*gsize+p])) {
                                    info->count8 += 1;
                                    if(sgsize <= 8) {
                                      info->count10++;
                                    } else {
                                      for(q=p+1;q<gsize-sgsize+9;q++){
                                        if ((g[i*gsize+j] == g[i*gsize+q]) && (g[i*gsize+j] == g[j*gsize+q]) &&(g[i*gsize+j] == g[k*gsize+q]) && (g[i*gsize+j] == g[l*gsize+q]) &&(g[i*gsize+j] == g[m*gsize+q]) &&(g[i*gsize+j] == g[n*gsize+q]) &&(g[i*gsize+j] == g[o*gsize+q]) &&(g[i*gsize+j] == g[p*gsize+q])) {
                                          if(info->count9 == info->nine_size) {
                                            // Reallocate nine_cliques
                                            info->nine_size *= 2;
                                            info->nine_cliques = (int **)realloc((void *)info->nine_cliques, info->nine_size);
                                          }
                                          info->nine_cliques[info->count9][0] = i;
                                          info->nine_cliques[info->count9][1] = j;
                                          info->nine_cliques[info->count9][2] = k;
                                          info->nine_cliques[info->count9][3] = l;
                                          info->nine_cliques[info->count9][4] = m;
                                          info->nine_cliques[info->count9][5] = n;
                                          info->nine_cliques[info->count9][6] = o;
                                          info->nine_cliques[info->count9][7] = p;
                                          info->nine_cliques[info->count9][8] = q;
                                          info->count9++;
                                          if(sgsize <= 9) {
                                            info->count10++;
                                          } else {
                                            for(r=q+1;r<gsize-sgsize+10;r++){
                                              if((g[i*gsize+j] == g[i*gsize+r]) && (g[i*gsize+j] == g[j*gsize+r]) &&(g[i*gsize+j] == g[k*gsize+r]) && (g[i*gsize+j] == g[l*gsize+r]) &&(g[i*gsize+j] == g[m*gsize+r]) &&(g[i*gsize+j] == g[n*gsize+r]) &&(g[i*gsize+j] == g[o*gsize+r]) &&(g[i*gsize+j] == g[p*gsize+r]) &&(g[i*gsize+j] == g[q*gsize+r])) { 
                                                if(info->count10 == info->ten_size) {
                                                  // Reallocate ten_cliques
                                                  info->ten_size *= 2;
                                                  info->ten_cliques = (int **)realloc((void *)info->ten_cliques, info->ten_size);
                                                }
                                                info->ten_cliques[info->count10][0] = i;
                                                info->ten_cliques[info->count10][1] = j;
                                                info->ten_cliques[info->count10][2] = k;
                                                info->ten_cliques[info->count10][3] = l;
                                                info->ten_cliques[info->count10][4] = m;
                                                info->ten_cliques[info->count10][5] = n;
                                                info->ten_cliques[info->count10][6] = o;
                                                info->ten_cliques[info->count10][7] = p;
                                                info->ten_cliques[info->count10][8] = q;
                                                info->ten_cliques[info->count10][9] = r;
                                                info->count10++;
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
  }
  return;
}

int CliqueCount10(int *g,int gsize) {
  int i;
  int j;
  int k;
  int l;
  int m;
  int n;
  int o;
  int p;
  int q;
  int r;
  int count=0;
  int sgsize = 10;
  for(i=0;i < gsize-sgsize+1; i++) {
    for(j=i+1;j < gsize-sgsize+2; j++) {
      for(k=j+1;k < gsize-sgsize+3; k++) { 
        if((g[i*gsize+j] == g[i*gsize+k]) && (g[i*gsize+j] == g[j*gsize+k])) {
          for(l=k+1;l < gsize-sgsize+4; l++) { 
            if((g[i*gsize+j] == g[i*gsize+l]) && (g[i*gsize+j] == g[j*gsize+l]) && (g[i*gsize+j] == g[k*gsize+l])) {
              for(m=l+1;m < gsize-sgsize+5; m++) {
                if((g[i*gsize+j] == g[i*gsize+m]) && (g[i*gsize+j] == g[j*gsize+m]) &&(g[i*gsize+j] == g[k*gsize+m]) && (g[i*gsize+j] == g[l*gsize+m])) {
                  if(sgsize <= 5) {
                    count++;
                  } else {
                    for(n=m+1;n<gsize-sgsize+6;n++) {
                      if ((g[i*gsize+j] == g[i*gsize+n]) && (g[i*gsize+j] == g[j*gsize+n]) &&(g[i*gsize+j] == g[k*gsize+n]) && (g[i*gsize+j] == g[l*gsize+n]) &&(g[i*gsize+j] == g[m*gsize+n])) {
                        if(sgsize <= 6){
                          count++;
                        } else {
                          for(o=n+1;o<gsize-sgsize+7;o++) {
                            if ((g[i*gsize+j] == g[i*gsize+o]) && (g[i*gsize+j] == g[j*gsize+o]) &&(g[i*gsize+j] == g[k*gsize+o]) && (g[i*gsize+j] == g[l*gsize+o]) &&(g[i*gsize+j] == g[m*gsize+o]) &&(g[i*gsize+j] == g[n*gsize+o])) {
                              if(sgsize <= 7) {
                                count++;
                              } else {
                                for(p=o+1;p<gsize-sgsize+8;p++){
                                  if ((g[i*gsize+j] == g[i*gsize+p]) && (g[i*gsize+j] == g[j*gsize+p]) &&(g[i*gsize+j] == g[k*gsize+p]) && (g[i*gsize+j] == g[l*gsize+p]) &&(g[i*gsize+j] == g[m*gsize+p]) &&(g[i*gsize+j] == g[n*gsize+p]) &&(g[i*gsize+j] == g[o*gsize+p])) {
                                    if(sgsize <= 8) {
                                      count++;
                                    } else {
                                      for(q=p+1;q<gsize-sgsize+9;q++){
                                        if ((g[i*gsize+j] == g[i*gsize+q]) && (g[i*gsize+j] == g[j*gsize+q]) &&(g[i*gsize+j] == g[k*gsize+q]) && (g[i*gsize+j] == g[l*gsize+q]) &&(g[i*gsize+j] == g[m*gsize+q]) &&(g[i*gsize+j] == g[n*gsize+q]) &&(g[i*gsize+j] == g[o*gsize+q]) &&(g[i*gsize+j] == g[p*gsize+q])) { 
                                          if(sgsize <= 9) {
                                            count++;
                                          } else {
                                            for(r=q+1;r<gsize-sgsize+10;r++){
                                              if((g[i*gsize+j] == g[i*gsize+r]) && (g[i*gsize+j] == g[j*gsize+r]) &&(g[i*gsize+j] == g[k*gsize+r]) && (g[i*gsize+j] == g[l*gsize+r]) &&(g[i*gsize+j] == g[m*gsize+r]) &&(g[i*gsize+j] == g[n*gsize+r]) &&(g[i*gsize+j] == g[o*gsize+r]) &&(g[i*gsize+j] == g[p*gsize+r]) &&(g[i*gsize+j] == g[q*gsize+r])) { 
                                                count++;
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
  }
  return(count);
}