# Lightning Fast Wiki Search
- Anmol Agarwal

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

* 9549 -> Jaws (film)
* 208654 -> Jaws (novel)
* 82845 -> Jaws 3-D
* 25702 -> Jaws: The Revenge
* 232167 -> Shark Jaws
* 24654 -> Jaws 2
* 592054 -> Ghost Shark 2: Urban Jaws
* 262926 -> Jaws (franchise)
* 09824 -> Peter Benchley
* 9203528 -> House Shark

T:  0.490723

##########################################################

Query to be answered:= `b:dystopian george orwell nazi propaganda c:british political novels censored books`

* 617654 -> Nineteen Eighty-Four
* 11 -> Animal Farm
* 486 -> George Orwell
* 4155 -> Brave New World
* 2716 -> Mein Kampf
* 2936 -> Down and Out in Paris and London
* 74878 -> Darkness at Noon
* 45 -> A Clockwork Orange (novel)
* 25552 -> Burmese Days
* 41133 -> It Can't Happen Here

T:  7.892481

##########################################################

Query to be answered:= `i:Harper Lee United States 281 r:Virginia`

* 6827 -> Robert E. Lee
* 37558 -> Harper Lee
* 5248 -> Harpers Ferry, West Virginia
* 8625 -> To Kill a Mockingbird
* 0994 -> John Brown (abolitionist)
* 195779 -> Arlington House, The Robert E. Lee Memorial
* 2374 -> Battle of Fredericksburg
* 382377 -> Harper v. Virginia State Board of Elections
* 52008 -> Henry Lee III
* 78023 -> Washington and Lee University

T:  7.541198

##########################################################

Query to be answered:= `t:neural b:NST deep neural networks manipulate image stylization artistic style r:visual recognition c:algorithms`

* 8755622 -> Neural Style Transfer
* 996046 -> Types of artificial neural networks
* 3983 -> Artificial neural network
* 2854015 -> Convolutional neural network
* 0384172 -> Deep learning
* 4849617 -> DeepDream
* 37860 -> Recurrent neural network
* 48579 -> Neural network
* 9264938 -> History of artificial neural networks
* 310365 -> Cellular neural network

T:  6.465407

##########################################################

Query to be answered:= `t:hidden b:Markov process drawing balls weather guessing inference speech recognition time series r:maximum likelihood l:revealing introduction c:bioinformatics`

* 6159 -> Hidden Markov model
* 93781 -> Baum–Welch algorithm
* 0821 -> Markov chain
* 877601 -> Bayesian inference in phylogeny
* 03619 -> Maximum likelihood estimation
* 2818 -> Bayesian inference
* 28979 -> Kalman filter
* 151536 -> Approximate Bayesian computation
* 2229394 -> List of RNA-Seq bioinformatics tools
* 0038 -> Likelihood function

T:  17.746295

##########################################################

Query to be answered:= `Tony Appleton`

* 7910662 -> Tony Appleton
* 10812 -> Appleton, Wisconsin
* 110593 -> John Appleton
* 3591865 -> James Appleton
* 252680 -> D. Appleton & Company
* 368122 -> Thomas Gold Appleton
* 368120 -> Nathan Appleton
* 146657 -> Daniel Appleton
* 8255878 -> Mount Appleton
* 593847 -> Samuel Appleton (merchant)

T:  1.147892

##########################################################

Query to be answered:= `t:messi b:argentina barcelona most career goals i:forward l:FIFA c:2020 World Cup players olympic medalists`

* 150110 -> Lionel Messi
* 22859 -> Ronaldinho
* 205168 -> Neymar
* 77311 -> Cristiano Ronaldo
* 681864 -> Sergio Agüero
* 104330 -> Luis Suárez
* 832681 -> Alex Morgan
* 473459 -> Johan Cruyff
* 89161 -> Javier Mascherano
* 719116 -> Dani Alves

T:  14.230851

##########################################################

Query to be answered:= `t:star i:Bradley Cooper Lady Gaga 1954 1976 136 b:country rock SHALLOW suicide by hanging Sam Elliott r:remake c:warner l:rotten tomatoes`

* 4513705 -> A Star Is Born (2018 film)
* 8325384 -> Shallow (Lady Gaga and Bradley Cooper song)
* 948153 -> Lady Gaga
* 8410539 -> List of accolades received by A Star Is Born (2018 film)
* 8066061 -> A Star Is Born (2018 soundtrack)
* 8442668 -> Maybe It's Time
* 8358404 -> I'll Never Love Again
* 697385 -> A Star Is Born (1976 film)
* 8305471 -> Always Remember Us This Way
* 2567402 -> American Sniper

T:  10.880973

##########################################################

Query to be answered:= `i:740 feet December 1903 silent the great train c:american silent new jersey train robbery`

* 8904 -> The Great Train Robbery (1903 film)
* 12636 -> Great Train Robbery (1963)
* 3079376 -> The Great Train Robbery (2013 TV series)
* 403524 -> The Great K & A Train Robbery
* 9010 -> New Brunswick, New Jersey
* 2244572 -> The Great Train Robbery (1941 film)
* 69641 -> Ronnie Biggs
* 8621 -> Camden, New Jersey
* 8613 -> Fair Lawn, New Jersey
* 992940 -> New Brunswick station

T:  12.645168

##########################################################

Query to be answered:= `Hitchcock smith 1941 charles halton 743000 adaptations normal krasna`
* 72282 -> Mr. & Mrs. Smith (1941 film)
* 27 -> Alfred Hitchcock
* 129498 -> Norman Krasna
* 3105397 -> The Man with Blond Hair
* 9669 -> Suspicion (1941 film)
* 011247 -> Thomas Hitchcock Sr.
* 5574 -> Psycho (1960 film)
* 67651 -> Alfred Hitchcock Presents
* 805375 -> The 39 Steps (1935 film)
* 82115 -> The Devil and Miss Jones

T:  6.592251

##########################################################

