# Lightning Fast Wiki Search
- Anmol Agarwal, 2019101068

## Description
This is a Wikipedia indexer and search engine, that uses the merge-sort algorithm to **create and store an inverted index** from a Wikipedia XML dump (tested on the recently released **85GB dump** of Wikipedia). 
The search engine supports two kinds of queries - normal queries and field queries  Articles are ranked based on their **term-frequency/inverse-document-frequency scores, weighted by the fields**.

Fields supported for field queries are:
- Title (`t`)
- Infobox (`i`)
- Body (`b`)
- Categories (`c`)
- External Links (`l`)
- References (`r`)

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

## Directory structure and running the code
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

### Performance sample
Number of queries being asked is  10
Query to be answered:= `jaws blockbuster thriller shark`

49549 -> Jaws (film)
3208654 -> Jaws (novel)
682845 -> Jaws 3-D
325702 -> Jaws: The Revenge
5232167 -> Shark Jaws
224654 -> Jaws 2
9592054 -> Ghost Shark 2: Urban Jaws
6262926 -> Jaws (franchise)
909824 -> Peter Benchley
19203528 -> House Shark

T:  0.490723
##########################################################
Query to be answered:= `b:dystopian george orwell nazi propaganda c:british political novels censored books`

7617654 -> Nineteen Eighty-Four
111 -> Animal Farm
7486 -> George Orwell
24155 -> Brave New World
12716 -> Mein Kampf
32936 -> Down and Out in Paris and London
374878 -> Darkness at Noon
245 -> A Clockwork Orange (novel)
225552 -> Burmese Days
141133 -> It Can't Happen Here

T:  7.892481
##########################################################
Query to be answered:= `i:Harper Lee United States 281 r:Virginia`

16827 -> Robert E. Lee
137558 -> Harper Lee
35248 -> Harpers Ferry, West Virginia
48625 -> To Kill a Mockingbird
50994 -> John Brown (abolitionist)
1195779 -> Arlington House, The Robert E. Lee Memorial
32374 -> Battle of Fredericksburg
1382377 -> Harper v. Virginia State Board of Elections
252008 -> Henry Lee III
178023 -> Washington and Lee University

T:  7.541198
##########################################################
Query to be answered:= `t:neural b:NST deep neural networks manipulate image stylization artistic style r:visual recognition c:algorithms`

18755622 -> Neural Style Transfer
8996046 -> Types of artificial neural networks
13983 -> Artificial neural network
12854015 -> Convolutional neural network
10384172 -> Deep learning
14849617 -> DeepDream
937860 -> Recurrent neural network
948579 -> Neural network
19264938 -> History of artificial neural networks
1310365 -> Cellular neural network

T:  6.465407
##########################################################
Query to be answered:= `t:hidden b:Markov process drawing balls weather guessing inference speech recognition time series r:maximum likelihood l:revealing introduction c:bioinformatics`

66159 -> Hidden Markov model
493781 -> Baum–Welch algorithm
40821 -> Markov chain
2877601 -> Bayesian inference in phylogeny
103619 -> Maximum likelihood estimation
32818 -> Bayesian inference
128979 -> Kalman filter
4151536 -> Approximate Bayesian computation
12229394 -> List of RNA-Seq bioinformatics tools
30038 -> Likelihood function

T:  17.746295
##########################################################
Query to be answered:= `Tony Appleton`

17910662 -> Tony Appleton
110812 -> Appleton, Wisconsin
3110593 -> John Appleton
13591865 -> James Appleton
2252680 -> D. Appleton & Company
1368122 -> Thomas Gold Appleton
1368120 -> Nathan Appleton
2146657 -> Daniel Appleton
18255878 -> Mount Appleton
3593847 -> Samuel Appleton (merchant)

T:  1.147892
##########################################################
Query to be answered:= `t:messi b:argentina barcelona most career goals i:forward l:FIFA c:2020 World Cup players olympic medalists`

1150110 -> Lionel Messi
322859 -> Ronaldinho
5205168 -> Neymar
377311 -> Cristiano Ronaldo
1681864 -> Sergio Agüero
3104330 -> Luis Suárez
6832681 -> Alex Morgan
8473459 -> Johan Cruyff
689161 -> Javier Mascherano
1719116 -> Dani Alves

T:  14.230851
##########################################################
Query to be answered:= `t:star i:Bradley Cooper Lady Gaga 1954 1976 136 b:country rock SHALLOW suicide by hanging Sam Elliott r:remake c:warner l:rotten tomatoes`

14513705 -> A Star Is Born (2018 film)
18325384 -> Shallow (Lady Gaga and Bradley Cooper song)
5948153 -> Lady Gaga
18410539 -> List of accolades received by A Star Is Born (2018 film)
18066061 -> A Star Is Born (2018 soundtrack)
18442668 -> Maybe It's Time
18358404 -> I'll Never Love Again
1697385 -> A Star Is Born (1976 film)
18305471 -> Always Remember Us This Way
12567402 -> American Sniper

T:  10.880973
##########################################################
Query to be answered:= `i:740 feet December 1903 silent the great train c:american silent new jersey train robbery`

48904 -> The Great Train Robbery (1903 film)
112636 -> Great Train Robbery (1963)
13079376 -> The Great Train Robbery (2013 TV series)
3403524 -> The Great K & A Train Robbery
89010 -> New Brunswick, New Jersey
12244572 -> The Great Train Robbery (1941 film)
269641 -> Ronnie Biggs
68621 -> Camden, New Jersey
88613 -> Fair Lawn, New Jersey
1992940 -> New Brunswick station

T:  12.645168
##########################################################
Query to be answered:= `Hitchcock smith 1941 charles halton 743000 adaptations normal krasna`
872282 -> Mr. & Mrs. Smith (1941 film)
227 -> Alfred Hitchcock
2129498 -> Norman Krasna
13105397 -> The Man with Blond Hair
49669 -> Suspicion (1941 film)
3011247 -> Thomas Hitchcock Sr.
15574 -> Psycho (1960 film)
167651 -> Alfred Hitchcock Presents
1805375 -> The 39 Steps (1935 film)
782115 -> The Devil and Miss Jones

T:  6.592251
##########################################################

