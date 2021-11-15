#include <bits/stdc++.h>
using namespace std;
typedef long long LL;
// const LL MOD = 998244353;
#define pb push_back
#define all(c) (c).begin(), (c).end()
#define debug(x) cout << #x << " : " << x << endl
#define part cout << "----------------------------------\n";
#include <iostream>
using namespace std::chrono;

#define fastinput                     \
    ios_base::sync_with_stdio(false); \
    cin.tie(NULL);                    \
    cout.tie(NULL);

size_t buffer_size = 1 << 20;
char *buffer = new char[buffer_size];

std::ofstream logging_file("../mounted_dump/log_rev.txt");
std::ofstream out_file;

const int DOC_CHUNK_THRESHOLD = 260000/5;

//docs which have been processed so far
int curr_docs_done = 0;

//bytes read so far
LL tot = 0;

//pattern
const string pattern = "</page>";
const int len_pat = pattern.length();

//doc number being processed
int curr_file_id = 1;

//////////////////////////////
std::chrono::steady_clock::time_point begin_time, end_time;
// std::chrono::steady_clock::time_point end ;
//////////////////////////////////////////

//text in curr chunk
string curr_chunk_text = "";
// if val=i, then i characters of pattern has been matched so far
int matched_so_far = 0;
const LL MASTER_SZ = 84602863258;
// ///////////////////////////////////
string get_str_version(int n)
{
    string ans = "";
    int tmp = n;
    while (tmp)
    {
        int d = tmp % 10;
        tmp /= 10;
        ans += (d + '0');
    }
    reverse(all(ans));
    // debug(ans);
    // exit(0);
    return ans;
}

void process_chunk(LL n)
{
    int i, j, k, t, temp;

    //more number of bytes read so far
    tot += n;

    //empty chunk
    curr_chunk_text = "";

    //go through read text
    for (i = 0; i < n; i++)
    {
        //add character to chunk
        curr_chunk_text += buffer[i];

        //invariant: not all have been matched so far
        if (pattern[matched_so_far] == buffer[i])
        {
            matched_so_far++;

            if (matched_so_far == len_pat)
            {
                matched_so_far = 0;

                //end of a page
                curr_docs_done++;

                if (curr_docs_done % DOC_CHUNK_THRESHOLD == 0)
                {
                    //write string so far
                    out_file << curr_chunk_text;
                    curr_chunk_text = "";

                    out_file.close();

                    curr_file_id++;
                    string output_file_name = "../mounted_dump/rev_segregated_outputs/part_" + get_str_version(curr_file_id);
                    out_file.open(output_file_name);
                    assert(curr_file_id < 800);
                }
            }
        }
        else
        {
            matched_so_far = 0;
            if (pattern[matched_so_far] == buffer[i])
            {
                matched_so_far++;
            }
        }
    }

    //write string taken in so far
    double done_yet = ((double)(tot) / MASTER_SZ);
    logging_file << "by:" << tot << "|";
    logging_file << "doc:" << curr_docs_done << "|";
    logging_file << "fd:" << curr_file_id << "|";
    logging_file << "com:" << done_yet << "|";
    end_time = std::chrono::steady_clock::now();

    logging_file<< "dt:" << std::chrono::duration_cast<std::chrono::seconds>(end_time - begin_time).count() << "[s]" << "\n";
    out_file << curr_chunk_text;
}
void read_file()
{

    std::ifstream fin("../mounted_dump/data");
    // std::ifstream fin("data_phase_1");

    // cout << "usual stuff success" << endl;
    // exit(0);
    while (fin)
    {
        // Try to read next chunk of data
        fin.read(buffer, buffer_size);
        // Get the number of bytes actually read
        size_t count = fin.gcount();
        // If nothing has been read, break
        if (!count)
            break;
        // Do whatever you need with first count bytes in the buffer
        process_chunk(count);
    }
}
int main()
{
    fastinput;
    LL n, i, j, k, t, temp, tc;
    //https://stackoverflow.com/q/2808398
    string output_file_name = "../mounted_dump/rev_segregated_outputs/part_" + get_str_version(curr_file_id);
    out_file.open(output_file_name);
    begin_time = std::chrono::steady_clock::now();
    read_file();
    // auto start = high_resolution_clock::now();

    end_time = std::chrono::steady_clock::now();

    std::cout << "FINAL Time difference = " << std::chrono::duration_cast<std::chrono::seconds>(end_time - begin_time).count() << "[s]" << std::endl;
    // std::cout << "Time difference = " << std::chrono::duration_cast<std::chrono::nanoseconds>(end - begin).count() << "[ns]" << std::endl;

    // debug(tot);
    return 0;
}
