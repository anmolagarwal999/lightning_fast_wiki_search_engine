#ifndef UTILS
#define UTILS

bool fetch_new_line(ifstream *&fd,string &line);

ifstream * fetch_new_fd(string path);
#endif