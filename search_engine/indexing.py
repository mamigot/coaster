from utils.sql import get_session
from utils.sql.models.course_video import CourseVideo
from utils.redis import redis
from redis.exceptions import ResponseError

from search_engine import fdt_name, ft_name, wd_name, s_name
from search_engine.nlp import tokenizer, normalize_token, is_valid_term
from search_engine.stats import get_weight_of_term_in_document, \
    get_magnitude_of_vector


def index_video_transcripts():
    session = get_session()
    collection = "video_transcripts"
    print "Indexing video transcripts..."

    for c in session.query(CourseVideo).filter(CourseVideo.transcript != None):
        # Only proceed if the document has not been fully indexed
        if not document_has_been_fully_indexed(s_name(collection), c.id):
            print "\nBuilding inverted index for document with id=%d..." % c.id

            transcript = c.transcript.lower()
            frequencies = determine_frequencies_of_valid_terms(transcript)
            doc_term_weights = []

            for term in frequencies.keys():
                print "indexing: (term, frequency) = (%s, %d)" % (term, frequencies[term])
                # Set the frequency of the term in the document
                redis.zadd(fdt_name(collection, term), c.id, frequencies[term])
                # Increment the frequency of the term in the collection
                redis.hincrby(ft_name(collection), term, frequencies[term])

                w = get_weight_of_term_in_document(frequencies[term])
                doc_term_weights.append(w)

            doc_weights_magnitude = get_magnitude_of_vector(doc_term_weights)
            # Set the magnitude of the vector of the document's term weights
            redis.hmset(wd_name(collection), {c.id : doc_weights_magnitude})

            signal_full_indexing_of_document(s_name(collection), c.id)
            print "Finished. %s terms examined in document with id=%d..." % \
                (len(frequencies.keys()), c.id)
            try:
                # Blocking operation to ensure that the data is written to disk.
                # If we try to save while Redis is already saving, then ignore.
                redis.bgsave()
                redis.save()
            except ResponseError, e:
                if "Background save already in progress" not in e:
                    session.close()
                    raise

        else:
            print "\nAlready considered. Skipping video transcript with id=%d..." % c.id

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


def document_has_been_fully_indexed(collection_kind, doc_ID):
    '''
    Returns True if the signal that the document has been fully indexed
    is set for a document of a given ID.

    ex.: "hmget fi_video_transcripts 7"
    '''
    return '1' in redis.hmget(collection_kind, doc_ID)


def signal_full_indexing_of_document(collection_kind, doc_ID):
    redis.hmset(collection_kind, {doc_ID : 1})
