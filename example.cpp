#include <iostream>
int add(int a, int b) 
{
    return a + b;
}

int main() 
{
    int a = 5;
    int addFive = add(a, 5);
    double myDouble = 6.5;
    int foo [5] = { 16, 2, 77, 40, 12071 };
    int twoDFoo [2][2] = {
    {1,2},
    {3,4},
    };
    char brace = '{';
    for (int i = 0; i < 5; ++i){
        foo[i] = foo[i] + 2;
        std::cout << "Incremented value!" << std::endl;
    }
    return 0;
}