from utils.sql import get_session
from utils.sql.models.course_video import CourseVideo
from utils.redis import redis
from redis.exceptions import ResponseError

from search_engine.nlp import tokenizer, normalize_token, is_valid_term


def get_term_frequency_in_document(collection_kind, term, doc_ID):
    '''
    Gets the frequency of the given term in the given document.

    ex.: "zscore ii_video_transcripts:hotel 7" for the following values:
        collection_kind = "ii_video_transcripts"
        doc_ID = 7
        term = "hotel"
    '''
    collection = "%s:%s" % (collection_kind, term)
    return redis.zscore(collection, doc_ID)


def get_number_of_documents_containing_term(collection_kind, term):
    '''
    Gets the number of documents containing the given term.

    ex.: "hvals ttc_video_transcripts hotel"
    '''
    return redis.hmget(collection_kind, term)


def get_number_of_terms_in_collection(collection_kind):
    '''
    Get the total number of terms in the given collection.

    ex.: "hvals ttc_video_transcripts"
    '''
    return sum([int(v) for v in redis.hvals(collection_kind)])


def index_video_transcripts():
    session = get_session()

    for c in session.query(CourseVideo).filter(CourseVideo.transcript != None):
        # Only proceed if the document has not been fully indexed
        if redis.hmget("fi_video_transcripts", c.id)[0] == None:
            print "Building inverted index for video transcript with id=%d..." % c.id

            transcript = c.transcript.lower()
            frequencies = determine_frequencies_of_valid_terms(transcript)

            for term in frequencies.keys():
                # print "indexing: (term, frequency) = (%s, %d)" % (term, frequencies[term])
                redis.zadd("ii_video_transcripts:%s" % term, c.id, frequencies[term])
                redis.hincrby("ttc_video_transcripts", term, frequencies[term])

            # Signal that the document has been fully indexed
            redis.hmset("fi_video_transcripts", {c.id: 1})

        else:
            print "Already considered. Skipping video transcript with id=%d..." % c.id

        # Blocking operation to ensure that the data is written to disk.
        # If we try to save while Redis is already saving, then ignore.
        try:
            redis.save()
        except ResponseError, e:
            if e != "Background save already in progress":
                session.close()
                raise

    session.close()


def determine_frequencies_of_valid_terms(text):
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
