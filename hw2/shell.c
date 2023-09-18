#define _GNU_SOURCE //this is needed to be able to use execvpe 
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>
#include <string.h>
#include <sys/resource.h>
#include <sys/types.h>
#include <fcntl.h>

#define MAX_COMMAND_ARGS 64

typedef struct {
  char* binary_path;
  char* stdin;
  char* stdout;
  char* arguments;
  short wait;
} command;

/**
 * @param arg_out allocate for length = MAX_COMMAND_ARGS
 */
void parse_arguments(char* arg_str, char** args) {
  char* token = strtok(arg_str, " ");

  while( token != NULL ) {
    *args = token;
    args++;

    token = strtok(NULL, " ");
  }

  *args = NULL;
}

//function prototypes
void print_parsed_command(command);
short parse_command(command*, char*);

// read a line from a file
short getlinedup(FILE* fp, char** value){
  char* line = NULL;
  size_t n = 0;
  //get one line
  int ret = getline(&line, &n, fp);

  if(ret == -1){
    //the file ended
    return 0;
  }
  //remove \n at the end
  line[strcspn(line, "\n")] = '\0';
  //duplicate the string and set value
  *value = strdup(line);
  free(line);

  return 1;
}

//parse a command_file and set a corresponding command data structure
short parse_command(command* parsed_command, char* cmdfile){
  FILE* fp = fopen(cmdfile, "r");
  if(!fp){
    //the file does not exist
    return 0;
  }

  char* value;
  short ret;
  int intvalue;

  ret = getlinedup(fp,&value);
  if(!ret){
    fclose(fp); return 0;
  }
  parsed_command->binary_path = value;

  ret = getlinedup(fp,&value);
  if(!ret){
    fclose(fp); return 0;
  }
  parsed_command->stdin = value;

  ret = getlinedup(fp,&value);
  if(!ret){
    fclose(fp); return 0;
  }
  parsed_command->stdout = value;

  ret = getlinedup(fp,&value);
  if(!ret){
    fclose(fp); return 0;
  }
  parsed_command->arguments = value;

  ret = getlinedup(fp,&value);
  if(!ret){
    fclose(fp); return 0;
  }
  intvalue = atoi(value);
  if(intvalue != 0 && intvalue != 1){
    fclose(fp); return 0;
  }
  parsed_command->wait = (short)intvalue;

  return 1;
}

//useful for debugging
void print_parsed_command(command parsed_command){
  printf("----------\n");
  printf("binary_path: %s\n", parsed_command.binary_path);
  printf("stdin: %s\n", parsed_command.stdin);
  printf("stdout: %s\n", parsed_command.stdout);
  printf("arguments: %s\n", parsed_command.arguments);
  printf("wait: %d\n", parsed_command.wait);
}

void free_command(command cmd){
  free(cmd.binary_path);
  free(cmd.stdin);
  free(cmd.stdout);
  free(cmd.arguments);
}

void process_command(command parsed_cmd) {
  int announce_proc = fork(); // used to announce completion of binary run

  if (announce_proc < 0) {
    fprintf(stderr, "fork failed\n");
    exit(1);
  } else if (announce_proc == 0) { // announce process
    /**
     * Announce process enables the exit announcement to be made parallel to
     * other events by offloading it to a separate process that owns the command
     * execution process
     */
    int run_proc = fork();

    if (run_proc < 0) {
      fprintf(stderr, "fork failed\n");
      exit(1);
    } else if (run_proc == 0) { // run process
      printf("New child process started <%d>\n", (int) getpid());
      
      if (strlen(parsed_cmd.stdin) > 0) {
        int fd = open(parsed_cmd.stdin, O_WRONLY|O_CREAT|O_TRUNC, 0664);
        dup2(fd, STDIN_FILENO);
        close(fd);
      }

      if (strlen(parsed_cmd.stdout) > 0) {
        int fd = open(parsed_cmd.stdout, O_WRONLY|O_CREAT|O_TRUNC, 0664);
        dup2(fd,STDOUT_FILENO);
        close(fd);
      }

      char* cmd_args[MAX_COMMAND_ARGS+1];
      cmd_args[0] = parsed_cmd.binary_path;
      parse_arguments(parsed_cmd.arguments, &cmd_args[1]);

      execvp(parsed_cmd.binary_path, cmd_args);
    } else { // announce process
      int status;
      waitpid(run_proc, &status, 0);
      printf("Child process <%d> terminated with exit code <%d>\n", run_proc, WEXITSTATUS(status));
      exit(0);
    }
    
  } else { // main process
    if (parsed_cmd.wait == 1) {
      waitpid(announce_proc, NULL, 0);
    }
  }
}

int main(int argc, char *argv[], char* env[]) {
  for(int ncommand=1; ncommand<argc; ncommand++){
    command parsed_command;
    int ret = parse_command(&parsed_command, argv[ncommand]);
    if (!ret){
      printf("command file %s is invalid\n", argv[ncommand]);
      continue;
    }

    print_parsed_command(parsed_command);

    process_command(parsed_command);
  
    free_command(parsed_command);
  }

  while(wait(NULL) > 0); // wait for termination of all child processes
}
