#include<stdio.h>
int main(){
   int i,k;
   int *a=NULL;
   *a=1;
   for(i=0;i<100000;i++)for(k=0;k<30000;k++);
   printf("B over\n");
   return 0;
}