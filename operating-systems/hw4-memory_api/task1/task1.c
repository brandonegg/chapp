#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>

/**
 * @param line Input line to read from
 * @param startRange output start hex value for the line's memory range
 * @param endRange output end hex value for the line's memory range
 */
void parse_mem_map_line_range(char* line, unsigned long* startRange, unsigned long* endRange) {
  int foundSplit = 0;
  int offset = 0; //tracks offset of either start or end range str

  int result = sscanf(line, "%lx-%lx %*s", startRange, endRange);
}

/**
 * @returns 1 if address provided is in the virtual memory otherwise 0
 */
int is_address_in_virt_mem(unsigned long *addr) {
  int pid = (int) getpid();
  unsigned long *startRangePtr = (unsigned long*) malloc(sizeof(unsigned long));
  unsigned long *endRangePtr = (unsigned long*) malloc(sizeof(unsigned long));

  char fileName[50];
  sprintf(fileName, "/proc/%d/maps", pid);

  FILE* file = fopen(fileName, "r");
  char line[256];

  while (fgets(line, sizeof(line), file)) {
    parse_mem_map_line_range(line, startRangePtr, endRangePtr);

    if (*startRangePtr <= *addr && *endRangePtr >= *addr) {
      free(startRangePtr);
      free(endRangePtr);

      return 1;
    }
  }

  fclose(file);

  free(startRangePtr);
  free(endRangePtr);

  return 0;
}

/**
 * Prints the 2 least significant hex digits of the value at the specified memory address.
 *
 * @note Assumes the address is in applications virtual memory map.
 */
void print_address(unsigned long * addr) {
  char* valuePtr = (char*) *addr; // 1 char = 1 byte = 2 hex digits
  printf("%02x\n", *valuePtr);
}

int main(int argc, char *argv[], char* env[]) {
  if (argc != 2) {
    fprintf(stderr, "Usage: %s <required_address>\n", argv[0]);
    exit(-1);
  }

  unsigned long addr = (unsigned long)strtoul(argv[1], NULL, 16);

  int result = is_address_in_virt_mem(&addr);

  if (result == 0) {
    exit(-1);
  }

  print_address(&addr);
}
