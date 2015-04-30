from utils.sql import get_session
from utils.sql.models.course_video import CourseVideo
from utils.redis import redis

import re
import requests
from search_engine.nlp import english_dict, english_contractions, \
    tokenizer, stemmer


def index_video_transcripts():
    session = get_session()

    for c in session.query(CourseVideo).filter(CourseVideo.transcript != None):
        # Only proceed if the document has not been fully indexed
        if redis.hmget("fi_video_transcripts", c.id)[0] == None:
            print "Building inverted index for video transcript with id=%d..." % c.id

            transcript = c.transcript.lower()
            frequencies = get_frequencies_of_valid_terms(transcript)

            for term in frequencies.keys():
                print "indexing: (term, frequency) = (%s, %d)" % (term, frequencies[term])
                redis.zadd("ii_video_transcripts:%s" % term, c.id, frequencies[term])
                redis.hincrby("ttc_video_transcripts", term, frequencies[term])

            # Signal that the document has been fully indexed
            redis.hmset("fi_video_transcripts", {c.id: 1})

        else:
            print "Already considered. Skipping video transcript with id=%d..." % c.id

        # Blocking operation to ensure that the data is written to disk
        redis.save()

    session.close()


def get_frequencies_of_valid_terms(text):
    frequencies = {}
    tokens = tokenizer.tokenize(text)

    for token in tokens:
        token = normalize_token(token)
        if token:
            if token in frequencies.keys():
                frequencies[token] += 1
            elif is_valid_term(token):
                frequencies[token] = 1

    return frequencies


def normalize_token(token):
    token = stemmer.stem(token)
    return remove_needless_punctuation(token).strip()


def remove_needless_punctuation(text):
    '''
    Remove punctuation that indicates pauses, as well
    as parentheses, brackets, etc.
    '''
    return re.sub(ur"[,.;:\[\]\(\)\{\}]+", '', text)


def is_valid_term(term):
    return in_english_dictionary(term) or in_wikipedia(term)


def in_english_dictionary(term):
    return english_dict.check(term)


def in_wikipedia(term):
    url = "http://en.wikipedia.org/w/api.php?format=json&action=query&titles=%s" \
        % term

    r = requests.get(url).json()
    return '-1' not in r['query']['pages'].keys()
