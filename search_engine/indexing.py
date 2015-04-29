from utils.redis import redis
import requests, enchant


english_dict = enchant.Dict("en_US")


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
    pass


def get_valid_term_frequencies(text):
    '''
    frequencies = {}
    tokens = tokenize(text)
    for token in tokens:
        token = token.stem().lower()
        if token in frequencies.keys:
            # increment frequencies[token]
        elif is_valid_term(token):
            frequencies[token] = 1
    return frequencies
    '''
    pass


def is_valid_term(term):
    return in_english_dictionary(term) or in_wikipedia(term)


def in_english_dictionary(term):
    return english_dict.check(term)


def in_wikipedia(term):
    url = "http://en.wikipedia.org/w/api.php?format=json&action=query&titles=%s" \
        % term

    r = requests.get(url).json()
    return '-1' not in r['query']['pages'].keys()
