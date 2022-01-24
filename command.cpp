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
    pid_t child_pid = fork();
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
    else
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
        //printf("Writing %s to gdb\n", file_command);
        write(gdbpipe[1], file_command, strlen(file_command) + 1);
        write(gdbpipe[1], "\nset pagination off\n", 20);
        free(file_command);
    }
    char output_buff[4096];
    /*
    while (1)
    {
        if (!fgets(input_buff, 4096, stdin)) {break;} // keep reading until we recieve an EOF
        //printf("%s\n", input_buff);
        write(gdbpipe[1], input_buff, strlen(input_buff));
        if (strcmp(input_buff, "quit\n"))
        {
            int bytes_read = read(gdbout[0], output_buff, 4096);
            write(1, output_buff, bytes_read);
        }
        
    }
    */
    //write(1, output_buff, bytes_read);
    //printf("%d\n", bytes_read);
    FILE *gdb_in = fdopen(gdbout[0], "r");
    //FILE *gdb_out = fdopen(gdbpipe[1], "w");
    //fprintf(gdb_out, "start");
    
    write(gdbpipe[1], "\nstart\n", 7);
    //write(gdbpipe[1], "\nselect-frame 0\n\n", 18);
    int bytes_read = 1;
    while (bytes_read != 220) 
    {
        fgets(output_buff, 4096, gdb_in);
        bytes_read = strlen(output_buff);
        //printf("%s %d\n", output_buff, bytes_read);
    }
    //write(gdbpipe[1], "\nselect-frame 0\n\n", 18);
    write(gdbpipe[1], "next\n", 5);
    //printf("%d\n", bytes_read);
    memset(output_buff, '\0', 4096);
    bytes_read = 0;
    for(int i = 0; i < 25; i++)
    {
        memset(output_buff, '\0', 4096);
        bytes_read = read(gdbout[0], output_buff, 4096);
        if (bytes_read == 109) {break;}
        write(1, output_buff, bytes_read);
        printf("\n\n");
        usleep(10000);
        write(gdbpipe[1], "next\n", 5);
        write(gdbpipe[1], "info locals\n", 12);
        


        /*
        bytes_read = 0;
        while (!bytes_read)
        {
            bytes_read = read(gdbout[0], output_buff, 4096);
        }
        if (bytes_read != 6)
        {
            write(1, output_buff, bytes_read);
            //printf("%d\n", bytes_read);
        }
        else {continue;}
        if (bytes_read == 98){break;}
        
        //write(gdbpipe[1], "info locals\n", 11);

        write(gdbpipe[1], "next\n", 5);
        //printf("%d\n", bytes_read);
        */
    }
    bytes_read = read(gdbout[0], output_buff, 4096);
    write(1, output_buff, bytes_read);
    write(gdbpipe[1], "quit\n", 5);

    wait(NULL);
    wait(NULL);
    return 0;
}