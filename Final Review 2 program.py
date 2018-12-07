######################## import all required stuff #########################
import re
import pandas as pd
import numpy as np 
#import string
#import csv

############## importing the dataset into program using pandas ##############

_file1 = pd.read_csv("data.csv")
dataset = _file1.replace(np.nan, 'NA', regex=True)

############## extracting required columns from the dataset  ################

_review_text=list(dataset["review_text"]);_review_clean=[];_cr=[];_review = "";reviews_text = list()

for _i in _review_text:
	for _j in _i:
		_j=str(_j)
		if(re.search(r'[a-z]',_j) or re.search(r'[A-Z]',_j) or re.search(r'[0-9]',_j) or re.search(r'\s',_j) or re.search(r'\'',_j) or re.search(r'.',_j) or re.search(r'\!',_j)):
			_review+=_j
	_review_clean.append(_review)
	_review=""

for _i in _review_clean:
	_res=re.findall(r'n\'t',_i)
	_i = _i.replace("n\'t",' not')
	_cr.append(_i)

_cr1 = _cr

_restaurant_name=list(dataset["name"]);_restaurant_name_clean=[];_review="";restaurant_names = list()

for _i in _restaurant_name:
	for _j in _i:
		_j=str(_j)
		if(re.search(r'[a-z]',_j) or re.search(r'[A-Z]',_j) or re.search(r'[0-9]',_j) or re.search(r'\s',_j) or re.search(r'\'',_j) or re.search(r'.',_j) or re.search(r'\!',_j)):
			_review+=_j
	_restaurant_name_clean.append(_review)
	_review=""

_rn = _restaurant_name_clean 

_review_title=list(dataset["title"]);_title_clean=[];_rtc1=[];_title = "";reviews_title = list()

for _i in _review_title:
	for _j in _i:
		_j=str(_j)
		if(re.search(r'[a-z]',_j) or re.search(r'[A-Z]',_j) or re.search(r'[0-9]',_j) or re.search(r'\s',_j) or re.search(r'\'',_j) or re.search(r'.',_j) or re.search(r'\!',_j)):
			_title+=_j
	_title_clean.append(_title)
	_title=""

_rtc1 = _title_clean

_reviewer_list=list(dataset["author"]);_reviewer_clean=[];_rc1=[];_reviewer = "";reviewers = list()

for _i in _reviewer_list:
	for _j in _i:
		_j=str(_j)
		if(re.search(r'[a-z]',_j) or re.search(r'[A-Z]',_j) or re.search(r'[0-9]',_j) or re.search(r'\s',_j) or re.search(r'\'',_j) or re.search(r'.',_j) or re.search(r'\!',_j)):
			_reviewer+=_j
	_reviewer_clean.append(_reviewer)
	_reviewer=""

_rc1 = _reviewer_clean

ids = list(dataset['uniq_id']) #done
restaurant_ids = list(dataset['restaurant_id']) #2 done
restaurant_names = _rn #4 done
reviews_title = _rtc1 #6 done
reviews_date = list(dataset['review_date']) #7 done
reviews_text = _cr1 #8 done
reviewers = _rc1 #9 done
star_ratings = list(dataset['rating']) #12 done
visit_dates = list(dataset['visited_on']) #16 done   

################# Grouping restaurants having same ids ################
unique_restaurant_ids = []
indexes_with_same_rest_id = {}
for id in restaurant_ids:
    if id not in unique_restaurant_ids: 
        index = [i for i,x in enumerate(restaurant_ids) if x == id]
        unique_restaurant_ids.append(id) 
        indexes_with_same_rest_id[id] = index


######## Keywords indicating the nature of review ############

positive_words = ['perfect','great','good','tasty','friendly','spectacular','awesome','delicious','yummy','best','soothing','juicy']

negative_words = ['bad','tastless','sad','mild','foul']

positive_words_syns = [] 

negative_words_syns = []


##### Getting Synonums using nltk #####
from nltk.corpus import wordnet  
for word in positive_words:    
    for syn in wordnet.synsets(word): 
        for l in syn.lemmas(): 
            positive_words_syns.append(l.name())

positive_words_syns = list(set(positive_words_syns))
#print(positive_words_syns) 

for word in negative_words:    
    for syn in wordnet.synsets(word): 
        for l in syn.lemmas(): 
            negative_words_syns.append(l.name())

negative_words_syns = list(set(negative_words_syns))
#print(negative_words_syns) 


########### Assigning scores for each review ##############

'''
clean_reviews_text = ['good awesome tasty','foul bad ok'] #get from Ksh

for a_review in clean_reviews_text:
    _tempScore = 0
    _wordsInReview = a_review.split()
    for word in _wordsInReview:
        if(word in positive_words_syns):
            _tempScore+=1
        elif(word in negative_words_syns):
            _tempScore-=1
    score.append(_tempScore)'''

indexes_with_rest_id_greater_than_one_elements = {}   
for id,sublist in indexes_with_same_rest_id.items():
    if(len(sublist)>1):
        indexes_with_rest_id_greater_than_one_elements[id] = sublist    


def classifyReviewsOf(indexes):
    reviews = []
    positive_reviews = []
    negative_reviews = []
    insufficient_data_to_classify = []
    for index in indexes:
        reviews.append(reviews_text[index])
    for review in reviews:
        score = calcScore(review)
        if(score>0):
            positive_reviews.append(review)
        elif(score<-0):
            negative_reviews.append(review)
        else:
            insufficient_data_to_classify.append(review)     
    return positive_reviews,negative_reviews,insufficient_data_to_classify     #a lot of things


def calcScore(review):
    score = 0
    for word in review.split():
        if(word in positive_words_syns):
            score+=1
        elif(word in negative_words_syns):
            score-=1
    return score

positive_reviews=[]
negative_reviews=[]
insufficient_data_to_classify=[]
reqId = input("Enter Restaurant ID: ")
reqIndexes = indexes_with_same_rest_id[reqId]
positive_reviews,negative_reviews,insufficient_data_to_classify = classifyReviewsOf(reqIndexes)

############################ 

food_in_restautants={} # indexes of restaurants with cuisine type as key

food_types=["french","italian","chinese","indian","pakistani","spanish","mexican","english","dutch","european"]

restaurants_index=[];

for food_type in food_types:
    for review in reviews_text: 
        if(re.search(food_type,review)):
            restaurants_index.append(reviews_text.index(review))
    food_in_restautants[food_type]=restaurants_index;
    restaurants_index=[];
positive_reviews,negative_reviews,insufficient_data_to_classify = classifyReviewsOf(food_in_restautants['indian'])