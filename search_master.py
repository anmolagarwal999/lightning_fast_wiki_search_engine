import os
import sys
from preprocess_helper import PreprocessHandlerClass
# import nltk
import math
import heapq
import linecache as lc
import re
from datetime import datetime
# import json
# from nltk.stem.snowball import SnowballStemmer
from search_helper import *
import config as conf


##################################################
######   BINARY SEARCH OVER INDEX TERMS  ###################
STARTING_TERMS=[]
with open(conf.PATH_TO_FILE_WITH_INV_INDEX_STARTING_TERMS,'r') as fd:
    lines_arr=fd.readlines()
    for curr_line in lines_arr:
        word_name=curr_line.split(" ")[-1].rstrip()
        STARTING_TERMS.append(word_name)
# print(*STARTING_TERMS)
NUM_INDEX_FILES=len(STARTING_TERMS)
print("Total files is ", NUM_INDEX_FILES)
# print("Metadata for index files read for bin search")
doc_info_list=[]
#####################################################
# Have a word which is taken as input
# '''NOTE THAN BINARY SEARCH just returns file where WORD may probably be present, it does not ENSURE that word will be present'''
def fetch_exp_file(curr_word):
    lb=0
    ub=NUM_INDEX_FILES-1
    pos=-1
    while(lb<=ub):
        mid=(lb+ub)//2
        # print("term comp is ", STARTING_TERMS[mid])
        if STARTING_TERMS[mid]<=curr_word:
            # print("LESSER")
            pos=mid
            lb=mid+1
        else:
            ub=mid-1
    # assert(pos!=-1)
    return pos

##################################
global_postings_list=""
######################################
def fetch_doc_details_list():
    global global_postings_list
    if global_postings_list=="":
        return []
    global doc_info_list
    docs_str_list=global_postings_list.split("|")
    doc_info_list=[]
    for curr_doc_details in docs_str_list:
        len_tokens=0
        tokens_list=[]
        prev_is_num=True
        curr_token=""
        for ch in curr_doc_details:
            if ch>='0' and ch<='9':
                if prev_is_num:
                    curr_token+=ch
                else:
                    tokens_list.append(curr_token)
                    len_tokens+=1
                    curr_token=ch
                    prev_is_num=True
            else:
                if not prev_is_num:
                    curr_token+=ch
                else:
                    tokens_list.append(curr_token)
                    len_tokens+=1
                    curr_token=ch
                    prev_is_num=False
        if curr_token!="":
            tokens_list.append(curr_token)
            len_tokens+=1
        # print(tokens_list)
        # print(len_tokens)
        # sys.exit()
        score_dict=dict()
        # len_tokens=len(tokens_list)
        for i in range(2, len_tokens,2):
            score_dict[tokens_list[i-1]]=int(tokens_list[i])

        doc_info_list.append((int(tokens_list[0]),score_dict))
        # print("-----------------")
    # return doc_info_list
######################################

def fetch_posting_data(file_id, curr_word):
    global global_postings_list
    global_postings_list=""
    # word_len=len(curr_word)
    # print("curr word is ", curr_word)
    with open(conf.PATH_TO_DIR_WITH_INV_INDEXES+"/out_"+str(file_id)+".txt",'r') as infile:
        for line in infile.readlines():
            # print("line is ", line)
            # sys.exit()
            colon_idx=line.find('=')
            line_key=line[:colon_idx]
            if colon_idx==-1:
                continue
            # print("line key is ", line_key)
            if line_key<=curr_word:
                if line_key==curr_word:
                    # return line[colon_idx+1:].rstrip("\n")
                    global_postings_list= line[colon_idx+1:].rstrip("\n")
                    return
            else:
                return
        return

#############################################################################################


#############################################################
# THRESHOLD_VAL=52000*4
THRESHOLD_VAL=52000//2
def fetch_title(curr_doc_id):
    outfile_id=int(math.ceil(curr_doc_id/THRESHOLD_VAL))
    # print("smuggle doc id is ", curr_doc_id)
    # print("outfile id type is ", type(outfile_id))
    offset=curr_doc_id%THRESHOLD_VAL
    if offset==0:
        offset+=THRESHOLD_VAL
    PATH_OF_SEEKED_FILE=conf.PATH_TO_FILE_WITH_TITLES+f"/fin_titles/out_title_{outfile_id}.txt"
    seeked_title=lc.getline(PATH_OF_SEEKED_FILE, offset)
    return seeked_title

#############################################################
# BONUS_CONST=30
# def fetch_doc_term_weighted_freq(zones_of_words, doc_dict):
#     # find list of common keys
#     common_zones=zones_of_words.intersection(set(doc_dict.keys()))
#     if len(common_zones)==0:
#         return 0,0

#     # 100 weightage to the ACTUALLY WANTED KEYS AS WELL
#     DEFAULT_SCORE=0
#     freq_in_doc=0
#     for key, val in doc_dict.items():
#         DEFAULT_SCORE+=SCORE_COEFF[key]*val
#         freq_in_doc+=val

