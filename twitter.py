import json
from pprint import pprint
import re
import urllib3.request
from bs4 import BeautifulSoup
from urllib.request import urlopen
from collections import Counter
from string import punctuation
import requests
import nltk
#nltk.download('stopwords')
from nltk.tokenize import RegexpTokenizer
from urllib.error import HTTPError
from urllib.error import URLError
import urllib.request
import  contractions
from nltk import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import LancasterStemmer, WordNetLemmatizer



with open('data.json') as file:
    data = json.load(file)
data = json.load(open('data.json'))
hashtags=[]
for key in data["tweets"]:

    for i in key.split():
        if i.startswith("#"):
         hashtags.append((i ))
        else:
            continue
    data['hashtags']=hashtags





words=[]
external = []

for url in data["urls"]:
    # try:




        print(url)
    #
    # response = urllib.request.urlopen(url)
    # html = response.read()
    # text = obo.stripTags(html).lower()  # add the string method here.
    # wordlist = text.split()
    #
    # print(wordlist)
        page = requests.get(url.strip())
    # # except requests.exceptions.ConnectionError :
    # #     r.status_code = "Connection refused"
    #
        soup = BeautifulSoup(page.text,"html.parser")
        text=soup.get_text()
        text=re.sub('\[[^]]*\]', '', text)
        print(text)
        text=contractions.fix(text)
        text=re.compile(r'\W+', re.UNICODE).split(text)
        print(text)
        words = nltk.word_tokenize(text)
        #print(words)



data['external'] = external
import json
# with open('data.txt', 'w') as outfile:
#     json.dump(data, outfile)
