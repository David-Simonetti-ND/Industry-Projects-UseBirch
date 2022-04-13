#include <iostream>
#include <vector>
#include <string>
#include <map>

int add(int a, int b) 
{
    return a + b;
}

int main() 
{
    int a = 5;
	while(1){

	}
    int addFive = add(a, 5);
    double myDouble = 6.5;
    int foo [5] = { 16, 2, 77, 40, 12071 };
    int twoDFoo [2][2] = {
    {1,2},
    {3,4}, };
    int threeDFoo[1][1][1] = {{{1}}};
    char character = 'a';
    char test_cstring[] = "Data Structures\n";
    bool isDavidSwag = 1;
    std::string foobar = "Computer Science\n";
    std::vector<int> vect;
    vect.assign(1,3);
    vect.push_back(5);
    vect.pop_back();
    std::vector< std::vector<int> > v1 = {{1, 2, 3}, {4, 5, 6}, {7, 8, 9}};
    std::map<int, float> map = { {5, 3.14}, {10, 6.23556}, {8, 1.2355}, {8, 1.2355}, {9, 1.23525}, {11, 1.235555}};
    std::map<char, int> map2 = { {'a', 1}, {'b', 3}, {'c', 4} };
    for (int i = 0; i < 5; ++i){
        foo[i] = foo[i] + 2;
        std::cout << "Incremented value!" << std::endl;
    }
    return 0;
}
