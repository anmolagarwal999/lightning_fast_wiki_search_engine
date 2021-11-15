#include "master_header.h"
#include <bits/stdc++.h>
using namespace std;

bool fetch_new_line(ifstream *&fd,string &line)
{
    //check if open
    assert(fd->is_open());
    // cout << "is open" << endl;
    // Each extracted character is appended to the string as if its member push_back was called.
    line = "";
    if (getline(*fd, line))
    {
        // debug(line);
        return true;
    }
    return false;
}

ifstream *fetch_new_fd(string path)
{
    auto file = new std::ifstream(path);
    return file;
}
