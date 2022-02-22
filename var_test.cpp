#include <iostream>
#include <vector>
#include <string>
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
    int threeDFoo[1][1][1] = {{{1}}};
    char character = 'a';
    char test_cstring[] = "Data Structures\n";
    bool isDavidSwag = 1;
    // std::vector<int> vect;
    // vect.assign(1,3);
    // vect.push_back(5);
    // vect.pop_back();
    for (int i = 0; i < 5; ++i){
        foo[i] = foo[i] + 2;
        std::cout << "Incremented value!" << std::endl;
    }
    return 0;
}