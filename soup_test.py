import requests
from bs4 import BeautifulSoup, Comment
import contractions
import nltk
from bs4 import BeautifulSoup
from nltk import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import LancasterStemmer, WordNetLemmatizer
import inflect
import json
import re, string, unicodedata

external=[]

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

for URL in data["urls"]:
    URL = "http://bit.ly/2DrYyhH"

    r = requests.get(URL)
    soup = BeautifulSoup(r.content, "lxml")

    textdata=""
    for text in soup.body.find_all(string=True):
        if text.parent.name not in ['script', 'meta', 'link', 'style'] and not isinstance(text, Comment) and text != '\n':
            text =contractions.fix(text.strip())
            textdata+=(text)

    words = nltk.word_tokenize(textdata)
    def remove_non_ascii(words):
        """Remove non-ASCII characters from list of tokenized words"""
        new_words = []
        for word in words:
            new_word = unicodedata.normalize('NFKD', word).encode('ascii', 'ignore').decode('utf-8', 'ignore')
            new_words.append(new_word)
        return new_words

    def to_lowercase(words):
        """Convert all characters to lowercase from list of tokenized words"""
        new_words = []
        for word in words:
            new_word = word.lower()
            new_words.append(new_word)
        return new_words

    def remove_punctuation(words):
        """Remove punctuation from list of tokenized words"""
        new_words = []
        for word in words:
            new_word = re.sub(r'[^\w\s]', '', word)
            if new_word != '':
                new_words.append(new_word)
        return new_words

    def replace_numbers(words):
        """Replace all interger occurrences in list of tokenized words with textual representation"""
        p = inflect.engine()
        new_words = []
        for word in words:
            if word.isdigit():
                new_word = p.number_to_words(word)
                new_words.append(new_word)
            else:
                new_words.append(word)
        return new_words

    def remove_stopwords(words):
        """Remove stop words from list of tokenized words"""
        new_words = []
        for word in words:
            if word not in stopwords.words('english'):
                new_words.append(word)
        return new_words

    def stem_words(words):
        """Stem words in list of tokenized words"""
        stemmer = LancasterStemmer()
        stems = []
        for word in words:
            stem = stemmer.stem(word)
            stems.append(stem)
        return stems

    def lemmatize_verbs(words):
        """Lemmatize verbs in list of tokenized words"""
        lemmatizer = WordNetLemmatizer()
        lemmas = []
        for word in words:
            lemma = lemmatizer.lemmatize(word, pos='v')
            lemmas.append(lemma)
        return lemmas

    def normalize(words):
        words = remove_non_ascii(words)
        words = to_lowercase(words)
        words = remove_punctuation(words)
        words = replace_numbers(words)
        words = remove_stopwords(words)
        return words

    words = normalize(words)


    def lemmatize(words):

        lemmas = lemmatize_verbs(words)
        return lemmas

    external.append(lemmatize(words))

data['external'] = external

print(data)