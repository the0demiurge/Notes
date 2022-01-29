```c
#include <pthread.h>
#include <stdio.h>
#include <unistd.h>

void *thread_func(void *p) {
    for (int j = 0; j < 5; j++) {
        printf("%s\n", (char *)p);
        sleep(1);
    }

    return NULL;
}

int main() {
    pthread_t t1, t2;
    pthread_create(&t1, 0, thread_func, "1st thread");
    pthread_create(&t2, 0, thread_func, "2nd thread");
    pthread_join(t1, NULL);
    pthread_join(t2, NULL);
}
```