#     BONUS_SCORE=0
#     for curr_zone in common_zones:
#         BONUS_SCORE+=BONUS_CONST * SCORE_COEFF[curr_zone] * doc_dict[curr_zone]
#     return DEFAULT_SCORE+BONUS_SCORE, freq_in_doc
#//////////////////////////////////////////////////////////


# NON_BONUS_DESERVED=0.1
EXP_NUMBER_OF_RELEVANT_RESULTS=10
TOT_NUMBER_OF_DOCS_IN_CORPUS=21384756
MASTER_LOG=math.log(TOT_NUMBER_OF_DOCS_IN_CORPUS,10)


with open(conf.PATH_TO_QUERY_TESTER, 'r') as query_fd:
    queries_str_list=query_fd.readlines()
    sys.stdout=open(conf.PATH_TO_QUERY_ANSWERING,'w')
    print("Number of queries being asked is ",len(queries_str_list))

    ############  PROCESS EACH QUERY ####################################
    for curr_query_str in queries_str_list:
        LB_TIME=datetime.now()
        # print("Curr query is ", curr_query_str)
        # print("------------")
        WORD_SEC_DICT=fetch_word_section_mapping(curr_query_str)

        # print(WORD_SEC_DICT)

        QUERY_SCORE_FOR_DOC=dict()
        sz=0
        ###############################################################
        # go through all the words
        # global doc_info_list
        for curr_term, expected_categories in WORD_SEC_DICT.items():
            term_file_id=fetch_exp_file(curr_term)
            # print("curr term is ", curr_term)
            # print("term file id is ", term_file_id)
            fetch_posting_data(term_file_id, curr_term)
            fetch_doc_details_list()
            # print(doc_info_list)
            # NUM_DOCS_WHERE_TERM_APPEARS=len(doc_info_list)
            # # print("Num docs is ", NUM_DOCS_WHERE_TERM_APPEARS)
            # if NUM_DOCS_WHERE_TERM_APPEARS==0:
            #     continue
            TERM_SCORE_DOC=[]
            DOC_ZONE_FREQ=[0,0,0,0,0,0]

            for curr_doc in doc_info_list:
                the_doc_id=curr_doc[0]
                doc_score_for_term=[0,0,0,0,0,0]
                for zone_in_doc , zone_f in curr_doc[1].items():
                    zone_id=conf.ZONE_INDEXES[zone_in_doc]
                    DOC_ZONE_FREQ[zone_id]+=1
                    doc_score_for_term[zone_id]+=conf.ZONE_COEFF[zone_in_doc]*zone_f
                TERM_SCORE_DOC.append(doc_score_for_term[:])

            i=-1
            for curr_doc in doc_info_list:
                the_doc_id=curr_doc[0]
                i+=1
                for zone_in_doc in curr_doc[1].keys():
                    num=TERM_SCORE_DOC[i][conf.ZONE_INDEXES[zone_in_doc]]
                    if num==0:
                        continue
                    if zone_in_doc in expected_categories:
                        num*=conf.BONUS_FREQ_DESERVED
                    tf=1+math.log(num, 10)
                    idf=MASTER_LOG-math.log(DOC_ZONE_FREQ[conf.ZONE_INDEXES[zone_in_doc]],10)
                    add=tf*idf
                    if zone_in_doc in expected_categories:
                        add*=conf.BONUS_OUTSIDE_FREQ_DESERVED
                    if the_doc_id in QUERY_SCORE_FOR_DOC:
                        QUERY_SCORE_FOR_DOC[the_doc_id]+=add
                    else:
                        QUERY_SCORE_FOR_DOC[the_doc_id]=add
                        sz+=1

        ###################################################################



        # scores_docs_list=[]
        # for doc_id, doc_score in SCORE_FOR_DOC.iteritems():
        #     scores_docs_list.append((doc_score, doc_id))
        # print("Total docs obtained is ", sz)
        # print(DOC_ZONE_FREQ)
        obtained=min(sz, EXP_NUMBER_OF_RELEVANT_RESULTS)
        rem=EXP_NUMBER_OF_RELEVANT_RESULTS-obtained
        winners_list=heapq.nlargest(obtained,QUERY_SCORE_FOR_DOC.items(), key=lambda e:e[1]) # Gives [ ("c++", 50), ("python", 30) ]
        # print(winners_list)
        # break
        # print("\n\n")
        titles_of_winners=[]
        winner_ids=[]
        for curr_winner_doc_id in winners_list:
            if rem!=0:
                winner_ids.append(curr_winner_doc_id[0])
            winner_title=fetch_title(curr_winner_doc_id[0])
            # titles_of_winners.append(str(curr_winner_doc_id)+" , "+winner_title)
            titles_of_winners.append(winner_title)
        curr_try=1
        while rem>0:
            if curr_try not in winner_ids:
                rem-=1
                titles_of_winners.append(fetch_title(curr_try))
            curr_try+=1



        UB_TIME=datetime.now()
        diff=UB_TIME-LB_TIME
        print(*titles_of_winners,sep='')

        print("T: ", diff.total_seconds())

        print("")
