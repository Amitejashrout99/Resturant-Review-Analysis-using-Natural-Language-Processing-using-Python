######################## import all required stuff #########################
import re
import pandas as pd
import string
import csv

############## importing the dataset into program using pandas ##############

dataset = pd.read_csv('ogdataset.csv')

############## extracting required columns from the dataset  ################

ids = list(dataset['uniq_id']) 
restaurant_ids = list(dataset['restaurant_id']) #2
restaurant_names = list(dataset['name']) #4
reviews_title = list(dataset['title']) #6
reviews_date = list(dataset['review_date']) #7
reviews_text = list(dataset['review_text']) #8
reviewers = list(dataset['author']) #9
star_ratings = list(dataset['rating']) #12
visit_dates = list(dataset['visited_on']) #16    

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
print(positive_words_syns) 

for word in negative_words:    
    for syn in wordnet.synsets(word): 
        for l in syn.lemmas(): 
            negative_words_syns.append(l.name())

negative_words_syns = list(set(negative_words_syns))
print(negative_words_syns) 


########### Assigning scores for each review ##############

score = []

clean_reviews_text = ['good awesome tasty','foul bad ok'] #get from Ksh

for a_review in clean_reviews_text:
    _tempScore = 0
    _wordsInReview = a_review.split()
    for word in _wordsInReview:
        if(word in positive_words_syns):
            _tempScore+=1
        elif(word in negative_words_syns):
            _tempScore-=1
    score.append(_tempScore)
    
    
   
        

