#include <iostream>
#include <map>
#include <string>

int main()
{
    int x = 5;
    std::map<std::string, int> m { {"David", 10}, {"Chris", 15}, {"Kat", 20}, {"Aidan", 5}};
    for (auto i : m)
    {
        std::cout << i.first << " " << i.second << std::endl;
    }
}