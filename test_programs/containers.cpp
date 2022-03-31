#include <iostream>
#include <array>
#include <forward_list>
#include <list>
#include <stack>
#include <deque>
#include <queue>
#include <set>
#include <map>
#include <unordered_set>
#include <unordered_map>

int main()
{
    std::array<int, 5> arr = {1, 2, 3, 4, 5};
    std::forward_list<int> sllist = {6, 7, 8, 9, 10};
    std::list<int> dllist = {11, 12, 13, 14, 15};
    std::deque<int> d = {7, 5, 16, 8};
    std::queue<int> q(d);
    std::priority_queue<int> pq;
    pq.push(50);
    pq.push(40);
    pq.push(60);
    pq.push(70);
    std::stack<int> stack;
    stack.push(-6); 
    stack.push(-7);
    stack.push(-8);
    stack.push(-9);
    std::set<int> set;
    set.insert(1);
    set.insert(2);
    set.insert(3);
    set.insert(4);
    std::multiset<int, std::greater<int> > multset;
    multset.insert(40);
    multset.insert(30);
    multset.insert(60);
    multset.insert(60);
    std::map<int, float> map = { {5, 3.14}, {10, 6.23556}, {8, 1.2355}, {8, 1.2355}, {9, 1.23525}, {11, 1.235555}};
    std::multimap<int, float> mmmap = { {5, 3.14}, {5, 6.23556}, {8, 1.2355}, {8, 1.2355}, {9, 1.23525}, {0, 1.6}};
    
    std::unordered_set<int> uset;
    uset.insert(1);
    uset.insert(2);
    uset.insert(3);
    uset.insert(4);
    std::unordered_multiset<int > umultset;
    umultset.insert(40);
    umultset.insert(30);
    umultset.insert(60);
    umultset.insert(60);

    std::unordered_map<int, float> umap = { {5, 3.14}, {10, 6.23556}, {8, 1.2355}, {8, 1.2355}, {9, 1.23525}, {11, 1.235555}};
    std::unordered_multimap<int, float> ummmap = { {5, 3.14}, {5, 6.23556}, {8, 1.2355}, {8, 1.2355}, {9, 1.23525}, {0, 1.6}};

    return 0;
}