#include "master_header.h"

////////////////

#define fastinput                     \
    ios_base::sync_with_stdio(false); \
    cin.tie(NULL);                    \
    cout.tie(NULL);
//////////////////////////////
vector<ifstream *> fds;
vector<string> file_paths;
//------------------
const int lb = 1;
const int ub = 412;
//------------------
LL tot_tokens_cnt = 0;
vector<string> curr_fd_line;

unordered_set<string> casual_stopwords;

bool is_worthy_token(const string &token)
{
    //remove 1 letter alphabets
    if (casual_stopwords.find(token) != casual_stopwords.end())
    {
        return false;
    }

    if (token.length() == 1)
    {
        // char ch = token[0];
        // if (!(ch >= '0' && ch <= '9'))
        // {
        //     return false;
        // }
        return false;
    }
    // else if (token.length() == 2)
    else if (true)
    {
        if (token[0] == '0')
        {
            return false;
        }
    }
    return true;
}
const LL FILE_LIMIT = 7 * 1000 * 1000;
// const LL FILE_LIMIT = 60;
LL output_file_id = 0;
LL output_file_sz = 0;
/////////////////////////////////////////
void find_all_file_paths()
{

    for (int i = lb; i <= ub; i++)
    {
        string curr_path = "../../mounted_dump/processed_output/inverted_indexes/index_" + to_string(i) + ".txt";
        // string curr_path = "./tests/input/" + to_string(i) + ".txt";
        file_paths.pb(curr_path);
        debug(curr_path);
    }
}

string fetch_token(const string &curr_line)
{
    string ans = "";
    for (auto &x : curr_line)
    {
        if (x == '=')
        {
            return ans;
        }
        ans += x;
    }
    return ans;
}

void append_docs_list(string &s_final, const string &curr_line)
{
    LL eq_pos = -1;
    LL line_len = curr_line.length();
    for (LL i = 0; i < line_len; i++)
    {
        if (curr_line[i] == '=')
        {
            eq_pos = i;
            break;
        }
    }

    assert(eq_pos != -1);
    for (LL i = eq_pos + 1; i < line_len; i++)
    {
        s_final += curr_line[i];
    }
}

string get_output_file_address()
{
    const string ans = "../../mounted_dump/final_merged_output/fin_inverted_indexes/out_" + to_string(output_file_id) + ".txt";
    // const string ans = "./tests/output/" + to_string(output_file_id) + ".txt";
    return ans;
}

void parse_files()
{
    LL n, i, j, k, t, temp;

    int num_files = fds.size();
    n = num_files;
    curr_fd_line.resize(n);
    debug(num_files);
    ///////////////
    ofstream output_fd;
    output_fd.open(get_output_file_address());
    ofstream token_placement_details("../../mounted_dump/final_merged_output/fin_placement_details.txt");
    ////////////
    string first_token = "";
    /////////////////////////////

    set<int> files_left;
    for (i = 0; i < num_files; i++)
    {
        files_left.insert(i);
    }

    set<string> words_in_contention;
    vector<string> rep_word(num_files, "");

    auto update_file_details = [&](int file_idx)
    {
        // debug(file_idx);
        assert(fds[file_idx]->is_open());
        bool stat;
        stat = fetch_new_line(fds[file_idx], curr_fd_line[file_idx]);
        if (!stat)
        {
            //file is empty it seems :(
            cout << "file at index " << file_idx << " needs to be closed" << endl;
            fds[file_idx]->close();
            files_left.erase(file_idx);
        }
        else
        {
            string curr_token = fetch_token(curr_fd_line[file_idx]);
            rep_word[file_idx] = curr_token;
            words_in_contention.insert(curr_token);
        }
    };

    /////////////////////////////
    //sanity check to close files if they are empty
    for (i = 0; i < num_files; i++)
    {
        update_file_details(i);
    }

    debug(files_left.size());
    queue<int> files_to_update;
    /////////////////////////
    while (!files_left.empty())
    {
        //atleast some file is there
        string curr_postings_list = "";
        assert(!words_in_contention.empty());
        string lucky_str = *(words_in_contention.begin());
        if (first_token == "")
        {
            first_token = lucky_str;
            token_placement_details << output_file_id << " : " << lucky_str << endl;
        }
        string doc_list = "";
        //find all files which need to be updated
        for (auto &x : files_left)
        {
            i = x;
            assert(rep_word[x] >= lucky_str);
            if (rep_word[x] == lucky_str)
            {
                files_to_update.push(x);
                if (doc_list != "")
                {
                    //pipe needs to be added
                    doc_list += '|';
                }

                //
                append_docs_list(doc_list, curr_fd_line[x]);

                //we need to update this doc
            }
        }

        if (is_worthy_token(lucky_str))
        {
            tot_tokens_cnt++;

            output_fd << lucky_str << "=" << doc_list << endl;
            output_file_sz += 2 + lucky_str.length() + doc_list.length();
        }
        if (output_file_sz > FILE_LIMIT)
        {
            debug(output_file_id);
            debug(lucky_str);
            output_file_sz = 0;
            output_file_id++;
            output_fd.close();
            output_fd.clear();
            first_token = "";
            output_fd.open(get_output_file_address());
        }
        // debug(files_to_update.size());
        // debug(doc_list);
        // part;

        words_in_contention.erase(lucky_str);

        while (!files_to_update.empty())
        {
            int file_id = files_to_update.front();
            files_to_update.pop();
            update_file_details(file_id);
        }
    }
    assert(words_in_contention.empty());
}
int main()
{
    fastinput;
    LL n, i, j, k, t, temp;
    // freopen("stopwords_prevent_merge.txt", "r", stdout);
    auto fd_now = fetch_new_fd("stopwords_prevent_merge.txt");
    string current_stopword = "";
    while (true)
    {
        current_stopword = "";
        bool stat = fetch_new_line(fd_now, current_stopword);
        if (!stat)
        {
            break;
        }
        casual_stopwords.insert(current_stopword);
    }
    cout << "Number of stopwords is " << casual_stopwords.size() << endl;
    for (auto &x : casual_stopwords)
    {
        cout << x << endl;
    }
    part;
    // exit(0);
    //fill file paths
    find_all_file_paths();

    //initialize file descriptors
    for (auto &x : file_paths)
    {
        auto fd_now = fetch_new_fd(x);
        fds.pb(fd_now);
        assert(fd_now->is_open());
    }

    parse_files();
    debug(tot_tokens_cnt);

    //each line is the form
    //<str>=docid<s><cnt><s><cnt>|

    //put words in heap
    //list just needs to be combined
    //but since sorted by docIDs, just direct combination would work as well
    //extract string and then <>|<>|<> type thing

    //if file is open, parse a line from it
    //keep a string mapping from file to string
    //read a word from it, put in the set and map the file to that words
    //iterate through all files, see which file has the lowest word and insert docIDs accordingly

    //for now, doing it for even just file is sufficient, but space to break files would also be needed in the futures

    return 0;
}
