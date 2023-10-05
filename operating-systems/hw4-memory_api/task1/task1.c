#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <math.h>

void read_file(char* const fileName) {
  FILE* file = fopen(fileName, "r"); /* should check the result */
  char line[256];

  while (fgets(line, sizeof(line), file)) {
      /* note that fgets don't strip the terminating \n, checking its
          presence would allow to handle lines longer that sizeof(line) */
      printf("%s", line); 
  }
  /* may check feof here to make a difference between eof and io failure -- network
      timeout for instance */

  fclose(file);
}

/**
 * @returns 1 if address provided is in the virtual memory otherwise 0
 */
int is_address_in_virt_mem(void *addr) {
  int pid = (int) getpid();

  char fileName[50];
  sprintf(fileName, "/proc/%d/maps", pid);

  read_file(fileName);

  return 0;
}

int main(int argc, char *argv[], char* env[]) {
  if (argc != 2) {
    fprintf(stderr, "Usage: %s <required_address>\n", argv[0]);
    exit(-1);
  }

  char* addr = (char *)strtoul(argv[1], NULL, 16);

  int result = is_address_in_virt_mem(addr);

  exit(-1);
}