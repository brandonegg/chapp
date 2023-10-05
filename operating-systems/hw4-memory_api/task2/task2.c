#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/mman.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>

int reverse_file_cmp_func(const void* p1, const void* p2) {
  return p2-p1;
}

void reverse_file(char* filePath) {
  int file = open(filePath, O_RDWR);

  struct stat fileStats;
	fstat(file, &fileStats);
	size_t fileSize = fileStats.st_size;

  char *addr = (char *)mmap(0, fileSize, PROT_READ | PROT_WRITE, MAP_SHARED, file, 0);

  qsort(addr, fileSize, 1, reverse_file_cmp_func);
	msync(addr, fileSize, MS_SYNC);

  close(file);
}

int main(int argc, char *argv[], char* env[]) {
  if (argc != 2) {
    fprintf(stderr, "Usage: %s <file_path>\n", argv[0]);
    exit(-1);
  }

  char * filePath = argv[1];

  reverse_file(filePath);
}