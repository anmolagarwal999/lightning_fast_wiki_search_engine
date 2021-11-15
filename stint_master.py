#!/usr/bin/env python
# coding: utf-8

# # Importing libraries


import os
import sys
import xml.sax
from datetime import datetime
import re
import json
import nltk
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
from preprocess_helper import PreprocessHandlerClass




BASIC_DIR_PATH="../mounted_dump/again_processed_output"
PATH_FOR_INPUT="../mounted_dump/rev_segregated_outputs"
# PATH_FOR_INPUT="../mounted_dump/check_folder"
PATH_TO_INVERTED_INDEX_DIR="../mounted_dump/again_processed_output/inverted_indexes"
INPUT_FILE_NAME=sys.argv[1]


# In[ ]:


print("input file received is ", INPUT_FILE_NAME)


# ### Init preprocess object for stopwords etc

# In[2]:


curr_preproc_obj=PreprocessHandlerClass()


# #### Metrics to measure performance

# In[3]:


begin = datetime.now()
print(begin)


# ### Init dict list

# In[4]:


dict_list=[]


# ### Most important variables 

# In[5]:


curr_text=""
curr_title=""
global_curr_doc_id=0
global_curr_wiki_page=None


# ### Write code to extract file id

# In[6]:


CURR_FILE_ID=-1
CURR_FILE_ID=int(INPUT_FILE_NAME.split("_")[1])
assert(CURR_FILE_ID!=-1)
GLOBAL_TRACKING_TITLES=""
GLOBAL_DOC_ID_OFFSET=(CURR_FILE_ID-1)*(260000//5)
print("offset is ", GLOBAL_DOC_ID_OFFSET)


# # Extract categories from text

# In[7]:


category_regex=r"\[\[category:(.*)\]\]"
category_pattern=re.compile(category_regex)
def extract_category_title(curr_text,arr):
        arr.append(curr_text.group(1))
        return ""

def get_categorical_text():
    arr=[]
    global curr_text
    curr_text=category_pattern.sub(lambda m:extract_category_title(m,arr),curr_text)
    category_str=" ".join(arr)
    return category_str


# ## Remove self contained REFS

# In[8]:


self_contained_ref_regex=r"<ref[^<]*\/>"
self_contained_ref_pattern=re.compile(self_contained_ref_regex)

def get_self_contained_refs_list():
    global curr_text
    curr_text=self_contained_ref_pattern.sub("",curr_text)
    #return data


# ## Getting paired refs

# In[9]:


paired_refs_regex=r"<ref(.*?)<\/ref>"
paired_refs_pattern=re.compile(paired_refs_regex)
def extract_paired_regs(m,arr):
        arr.append(m.group(0))
        return ""
def get_paired_refs_list():
    global curr_text
    arr=[]
    
    curr_text=paired_refs_pattern.sub(lambda m:extract_paired_regs(m,arr),curr_text)
    curr_ans=" ".join(arr)
    return  curr_ans


# ## Dealing with infobox

# In[10]:


info_substring = '{{infobox'
def extract_infobox():
    # regex is bad for this task as cannot handle BALANCED BRACKET
    global curr_text
    # Find first {{ before infobox
    # Keep counter for balanced
    
    lb_idx=curr_text.find(info_substring)
    if lb_idx==-1:
        return  ""
    assert(lb_idx!=-1)
    tot_len=len(curr_text)
    cnt=0
    ub_idx=-1

    pref_str=""
    info_str=""
    suffix_str=""

    # fill prefix
    for i in range(0, lb_idx):
        pref_str+=curr_text[i]
    
    for i in range(lb_idx,tot_len ):
        info_str+=curr_text[i]
        if curr_text[i]=='{':
            cnt+=1
        elif curr_text[i]=='}':
            cnt-=1
        if cnt==0:
            ub_idx=i
            break
        
    if ub_idx==-1:
        #print(f"{title_stuff} -> WEIRD STUFF")
        curr_text=""
        return ""
    
    for i in range(ub_idx+1, tot_len):
        suffix_str+=curr_text[i]    
    
        #print(curr_text)
    #assert(ub_idx!=-1)
    curr_text=pref_str+" "+suffix_str
    return info_str


# ### Getting external links

# In[11]:


# # Getting external links

check_substring_1 = "== external links"
check_substring_2 = "==external links"
def extract_ext_links():
    global curr_text
    idx1=-1
    idx2=-1
    lb_idx=-1
    idx_before=-1
    idx1=curr_text.rfind(check_substring_1)
    if idx1!=-1:
        lb_idx=idx1+len(check_substring_1)
        idx_before=idx1
    else:
        idx2=curr_text.rfind(check_substring_2)
        if idx2!=-1:
            lb_idx=idx2+len(check_substring_2)
            idx_before=idx2
    if idx1==-1 and idx2==-1:
        return ""
    assert(lb_idx!=-1)

    # break by newlines
    links_list=[]
    #remaining_str=""
    
    curr_list=curr_text[lb_idx:].split("\n")
    curr_text=curr_text[:idx_before]
    # redundancy
    found_end=False
    for curr_line in curr_list:
        if curr_line=="":
            found_end=True
        if found_end==False:
            links_list.append(curr_line)
        else:
            curr_text+='\n'+curr_line
    #print("Links list is ", links_list)
    curr_ans=" ".join(links_list)
    #print(curr_ans)
    return curr_ans


# ### Getting proper references

# In[12]:


check_substring_3 = "==references"
check_substring_4 = "== references"
def extract_ext_refs():
    global curr_text
    idx1=-1
    idx2=-1
    lb_idx=-1
    idx_before=-1
    idx1=curr_text.rfind(check_substring_3)
    if idx1!=-1:
        lb_idx=idx1+len(check_substring_3)
        idx_before=idx1
    else:
        idx2=curr_text.rfind(check_substring_4)
        if idx2!=-1:
            lb_idx=idx2+len(check_substring_4)
            idx_before=idx2
    if idx1==-1 and idx2==-1:
        return  ""
    assert(lb_idx!=-1)

    # break by newlines
    links_list=[]
    #remaining_str=""
    #remaining_str=curr_text[:idx_before]
    curr_list=curr_text[lb_idx:].split("\n")
    curr_text=curr_text[:idx_before]

    found_end=False
    for curr_line in curr_list:
        if curr_line=="":
            found_end=True
        if found_end==False:
            links_list.append(curr_line)
        else:
            curr_text+='\n'+curr_line
    #print("Links list is ", links_list)
    curr_ans=" ".join(links_list)
    #print(curr_ans)
    return  curr_ans


# ### Removing URLS

# In[13]:


URLS_REGEX = "((http|https)://)(www.)?" +             "[a-zA-Z0-9@:%._\\+~#?&//=]" +             "{2,256}\\.[a-z]" +             "{2,6}\\b([-a-zA-Z0-9@:%" +             "._\\+~#?&//=]*)"
#URLS_REGEX=r"(https?://\S+)"
URL_PATTERN=re.compile(URLS_REGEX)
def extract_urls(curr_text):
    curr_text=URL_PATTERN.sub("", curr_text)
    return curr_text


# ## Process the wiki page

# In[14]:


def process_wiki_page():
    global curr_title, curr_text
    # change both to lower case
    curr_title=curr_title.lower()
    curr_text=curr_text.lower()
    
    global global_curr_wiki_page
    
    ######### TITLE ######################
    global_curr_wiki_page['t']=curr_title
    
    ############ INFOBOX #########################
    # Extract infobox
    global_curr_wiki_page['i']=""
    
    # There may be multiple infoboxes in the page
    curr_info_text="a"
    while (curr_info_text!=""):
        curr_info_text=extract_infobox()
        global_curr_wiki_page['i']+=curr_info_text
    global_curr_wiki_page['i']=extract_urls(global_curr_wiki_page['i'])
    
    ############# CATEGORIES #############################
    # extract categories, join them and modify original string
    category_text=get_categorical_text()
    global_curr_wiki_page['c']=extract_urls(category_text)

    ###########  EXTERNAL LINKS ##############################
    # extract external links
    ext_links=extract_ext_links()
    global_curr_wiki_page['l']=extract_urls(ext_links)
    
    
    ############### SELF CONTAINED references ##########################
    get_self_contained_refs_list()
    #global_curr_wiki_page['self_contained_refs_list']=list(map(extract_urls, self_contained_refs_list))
    
    ######  PAIRED REFS  ########################
    paired_refs_list=get_paired_refs_list()
    below_refs=extract_ext_refs()
    #global_curr_wiki_page['prl']=list(map(extract_urls,paired_refs_list))
    global_curr_wiki_page['r']=extract_urls(paired_refs_list)
    global_curr_wiki_page['r']+=" "+extract_urls(below_refs)

    global_curr_wiki_page['b']=curr_text
    global_curr_wiki_page['b']=extract_urls(global_curr_wiki_page['b'])
    
      
    for curr_key in global_curr_wiki_page:
        # global_curr_wiki_page[curr_key]=extract_urls(global_curr_wiki_page[curr_key])
        global_curr_wiki_page[curr_key]=curr_preproc_obj.tokenize_text(global_curr_wiki_page[curr_key])
        
    #return global_curr_wiki_page


# ### Words related stuff

# In[15]:


#################################################################3
# # Dealing with STEMMING

#the stemmer requires a language parameter
snow_stemmer = SnowballStemmer(language='english')

STEMMER_CACHE=dict()

def fetch_stemmed_version(curr_word):
    #https://stackoverflow.com/a/17539425/6427607
    if curr_word not in STEMMER_CACHE:
        STEMMER_CACHE[curr_word]= snow_stemmer.stem(curr_word)
    #if STEMMER_CACHE[curr_word] in ["base","locat","usual"]:
        #print("Weirdness quotient: ", curr_word)
    return STEMMER_CACHE[curr_word]

##################################################################################
# ### Create a master dict for each word with REQD sections

# * iterate through all pages
# * implement a function that takes a list of words and returns frequency stuff


def filter_stopwords(curr_lst):
    arr=[]
    for curr_word in curr_lst:
        if not curr_preproc_obj.is_in_stopwords_list(curr_word):
            arr.append(curr_word)
    return arr

CONST_LEN_THRESHOLD=18

def get_word_status(curr_word):
    # returns <pure alpha status, pure number status>
    stat_num=True
    stat_alpha=True
    for curr_ch in curr_word:
        if not (ord(curr_ch)>=0 and ord(curr_ch)<256):
            return False, False
        if curr_ch.isdigit():
            stat_alpha=False
        elif curr_ch.isalpha():
            stat_num=False
    return stat_alpha, stat_num
        
def approve_non_stemmed_words(curr_lst):
    arr=[]
    
    # List of checks
    ## len filter
    ## foreign character or alphanumeric (false, false etc)
    ## if numeric, reject above 4, for 4: reject aif first digit more than 2
    for curr_word in curr_lst:
        curr_word_len=len(curr_word)
        if curr_word_len>CONST_LEN_THRESHOLD:
            continue

        pure_alpha, pure_num=get_word_status(curr_word)
        if pure_alpha==False:
            # either a pure number
            if pure_num:
                if curr_word_len>4 or curr_word_len==3:
                    continue
                if curr_word_len==4 and curr_word[0] not in ['1','2']:
                    continue
            else:
                continue
        else:
            if curr_word_len==1:
                continue
        arr.append(curr_word)
    return arr

def get_stemmed_version_of_list(curr_lst):
    arr=[]
    for curr_word in curr_lst:
        ans=fetch_stemmed_version(curr_word)
        arr.append(ans)
    return arr

####################################################################################


# ### Handle stemming and filter

# In[16]:


def handle_stemming_and_filter():
    global global_curr_wiki_page
    for curr_key in global_curr_wiki_page:
        # this is COPY by reference
        curr_arr=global_curr_wiki_page[curr_key]
        curr_arr=filter_stopwords(curr_arr)
        curr_arr=approve_non_stemmed_words(curr_arr)
        curr_arr=get_stemmed_version_of_list(curr_arr)
        curr_arr=filter_stopwords(curr_arr)
        global_curr_wiki_page[curr_key]=curr_arr


# ## gen output

# In[17]:


ans_dict=dict()


# In[18]:


LOCAL_USE_WORDS_SET=set()
ZONE_FREQ=dict()
def gen_output():
    global global_curr_doc_id
    global curr_wiki_page
    
    ##############################
    global LOCAL_USE_WORDS_SET
    LOCAL_USE_WORDS_SET=set()
    ##############################
    global ZONE_FREQ    
    ############################
    curr_doc_id=global_curr_doc_id
    #################################
    str_doc_id=str(global_curr_doc_id)
    
    for curr_key in global_curr_wiki_page:
        ZONE_FREQ=dict()
        for curr_word in global_curr_wiki_page[curr_key]:
            
            # this word was already found in the zone before
            if curr_word in ZONE_FREQ:
                ZONE_FREQ[curr_word]+=1
            else:
                ZONE_FREQ[curr_word]=1
            
        for curr_word, word_freq in ZONE_FREQ.items():
            if curr_word in LOCAL_USE_WORDS_SET:
                # Means it has already been present in some zone
                # Also, it has to be present in GLOBAL STORAGE
                ans_dict[curr_word]+=curr_key+str(word_freq)
            else:
                # First time in any zone, insert it in the zone
                LOCAL_USE_WORDS_SET.add(curr_word)
                
                # DOC needs to be introduced to this word
                if curr_word in ans_dict:
                    # has occurred before in some other doc
                    ans_dict[curr_word]+='|'+str_doc_id
                else:
                    # has never occurred before, so no pipe
                    ans_dict[curr_word]=""
                    ans_dict[curr_word]+=str_doc_id
                    
                ans_dict[curr_word]+=curr_key+str(word_freq)


# ### Parser

# In[19]:



'''
Currently, you are disregarding all other tags like REVISION, DOC ID from the WIKI DUMP, ns
'''

class SaxParserHandler(xml.sax.ContentHandler):
    def __init__(self):
        #'''self.text = ""
        #self.title = ""'''
        global GLOBAL_DOC_ID_OFFSET
        self.docID = GLOBAL_DOC_ID_OFFSET
        self.curr_html_tag = ""
    
    def startElement(self, curr_tag, curr_attributes):
        self.curr_html_tag = curr_tag
        #all_unique_tags.add(curr_tag)

    def endElement(self, curr_tag):
        global curr_title,curr_text
        global global_curr_wiki_page
        global GLOBAL_TRACKING_TITLES
        # Time to store stuff related to the previous page
        if curr_tag == "page":
            
            self.docID += 1
            global global_curr_doc_id
            global_curr_doc_id=self.docID
            
            GLOBAL_TRACKING_TITLES+=str(self.docID)+":"+curr_title.strip()+'\n'
            #if self.docID%1000==0:
            #print(f"{self.docID}:{curr_title}->{datetime.now()}")'''
            
            
            global_curr_wiki_page=dict()
            process_wiki_page()
            handle_stemming_and_filter()
            gen_output()
            #dict_list.append(dict_now)
                
            #self.title = ""            
            #self.text = ""
            curr_title=""
            curr_text=""
            
    def characters(self, page_content):

        ###### OMIT HANDLE
        global curr_title

        #if "Database reports" in curr_title or curr_title=="Template:Infobox WTCC race report":
        #return
        
        if self.curr_html_tag == "title":
            #print("adding ", page_content)
            curr_title += page_content
            
        elif self.curr_html_tag == "text":
            global curr_text
            curr_text += page_content


# ### Initiation related

# In[ ]:



#PATH_TO_DUMP=sys.argv[1]
#PATH_TO_DUMP="./part_1"
#PATH_TO_INVERTED_INDEX_DIR=sys.argv[2]

WIKI_DATA = os.path.join(PATH_FOR_INPUT,INPUT_FILE_NAME)

# Setting up parser
parser = xml.sax.make_parser()
parser.setFeature(xml.sax.handler.feature_namespaces, 0)
parser_obj = SaxParserHandler()
parser.setContentHandler(parser_obj)


parser.parse(WIKI_DATA)


# ## Finale

# ## Write titles to the title file

# In[ ]:


FILE_RECORDS_NAME=os.path.join(BASIC_DIR_PATH,'title_logs_for_37.txt')
with open(FILE_RECORDS_NAME,"a+") as fd:
    fd.write(GLOBAL_TRACKING_TITLES)


# ### Final output

# In[ ]:


WORD_SEP='\n'
LST_SEP='|'
LOC_SEP='='
WORD_LST_SEP=':'


# In[ ]:


#  Writing to disk is a complex physical and logical process. It involves a lot of mechanics and control. It is much faster to tell the disk "Here, this is 10 MB of data, write it!" than telling it millions of times "Here, this is 1 byte of data, write it!". Therefore, the operating system has a mechanism to "collect" data that a process wants to write to disk before actually saving it to disk.
arr_now=list(ans_dict.keys()) 
arr_now.sort()
master_str=""
for curr_word in arr_now:
    master_str+=curr_word+LOC_SEP+ans_dict[curr_word]
    master_str+=WORD_SEP

ACTUAL_INVERTED_FILE=os.path.join(PATH_TO_INVERTED_INDEX_DIR,f"index_{CURR_FILE_ID}.txt")
with open(ACTUAL_INVERTED_FILE,"w") as fd:
    fd.write(master_str)


# In[ ]:


ending = datetime.now()
print("Total time is ", ending-begin)
print("####")


# In[ ]:




