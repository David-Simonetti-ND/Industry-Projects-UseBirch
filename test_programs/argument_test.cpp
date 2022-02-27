#include <iostream>

int main(int argc, const char *argv[])
{
    std::cout << "There are " << argc << " arguments to this program\n";
    int i = 0;
    for (i = 0; i < argc; i++)
    {
        std::cout << "Argument " << i << " is: " << argv[i] << std::endl;
    }
    return 0;
}