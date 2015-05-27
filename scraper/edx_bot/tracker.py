import time
from utils.redis import redis


class Status(object):
    '''
    Used to keep track of the statuses of the documents in the crawl.
    '''
    UNVISITED   = 0
    VISITED     = 1
    IN_PROGRESS = 2
    FINISHED    = 3
    DISCARDED   = 4

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

    @classmethod
    def identify_sorted_set(cls, collection_kind, status_code):
        status = Status.classify_status_code(status_code)
        if status:
            return "crawl_statuses:" + collection_kind + ":" + status
        else:
            return None


    @classmethod
    def get_all_documents_by_status(cls, collection_kind, status_code, with_timestamps=False):
        sorted_set = cls.identify_sorted_set(collection_kind, status_code)
        if sorted_set:
            doc_IDs = redis.zrange(sorted_set, 0, -1, withscores=with_timestamps)
            if with_timestamps:
                return [(int(p[0]), int(p[1])) for p in doc_IDs]
            else:
                return [int(p) for p in doc_IDs]


    @classmethod
    def check_document_status(cls, collection_kind, doc_ID, status_code):
        sorted_set = cls.identify_sorted_set(collection_kind, status_code)
        if sorted_set:
            return redis.zscore(sorted_set, doc_ID) != None
        else:
            return False


    @classmethod
    def set_document_status(cls, collection_kind, doc_ID, status_code):
        sorted_set = cls.identify_sorted_set(collection_kind, status_code)
        if sorted_set:
            # http://stackoverflow.com/a/16299439/2708484
            timestamp = int(time.time())

            # Redis sorted sets don't allow repeats... therefore repeated
            # elements' timestamps/scores will be updated if needed
            redis.zadd(sorted_set, doc_ID, timestamp)


    @classmethod
    def delete_document_status(cls, collection_kind, doc_ID, status_code):
        sorted_set = cls.identify_sorted_set(collection_kind, status_code)
        if sorted_set:
            redis.zrem(sorted_set, doc_ID)


    @classmethod
    def update_document_status(cls, collection_kind, doc_ID, old_status_code, new_status_code):
        cls.delete_document_status(collection_kind, doc_ID, old_status_code)
        cls.set_document_status(collection_kind, doc_ID, new_status_code)
