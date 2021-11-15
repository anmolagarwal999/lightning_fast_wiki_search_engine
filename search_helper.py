import os
import sys
from preprocess_helper import PreprocessHandlerClass
import nltk
import json 
from nltk.stem.snowball import SnowballStemmer
  
# Init class object
curr_preproc_obj=PreprocessHandlerClass()

EXTRA_DELIMITERS=[","]
CATEGORY_ALPHABETS=['t','i','b','c','l','r']
DEFAULT_SECTIONS_NEEDED=set(CATEGORY_ALPHABETS)    
WORD_SECTION_MAPPING=dict()
#--------------------------------------------
snow_stemmer = SnowballStemmer(language='english')
# def fetch_stemmed_version(curr_word):
#     return snow_stemmer.stem(curr_word)
#######################################
def is_field_query(query_str):
    if query_str.count(":")!=0:
        return True
    return False
#######################################
def add_category_to_word(curr_word, cat_arr):
    if curr_word not in WORD_SECTION_MAPPING:
        WORD_SECTION_MAPPING[curr_word]=set()
    for curr_cat in cat_arr:
        WORD_SECTION_MAPPING[curr_word].add(curr_cat)
#######################################

def fetch_word_section_mapping(QUERY_SENT):
    QUERY_STR=QUERY_SENT

    ORIGINAL_TERMS=set()
    #####################################################
    # Process field query to remove REDUNDANT PUNCTUATION
    MOD_QUERY=""
    for ch in QUERY_STR:
        if ch not in EXTRA_DELIMITERS:
            MOD_QUERY+=ch
        else:
            MOD_QUERY+=" "

    QUERY_STR=MOD_QUERY

    # Convert to LOWER CASE
    QUERY_STR=QUERY_STR.lower()
    ###########################

    # Title, Infobox, Body, Category, Links and References
    # T I B C L R
    #####################################################
    global WORD_SECTION_MAPPING
    WORD_SECTION_MAPPING=dict()


    '''
    CHOICE 1: Simple split by space
    CHOICE 2: Proper Word split
    '''

    current_category=None
 

    # Split by default whitespace
    space_separated_tokens=QUERY_STR.split()

    actual_words=[]
    for curr_space_token in space_separated_tokens:

        curr_word=curr_space_token[:]
        if is_field_query(curr_space_token):
            # So, divide this into CATEGORY and ACTUAL STRING
            curr_bin=""
            actual_word=""

            #Update current category
            found_it=False
            for curr_ch in curr_space_token:

                if found_it:
                    actual_word+=curr_ch
                else:
                    if curr_ch==':':
                        found_it=True
                        continue
                    else:
                        curr_bin+=curr_ch
            if len(curr_bin)==1 and curr_bin in CATEGORY_ALPHABETS:
                current_category=curr_bin
            curr_word=actual_word
    
    #############################
        if curr_word=="":
            continue
        # Get rid of hyphens etc and store DO NOT WASTE EFFORT ON STOPWORDS
        org_words_list=curr_preproc_obj.tokenize_text(curr_word)
        for valid_word in org_words_list:
            if curr_preproc_obj.is_in_stopwords_list(valid_word):
                continue
            if current_category is None:
                add_category_to_word(snow_stemmer.stem(valid_word), CATEGORY_ALPHABETS)
            else:
                # Some category has been identified
                add_category_to_word(snow_stemmer.stem(valid_word),[current_category] )
    #the stemmer requires a language parameter

    return WORD_SECTION_MAPPING
