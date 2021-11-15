# Lightning Fast Wiki Search
- Anmol Agarwal, 2019101068

## Description
This is a basic tool built on recent dump of Wikipedia pages **(85GB)**. The search engine supports two kinds of queries - normal queries and field queries
### Requirements
* `nltk` is the only non-standard library being used by my code

#### To run code
* Install dependcies using the requirements.txt which has been given
* Please put relevant paths in `config.py`

### File structure
*  `stint_master.py`: main code (parser, filtering, index creation)
*  `preprocess_handler.py`: common code used for stemming and stopword removal for both index creation and query answering
*  `search_master.py`: parses user query and outputs apt search results
*  `search_helper.py`: helps to parse the query and clasify tokens to the different zones
*  folder `merge` contains `merge.cpp` and `utils.cpp` alongwith some sample tests: code written in `c++` to merge the inverted indexes of the 412 separate files. Code written in c++ (due to faster execution time)
*  `run.sh` : used to feed one of the 412 files to `stint_master.py` at different durations over the past week


## Implementation details
* I first **divided the entire 85 GB data into 412 files**. Implementation was based on a balanced bracket logic based on the <page> </page> tags. This was done in `c++` and code can be found in `parse_2.cpp`
* Then, I wrote a bash script `run.sh` which sent some range of these 412 files to be processed by `stint_master.py`
* The output of `stint_master.py` were 412 inverted index files which had sorted keys within themselves individually
* Addtionally, a track of which doc_id corresponded to which title was also kept.
* I had to do a **412-way merge sort** to combine these files to form a common inverted index. While combining, I also broke the combined index into serveral parts (approx 1500 parts).

## Some assumptions and other implementation details
* Queries in which multiple tokens are separated by spaces are enclosed within double quotes before being sent to `search.sh`
* `:` as a character only occurs in field queries. I needed this to deduce whether the query is a simple query or a field query
* A `:` is always preceeded by a valid category representing character ie one of [t,i,b,c,l,r]



## Indexing Technique 

*  **Parsing and Chunkwise blocking:** : The SAX XML parser has been used to parse the XML files containing the wiki dump. For every 52000 documents, a new file is used to store the corresponding index.
* **Splitting content of each page in Zones**: using regex and balanced bracket techniques
*  **Text Processing**: tokenizing, stopwords removal, stemming, url removal etc
*  **Merging the 412 index files**: A pointer to the beginning of each index file was maintained and postings list was combined if the pointer to 2 different files pointed to the same key. The lexicographically smallest word which was being pointed by any one of the 412 pointers was considered active and pointers were incremented accordingly.
*  **Splitting merged index alphabetically**: Splitting the master index file into several parts to reduce search time

### Format of postings list
<term>=<doc_id><zone_1><f1><zone_2><f2>...<zone_n><fn>|<DOC DETAILS>|<DOC DETAILS>|.....

## Searching and Ranking mechanism
* **tf-idf** is used (with sublinear tf-scaling)
* Different weightage are assigned to the frequency of a word in different zones 
* Eg. Title,infobox having a higher weightage than body 
* If the query requires a `word` to belong in a zone `z`, then corresponding score for that zone is scaled by `BONUS_FREQ_DESERVED`



