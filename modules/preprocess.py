from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
import nltk
import pymorphy2

nltk.download('stopwords')
STOPWORDS = set(stopwords.words('russian'))

def preprocess(text):
    text.lower()
    tokens = tokinize(text)
    lemmas = lemmatize(tokens)
    clear_lemmas = remove_stopwords(lemmas)
    filtered_lemmas = list(filter(lambda w: len(w) > 2 , clear_lemmas))

    return filtered_lemmas

def tokinize(text):
    tokenizer = RegexpTokenizer(r'\b[а-яА-ЯёЁ]+\b')
    return tokenizer.tokenize(text)

def remove_stopwords(tokens):
    return [token for token in tokens 
            if token not in STOPWORDS]


def lemmatize(tokens):
    morph = pymorphy2.MorphAnalyzer()
    
    return [morph.parse(token)[0].normal_form 
            for token in tokens]
