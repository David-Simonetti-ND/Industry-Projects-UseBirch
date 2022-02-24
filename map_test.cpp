#include <iostream>
#include <map>
#include <string>
#include <vector>

int main()
{
    std::map<std::string, int> m { {"David", 10}, {"Chris", 15}, {"Kat", 20}, {"Aidan", 5}};
    std::map<std::string, std::map<std::string, int> > mapSquared = {{"hello", m}, {"panda", m}};
    std::vector<char> vect = {'a','b'};
    std::vector<char> vect2 = {'c','d'};
    std::map<int, std::vector<char> > vectMap = {{1, vect}, {2, vect2}};
    std::map<std::string, std::vector<std::string> > useBirchMap = {{"one", {"a", "b", "c", "d"}}, {"two", {"e", "f", "g", "h"}}};
    for (auto i : m)
    {
        std::cout << i.first << " " << i.second << std::endl;
    }
}