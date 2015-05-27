import time
from utils.redis import redis


class Status(object):
    '''
    Used to keep track of the statuses of the documents in the crawl.
    '''
    # Document is ready to be crawled (hasn't been previously attempted).
    UNVISITED   = 0

    # Document has been previously processed, i.e. it's classified under
    # one of the statuses below... use this to quickly determine whether
    # a document has been processed.
    VISITED     = 1

    # Document crawl was attempted --theoretically, this status should only
    # apply while the crawl is taking place. As soon as a known error strikes
    # or the crawl finishes correctly, this should no longer apply.
    # (Subcategory of VISITED)
    IN_PROGRESS = 2

    # Document was not crawled because it did not fulfill the right criteria
    # (e.g. not in English), was incomplete in terms of content or there
    # was an error while attempting the crawl
    # (Subcategory of VISITED)
    DISCARDED   = 3

    # Document was crawled correctly.
    # (Subcategory of VISITED)
    FINISHED    = 4

    visited_types = [Status.IN_PROGRESS, Status.DISCARDED, Status.FINISHED]

    @classmethod
    def classify_status_code(cls, status_code):
        try:
            obj = cls.__dict__
            for var in dir(cls):
                if obj[var] == status_code:
                    return var.lower()

        except KeyError:
            return None



class Tracker(object):

    valid_collections = ['course_list', 'general_course_content',
        'video_transcripts']

    @classmethod
    def identify_sorted_set(cls, collection_kind, status_code):
        '''
        As long as the given status_code and collection_kind exist,
        return the name of the key in Redis that corresponds to it.
        '''
        status = Status.classify_status_code(status_code)

        if status and collection_kind in cls.valid_collections:
            return "crawl_statuses:" + collection_kind + ":" + status
        else:
            return None


    @classmethod
    def get(cls, collection_kind, status_code, with_timestamps=False):
        '''
        Get the document IDs (or tuples of document IDs and timestamps)
        corresponding to the given status_code and collection_kind.
        '''
        sorted_set = cls.identify_sorted_set(collection_kind, status_code)
        if sorted_set:
            doc_IDs = redis.zrange(sorted_set, 0, -1, withscores=with_timestamps)
            if with_timestamps:
                return [(int(p[0]), int(p[1])) for p in doc_IDs]
            else:
                return [int(p) for p in doc_IDs]


    @classmethod
    def check(cls, collection_kind, doc_ID, status_code):
        '''
        Check if the document with the provided doc_ID is classified under
        the given collection and status_code.
        '''
        sorted_set = cls.identify_sorted_set(collection_kind, status_code)
        if sorted_set:
            return redis.zscore(sorted_set, doc_ID) != None
        else:
            return False


    @classmethod
    def add(cls, collection_kind, doc_ID, status_code):
        '''
        Categorize the document with the given doc_ID under the given
        collection_kind and status_code. Insert the doc_ID as well as
        the timestamp of the event.
        '''
        sorted_set = cls.identify_sorted_set(collection_kind, status_code)
        if sorted_set:
            # http://stackoverflow.com/a/16299439/2708484
            timestamp = int(time.time())

            # Redis sorted sets don't allow repeats... therefore repeated
            # elements' timestamps/scores will be updated if needed
            redis.zadd(sorted_set, doc_ID, timestamp)

            # Mark the given document ID as Status.VISITED (unless the original
            # intent was to mark it as Status.UNVISITED or Status.VISITED
            # --this condition is necessary in order to stop recursive calls).
            # Additionally, make sure it's not in Status.UNVISITED (this will
            # likely be redundant, but that doesn't matter).
            if status_code in Status.visited_types:
                cls.add(collection_kind, doc_ID, status.VISITED)
                cls.delete(collection_kind, doc_ID, status.UNVISITED)


    @classmethod
    def delete(cls, collection_kind, doc_ID, status_code):
        '''
        Stop the document with the given doc_ID from being classified under
        the provided collection_kind's status_code.
        '''
        sorted_set = cls.identify_sorted_set(collection_kind, status_code)
        if sorted_set:
            redis.zrem(sorted_set, doc_ID)

            # Remove the document from Status.VISITED if it's being removed
            # from one of the following visited categories and it's not in any
            # of the other visited categories.
            if status_code in Status.visited_types:
                for visited_type in Status.visited_types:
                    if cls.check(collection_kind, doc_ID, visited_type):
                        return

                cls.delete(collection_kind, doc_ID, Status.VISITED)


    @classmethod
    def update(cls, collection_kind, doc_ID, new_status_code):
        '''
        Document with the given doc_ID is reassigned to a new status.

        Looks through the list of status types and removes the document
        from the data structure with conflicting types.
        '''
        # Delete the document from existing structures
        for visited_type in Status.visited_types:
            if cls.check(collection_kind, doc_ID, visited_type):
                cls.delete(collection_kind, doc_ID, visited_type)

        # Add the document to the new structure
        cls.add(collection_kind, doc_ID, new_status_code)
