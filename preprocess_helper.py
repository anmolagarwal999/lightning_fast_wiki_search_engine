import os
import sys
import xml.sax
from datetime import datetime
import re
import json
import nltk
from nltk.corpus import stopwords

class PreprocessHandlerClass:
    def __init__(self):
        self.TOKEN_REGEX=re.compile(r'[a-z0-9]+')
        ######  Filling STOPWORDS ######
        self.final_stopwords=[]
        self.fill_stopwords()
        self.final_stopwords_len=len(self.final_stopwords)
        #############################

    def tokenize_text(self,curr_chunk):
        curr_tokens=self.TOKEN_REGEX.findall( curr_chunk)
        return curr_tokens

    def is_in_stopwords_list(self,curr_txt):
        lb=0
        ub=self.final_stopwords_len-1
        mid=-1
        while(lb<=ub):
            mid=(lb+ub)//2
            mid_str=self.final_stopwords[mid]
            if mid_str==curr_txt:
                return True
            elif mid_str<curr_txt:
                lb=mid+1
            else:
                ub=mid-1
        return False

    def fill_stopwords(self):
        sw_nltk = stopwords.words('english')

        sp_stops=['those', 'on', 'own', '’ve', 'yourselves', 'around', 'between', 'four', 'been', 'alone', 'off', 'am', 'then', 'other', 'can', 'regarding', 'hereafter', 'front', 'too', 'used', 'wherein', '‘ll', 'doing', 'everything', 'up', 'onto', 'never', 'either', 'how', 'before', 'anyway', 'since', 'through', 'amount', 'now', 'he', 'was', 'have', 'into', 'because', 'not', 'therefore', 'they', 'n’t', 'even', 'whom', 'it', 'see', 'somewhere', 'thereupon', 'nothing', 'whereas', 'much', 'whenever', 'seem', 'until', 'whereby', 'at', 'also', 'some', 'last', 'than', 'get', 'already', 'our', 'once', 'will', 'noone', "'m", 'that', 'what', 'thus', 'no', 'myself', 'out', 'next', 'whatever', 'although', 'though', 'which', 'would', 'therein', 'nor', 'somehow', 'whereupon', 'besides', 'whoever', 'ourselves', 'few', 'did', 'without', 'third', 'anything', 'twelve', 'against', 'while', 'twenty', 'if', 'however', 'herself', 'when', 'may', 'ours', 'six', 'done', 'seems', 'else', 'call', 'perhaps', 'had', 'nevertheless', 'where', 'otherwise', 'still', 'within', 'its', 'for', 'together', 'elsewhere', 'throughout', 'of', 'others', 'show', '’s', 'anywhere', 'anyhow', 'as', 'are', 'the', 'hence', 'something', 'hereby', 'nowhere', 'latterly', 'say', 'does', 'neither', 'his', 'go', 'forty', 'put', 'their', 'by', 'namely', 'could', 'five', 'unless', 'itself', 'is', 'nine', 'whereafter', 'down', 'bottom', 'thereby', 'such', 'both', 'she', 'become', 'whole', 'who', 'yourself', 'every', 'thru', 'except', 'very', 'several', 'among', 'being', 'be', 'mine', 'further', 'n‘t', 'here', 'during', 'why', 'with', 'just', "'s", 'becomes', '’ll', 'about', 'a', 'using', 'seeming', "'d", "'ll", "'re", 'due', 'wherever', 'beforehand', 'fifty', 'becoming', 'might', 'amongst', 'my', 'empty', 'thence', 'thereafter', 'almost', 'least', 'someone', 'often', 'from', 'keep', 'him', 'or', '‘m', 'top', 'her', 'nobody', 'sometime', 'across', '‘s', '’re', 'hundred', 'only', 'via', 'name', 'eight', 'three', 'back', 'to', 'all', 'became', 'move', 'me', 'we', 'formerly', 'so', 'i', 'whence', 'under', 'always', 'himself', 'in', 'herein', 'more', 'after', 'themselves', 'you', 'above', 'sixty', 'them', 'your', 'made', 'indeed', 'most', 'everywhere', 'fifteen', 'but', 'must', 'along', 'beside', 'hers', 'side', 'former', 'anyone', 'full', 'has', 'yours', 'whose', 'behind', 'please', 'ten', 'seemed', 'sometimes', 'should', 'over', 'take', 'each', 'same', 'rather', 'really', 'latter', 'and', 'ca', 'hereupon', 'part', 'per', 'eleven', 'ever', '‘re', 'enough', "n't", 'again', '‘d', 'us', 'yet', 'moreover', 'mostly', 'one', 'meanwhile', 'whither', 'there', 'toward', '’m', "'ve", '’d', 'give', 'do', 'an', 'quite', 'these', 'everyone', 'towards', 'this', 'cannot', 'afterwards', 'beyond', 'make', 'were', 'whether', 'well', 'another', 'below', 'first', 'upon', 'any', 'none', 'many', 'serious', 'various', 're', 'two', 'less', '‘ve']
        stopwords_lst=[]

        reluctant_removals=['image','page','link','list','jpg','file','class','edit','main','comment','caption','text','note','type','pdf','map']
        emergency_reluctant_removals=['people','high','origin','public','birth','former','man','general','world','win','big','short','record','system','day','region','born','service','wikipedia','need','perform','publish','small','dead','start','time','size','date','small','group','review','year','talk','article','return','found','end']
        wikipedia_based_stopwords=['authority','control','ref','reflist','references','cite','web','url',
                                'user','template','format','display','title','see','also'
                                'type','infobox','navbox','font','background','listclass','citatation','citations',
                                'br','colwidth','width',
                                'width1','width2','width3','width4','tablewidth','groupwidth','bars',
                                'align','span','center','nowiki','flagicon','redirect','timestamp','linecolor',
                                'category','colspan', 'rowspan','left','right','defaultsort','margin','scope','alt','id',
                                'nbsp','amp','border','footnote','disambiguation','utc','access','color','style','archive','use','status','div','box','wikiproject','linksummary','internetarchivebot', 'delete','otherlink','ul','en','php','whitelist','contributor','contribute','pagename','com','bgcolor','known','later','like',
                                'open','follow','include','said','built','based','local','usually','bases','usual','unit','number','select','picture','colour','custom','example','mean','org','svg','gov','col','syntaxhighlight'
                                ]
        additional_to_add=['usersummary','ipsummary','domain','refnum']

        stopwords_lst.extend(sw_nltk)
        stopwords_lst.extend(sp_stops)
        stopwords_lst.extend(additional_to_add)
        stopwords_lst.extend(wikipedia_based_stopwords)
        stopwords_lst.extend(reluctant_removals)
        # stopwords_lst.extend(emergency_reluctant_removals)


        STOPWORDS_FINAL=[]
        for wrd in stopwords_lst:
            STOPWORDS_FINAL.extend(self.tokenize_text(wrd))

        STOPWORDS_FINAL=list(set(STOPWORDS_FINAL))
        STOPWORDS_FINAL.sort()
        STOPWORDS_FINAL_LEN=len(STOPWORDS_FINAL)
        self.final_stopwords=STOPWORDS_FINAL