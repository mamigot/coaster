import re
import enchant
import requests
from nltk.tokenize import RegexpTokenizer, WhitespaceTokenizer
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords


tokenizer = WhitespaceTokenizer()
stemmer = SnowballStemmer("english")
stopwords = set(stopwords.words("english"))

english_dict = enchant.Dict("en_US")


def tokenize(text):
    return tokenizer.tokenize(text)


def normalize_token(token):
    token = token.lower()
    token = stemmer.stem(token)
    return remove_needless_punctuation(token).strip()


def remove_needless_punctuation(text):
    '''
    Remove punctuation that indicates pauses, as well
    as parentheses, brackets, etc.
    '''
    return re.sub(ur"[,.;:!\?\[\]\(\)\{\}<>\"]+", '', text)


def is_stopword(term):
    return term in stopwords


def is_valid_term(term):
    return in_english_dictionary(term) or in_wikipedia(term)


def in_english_dictionary(term):
    return english_dict.check(term)


def in_wikipedia(term):
    url = "http://en.wikipedia.org/w/api.php?format=json&action=query&titles=%s" \
        % term

    r = requests.get(url).json()
    if 'query' not in r: return False
    return '-1' not in r['query']['pages'].keys()
