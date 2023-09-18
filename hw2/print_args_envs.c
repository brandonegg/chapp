/**
 * Prints all arguments and environment variables to STDOUT
 */
#include <stdio.h>

int main(int args, char *argv[], char *env[]) 
{
  int n = 0;
  char *cur = argv[n];

  while (cur != NULL) {
    printf("%s\n", cur);
    n++;
    cur = argv[n];
  }

  n = 0;
  cur = env[n];

  while (cur != NULL) {
    printf("%s\n", cur);
    n++;
    cur = env[n];
  }
  return 0;
}
