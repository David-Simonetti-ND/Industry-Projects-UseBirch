#include <iostream>
#include <string>
#include <cstring>
#include <unistd.h>

int main()
{
    int x = 5;
    int z[5];
    for (int y = 0 ; y < x; y++)
    {
        z[y] = y;
        std::cout << "y: " << y <<  " z: " << z[y] << "\n";
    }
    return 0;
}