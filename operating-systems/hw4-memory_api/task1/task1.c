#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/mman.h>

// A function that checks if a given address is in the virtual address space of the program
int is_valid_address(void *addr) {
  // Get the page size of the system
  long page_size = sysconf(_SC_PAGESIZE);
  // Align the address to the page boundary
  void *page_start = (void *)((unsigned long)addr & ~(page_size - 1));
  // Use mincore to check if the page is mapped
  unsigned char vec;
  if (mincore(page_start, page_size, &vec) == -1) {
    // The page is not mapped
    return 0;
  }
  // The page is mapped
  return 1;
}

int main(int argc, char *argv[]) {
  if (argc != 2) {
    fprintf(stderr, "Usage: %s <required_address>\n", argv[0]);
    exit(-1);
  }
  // Convert the argument to a pointer
  void *addr = (void *)strtoul(argv[1], NULL, 0);
  // Check if the address is valid
  if (is_valid_address(addr)) {
    // Print the value of the byte at the address
    printf("Is valid");
    printf("%d\n", *(unsigned char *)addr);
    exit(0);
  }
  else {
    // Do nothing and exit with -1
    exit(-1);
  }
}