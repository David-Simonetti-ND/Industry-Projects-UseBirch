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
    /*
    std::array<int, 5>      iarr = {1, 2, 3, 4, 5}; iarr[0] = -1;
    std::array<char, 5>     carr = {'a', 'b', 'c', 'd', 'e'}; carr[0] = 'f';
    std::array<float, 5>    farr = {1.1, 2.2, 3.3, 4.4, 5.5}; farr[0] = 3.5;
    std::array<double, 5>   darr = {1.6, 2.7, 3.8, 4.9, 5.1}; darr[0] = 7.1;
    */

    std::forward_list<int>      isllist = {6, 7, 8, 9, 10};
    std::forward_list<char>     csllist = {'a', 'b', 'c'};
    std::forward_list<float>    fsllist = {1.1, 2.1, 3.1};
    std::forward_list<double>   dsllist = {10.1, 11.1, 12.1};

    std::list<int>      idllist = {6, 7, 8, 9, 10};
    std::list<char>     cdllist = {'a', 'b', 'c'};
    std::list<float>    fdllist = {1.1, 2.1, 3.1};
    std::list<double>   ddllist = {10.1, 11.1, 12.1};

    std::deque<int>     id = {7, 5, 16, 8};
    std::deque<char>    cd = {'a', 'b', 'c', 'd'};
    std::deque<float>   fd = {7.1, 5.2, 16.3, 8.4};
    std::deque<double>  dd = {7.8, 5.7, 16.6, 8.5};

    std::queue<int>     iq(id);
    std::queue<char>    cq(cd);
    std::queue<float>   fq(fd);
    std::queue<double>  dq(dd);

    std::priority_queue<int>    ipq; ipq.push(50); ipq.push(40); ipq.push(60); ipq.push(70);
    std::priority_queue<char>   cpq; cpq.push('a'); cpq.push('b'); cpq.push('c'); cpq.push('d');
    std::priority_queue<float>  fpq; fpq.push(50.1); fpq.push(40.2); fpq.push(60.3); fpq.push(70.4);
    std::priority_queue<double> dpq; dpq.push(50.5); dpq.push(40.6); dpq.push(60.7); dpq.push(70.8);

    std::stack<int>     is; is.push(-6); is.push(-7); is.push(-8);
    std::stack<char>    cs; cs.push('a'); cs.push('b'); cs.push('c');
    std::stack<float>   fs; fs.push(-6.1); fs.push(-7.2); fs.push(-8.3);
    std::stack<double>  ds; ds.push(-6.6); ds.push(-7.5); ds.push(-8.4);

    std::set<int>       iset; iset.insert(1); iset.insert(2); iset.insert(3);
    std::set<char>      cset; cset.insert('a'); cset.insert('b'); cset.insert('c');
    std::set<float>     fset; fset.insert(1.1); fset.insert(2.2); fset.insert(3.3);
    std::set<double>    dset; dset.insert(1.6); dset.insert(2.7); dset.insert(3.8);

    std::multiset<int, std::greater<int> > multset;
    multset.insert(40);
    multset.insert(30);
    multset.insert(60);
    multset.insert(60);
    std::map<int, float> map = { {5, 3.14}, {10, 6.23556}, {8, 1.2355}, {8, 1.2355}, {9, 1.23525}, {11, 1.235555}};
    std::multimap<int, float> mmmap = { {5, 3.14}, {5, 6.23556}, {8, 1.2355}, {8, 1.2355}, {9, 1.23525}, {0, 1.6}};
    

    return 0;
}