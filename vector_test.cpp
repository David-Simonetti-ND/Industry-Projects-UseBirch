#include <iostream>
#include <map>
#include <string>
#include <vector>

int main(){
    std::vector<int> intVect;
    intVect.assign(1,3);
    std::vector<char> charVect = {'a','b','c','d'};
    charVect.push_back('e');
    std::vector<std::string> stringVect = {"Hello", "Goodbye"};
    std::vector<std::vector<std::string>> v1 = {{"Hi", "Some", "DHSIJFDSBGBGUFGEWFB"}};
    std::vector<std::vector<int> > vectorSquared = {{1,2,3}, {4,5,6}, intVect};
    intVect.push_back(5);
    intVect.pop_back();
}