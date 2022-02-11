#include <iostream>

int main(int argc, const char *argv[])
{
    printf("There are %d arguments to this program\n", argc);
    int i = 0;
    for (i = 0; i < argc; i++)
    {
        printf("Argument %d is: %s\n", i, argv[i]);
    }
    return 0;
}