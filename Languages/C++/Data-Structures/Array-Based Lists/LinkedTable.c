#include <stdio.h>
#include <stdlib.h>

struct Node{
  struct Node * next;
  int data;
};

int main(){
  int n = 10;
  struct Node head;
  struct Node* p=&head;
  for(int j=0; j<n; j++){
    p -> data = j * j;
    p -> next = (struct Node*)malloc(sizeof(struct Node));
    p = p -> next;
  }



  p=&head;//pointer back to head to traverse linked list
  for(int i=0; i<n; i++){
    printf("data of node %d: %d, addr: %p\n", i, p->data, p);
    p = p -> next;
  }

  return 0;
}
