from utils.sql import get_session
from utils.sql.models.course_video import CourseVideo
from utils.redis import redis
from redis.exceptions import ResponseError
from search_engine.nlp import tokenizer, normalize_token, is_valid_term

'''
Three underlying types of data structure in Redis for each document
type, as in video_transcripts, etc.:
    - (fdt) Sorted sets to record the frequency of a term t in a document d:
        - The name of the structure combines the collection type as well as
        the term. The keys of the sorted set are the document IDs and the
        scores (or values) are the frequencies of the term in the document.
        - ex.: "video_transcripts:my_term 4 7" means that there are 4 instances
        of "my_term" in document 7.
    - (ft) Hashes to record the number of documents containing a term t:
        - The name of the structure is essentially the collection type,
        the keys are the terms and the values are the number of documents
        containing them.
    - (s) Hashes to signal whether a document has been fully indexed:
        - Once a document is fully indexed, a flag is set on Redis to signal
        that said document does not need to be indexed again.

Relevant collection kinds (collections whose documents are indexed):
    - video_transcripts
'''

def fdt_name(collection_kind, term):
    '''
    Returns the name of the fdt structure (see above) for the given
    collection kind.
    '''
    return "fdt:" + collection_kind + ":" + term


def ft_name(collection_kind):
    '''
    Returns the name of the ft structure (see above) for the given
    collection kind.
    '''
    return "ft:" + collection_kind


def s_name(collection_kind):
    '''
    Returns the name of the s structure (see above) for the given
    collection kind.
    '''
    return "s:" + collection_kind


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

            for term in frequencies.keys():
                # print "indexing: (term, frequency) = (%s, %d)" % (term, frequencies[term])
                redis.zadd(fdt_name(collection, term), c.id, frequencies[term])
                redis.hincrby(ft_name(collection), term, 1)

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
    redis.hmset(collection_kind, {doc_ID: 1})


def get_frequency_of_term_in_document(collection_kind, term, doc_ID):
    '''
    Gets the frequency of the given term in the given document.
    '''
    collection = fdt_name(collection_kind, term)
    return redis.zscore(collection, doc_ID)


def get_number_of_documents_containing_term(collection_kind, term):
    '''
    Gets the number of documents containing the given term.
    '''
    return redis.hmget(ft_name(collection_kind), term)


def get_number_of_terms_in_collection(collection_kind):
    '''
    Get the total number of terms in the given collection.
    '''
    term_frequencies = [int(v) for v in redis.hvals(ft_name(collection_kind))]
    return sum(term_frequencies)
