#include <unistd.h>
#include <iostream>
#include <cstring>
#include <sys/wait.h>
#include <fcntl.h>
#include <stdio.h>

int main(int argc, const char *argv[])
{
    if (argc != 2)
    {
        fprintf(stderr, "Please only input one argument as the process you wish to run\n");
        exit(1);
    }
    int pipefd[2]; // variable to store the file descriptors for the master program and running process pipe
    if (pipe(pipefd)) // create pipe both master program and running process can access
    {
        fprintf(stderr, "Unable to create pipe: %s\n", strerror(errno));
        exit(1);
    }
    pid_t child_pid = fork(); // create child process to run
    if (child_pid < 0) 
    {
        fprintf(stderr, "Unable to fork process: %s\n", strerror(errno));
        exit(1);
    }
    else if (child_pid == 0)
    {
        std::cout << "I am the child process\n";
        // close output of pipe and close stdin of child process
        if (close(pipefd[1]))  
        { 
            fprintf(stderr, "Unable to close child stdout of pipe: %s\n", strerror(errno));
            exit(1);
        }
        if (close(0))  
        { 
            fprintf(stderr, "Unable to close stdin of child process: %s\n", strerror(errno));
            exit(1);
        }
        // duplicate the input of the pipe to become the process stdin
        if (dup(pipefd[0]))
        {
            fprintf(stderr, "Unable to replace stdin of child with pipe: %s\n", strerror(errno));
            exit(1);
        }
        if (close(1))  
        { 
            fprintf(stderr, "Unable to close stdout of child process: %s\n", strerror(errno));
            exit(1);
        }
        // run the program we wish to analyze
        execl(argv[1], argv[1], NULL);
        fprintf(stderr, "Unable to exec target process: %s\n", strerror(errno));
        exit(1);
    }
    else // what the master program will do
    {
        std::cout << "I am parent process\n";
        if (close(pipefd[0]))  
        { 
            fprintf(stderr, "Unable to close master stdin of pipe: %s\n", strerror(errno));
            exit(1);
        }
    }
    int gdbpipe[2];
    if (pipe(gdbpipe)) // create pipe both master program and running process can access
    {
        fprintf(stderr, "Unable to create pipe: %s\n", strerror(errno));
        exit(1);
    }
    int gdbout[2];
    if (pipe(gdbout)) // create pipe both master program and running process can access
    {
        fprintf(stderr, "Unable to create pipe: %s\n", strerror(errno));
        exit(1);
    }
    pid_t gdb_pid = fork();
    if (gdb_pid < 0) 
    {
        fprintf(stderr, "Unable to fork process for gdb: %s\n", strerror(errno));
        exit(1);
    }
    else if (gdb_pid == 0)
    {
        std::cout << "I am the gdb process\n";
        // close output of pipe and close stdin of child process
        if (close(gdbpipe[1]))  
        { 
            fprintf(stderr, "Unable to close gdb stdout of pipe: %s\n", strerror(errno));
            exit(1);
        }
        if (close(0))  
        { 
            fprintf(stderr, "Unable to close stdin of gdb process: %s\n", strerror(errno));
            exit(1);
        }
        // duplicate the input of the pipe to become the process stdin
        if (dup2(gdbpipe[0], 0))
        {
            fprintf(stderr, "Unable to replace stdin of gdb with pipe: %s\n", strerror(errno));
            exit(1);
        }
        if (close(gdbout[0]))  
        { 
            fprintf(stderr, "Unable to close gdb stdout of pipe: %s\n", strerror(errno));
            exit(1);
        }
        if (close(1))  
        { 
            fprintf(stderr, "Unable to close stdin of gdb process: %s\n", strerror(errno));
            exit(1);
        }
        // duplicate the input of the pipe to become the process stdin
        if (dup2(gdbout[1], 1) != 1)
        {
            fprintf(stderr, "Unable to replace stdout of gdb with pipe: %s\n", strerror(errno));
            exit(1);
        }
        char pid_dest[1024];
        sprintf(pid_dest, "--pid=%d", child_pid);
        // run the program we wish to analyze
        execl("/usr/bin/gdb", pid_dest, NULL);
        fprintf(stderr, "Unable to exec target process: %s\n", strerror(errno));
        exit(1);
    }
    else
    {
        std::cout << "I am parent process\n";
        if (close(gdbpipe[0]))  
        { 
            fprintf(stderr, "Unable to close master stdin of gdbpipe: %s\n", strerror(errno));
            exit(1);
        }
        if (close(gdbout[1]))  
        { 
            fprintf(stderr, "Unable to close master stdin of gdbpipe: %s\n", strerror(errno));
            exit(1);
        }
        char *file_command = (char *)malloc( sizeof(char) * (5 + strlen(argv[1]) + 2) );
        if (file_command == NULL)
        {
            fprintf(stderr, "Unable to allocate memory: %s\n", strerror(errno));
            exit(1);
        }
        sprintf(file_command, "file %s\n", argv[1]);
        int file_ret = write(gdbpipe[1], file_command, strlen(file_command) + 1);
        if (file_ret <= -1)
        {
            fprintf(stderr, "Writing file to gdb failed: %s", strerror(errno));
            exit(1);
        }
        free(file_command);
    }
    char output_buff[4096];

    int flags = fcntl(gdbout[0], F_GETFL, 0);
    int fcntl_ret = fcntl(gdbout[0], F_SETFL, flags | O_NONBLOCK);
    if (fcntl_ret <= -1)
    {
        fprintf(stderr, "Unable to make gdboutput nonblocking: %s", strerror(errno));
        exit(1);
    }
    

    int output_fd = open("out.txt", O_CREAT|O_WRONLY, 0700);
    if (output_fd <= -1)
    {
        fprintf(stderr, "Unable to open output file out.txt: %s", strerror(errno));
        exit(1);
    }
    int bytes_written = write(gdbpipe[1], "\nstart\n", 7);
    if (bytes_written <= -1)
    {
        fprintf(stderr, "Unable to write to gdb: %s", strerror(errno));
        exit(1);
    }
    int bytes_read = 0;
    char end_str[] = "exited normally";
    char *temp_end;
    int i = 0;
    while(1)
    {
        usleep(100000);
        int w_ret = write(gdbpipe[1], "next\n", 5);
        printf("Wrote %d bytes to gdb\n", w_ret);
        int bytes_read = 1;
        while ( 1 )
        {
            bytes_read = read(gdbout[0], output_buff, 4096);
            if (bytes_read <= 0)
            {
                if (errno == EAGAIN) break;
                fprintf(stderr, "Unable to read from gdb: %s", strerror(errno));
                exit(1);
            }
            temp_end = strstr(output_buff, end_str);
            
            printf("Read %d bytes from gdb\n", bytes_read);
            if (bytes_read == -1) break;
            write(output_fd, output_buff, bytes_read);
            write(1, output_buff, bytes_read);
        }
        if (temp_end != NULL){break;}
    }
    int w_ret = write(gdbpipe[1], "quit\n", 5);
    wait(NULL);
    wait(NULL);
    return 0;
}