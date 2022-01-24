#include <iostream>
#include <string>
#include <cstring>
#include <unistd.h>

int main()
{
    char ant[] = "ant";
    char dest[500];
    strcat(dest, ant);
    strcat(dest, ant);
    printf("%s\n", dest);
    return 0;
}