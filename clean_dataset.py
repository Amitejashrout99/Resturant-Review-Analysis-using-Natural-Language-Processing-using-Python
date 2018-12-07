import pandas as pd
import numpy as np
import re

'''
import nltk
from nltk.corpus import stopwords
stopWords = set(stopwords.words('english'))
'''

file1 = pd.read_csv("data.csv")
file2 = file1.replace(np.nan, 'NA', regex=True)
review_y=list(file2["review_text"])
review_clean=[];cr=[];review = ""

for i in review_y:
	for j in i:
		j=str(j)
		if(re.search(r'[a-z]',j) or re.search(r'[A-Z]',j) or re.search(r'[0-9]',j) or re.search(r'\s',j) or re.search(r'\'',j) or re.search(r'.',j)):
			review+=j
	review_clean.append(review)
	review=""

for i in review_clean:
	res=re.findall(r'n\'t',i)
	i = i.replace("n\'t",' not')
	cr.append(i)

final_clean_review = list()
final_clean_review=cr 
