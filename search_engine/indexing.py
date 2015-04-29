from utils.sql import get_session
from utils.sql.models.course_video import CourseVideo
from utils.redis import redis

import requests
from search_engine.utils import english_dict, english_contractions \
    whitespace_tokenizer, snowball_stemmer


def index_video_transcripts():
    '''
    Get sorted set from Redis containing info about video transcripts.
    Get video transcripts from Postgres.
    '''
    '''
    r_video_transcripts = redis object
    for video_transcript in SQL_video_transcripts:
        term_frequencies = get_valid_term_frequencies(video_transcript)
        for term in term_frequencies.keys:
            # add to r_video_transcript sorted set
            # increment appropriate key in video_transcript hash
        # finished parsing video_transcript... call save() in Redis
    '''
    self.session = get_session()

    for c in self.session.query(CourseVideo):
        # Only proceed if the document has not been fully indexed
        if redis.hmget("fi_video_transcripts", c.id)[0] == 0:
            transcript = c.transcript.lower()
            frequencies = get_frequencies_of_valid_terms(transcript)

            for term in frequencies.keys():
                redis.zadd("ii_video_transcripts:%s" % term, frequencies[term], term)
                redis.hincrby("ttc_video_transcripts", term, frequencies[term])

            # Signal that the document has been properly indexed
            redis.hmset("fi_video_transcripts", c.id, 1)

        redis.bgsave()

    self.session.close()


def get_frequencies_of_valid_terms(text):
    frequencies = {}
    tokens = whitespace_tokenizer.tokenize(text)

    for token in tokens:
        token = snowball_stemmer.stem(token)
        if token in frequencies.keys():
            frequencies[token] += 1
        elif is_valid_term(token):
            frequencies[token] = 1

    return frequencies


def is_valid_term(term):
    return in_english_dictionary(term) or in_wikipedia(term)


def in_english_dictionary(term):
    return english_dict.check(term)


def in_wikipedia(term):
    url = "http://en.wikipedia.org/w/api.php?format=json&action=query&titles=%s" \
        % term

    r = requests.get(url).json()
    return '-1' not in r['query']['pages'].keys()
