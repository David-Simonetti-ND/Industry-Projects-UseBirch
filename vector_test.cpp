#include <iostream>
#include <map>
#include <string>
#include <vector>

int main(){
    std::vector<int> intVect;
    intVect.assign(1,3);
    int nums[5]={1,2,3,4,5};
    int nums2[5]={6,7,8,9,10};
    std::vector<char> charVect = {'a','b','c','d'};
    std::vector<int*> arrVect = {nums, nums2};
    std::vector<std::string> stringVect = {"Hello", "Goodbye"};
    std::vector<std::vector<int> > vectorSquared = {{1,2,3}, {4,5,6}, intVect};
    intVect.push_back(5);
    intVect.pop_back();
}