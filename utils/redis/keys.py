'''
The classes in this module contain the functions that are used to get
the names of the data structures in Redis.
'''


class Scraper(object):
    '''
    Used to keep track of the different types of documents that are crawled.
    '''

    class Status(object):
        IN_PROGRESS = 1
        FINISHED    = 2
        DISCARDED   = 3

        @classmethod
        def discern_status(cls, status_code):
            try:
                obj = cls.__dict__
                for var in dir(cls):
                    if obj[var] == status_code:
                        return var.lower()

            except KeyError:
                return None

    @classmethod
    def status_name(cls, collection_kind, status_code):
        '''
        ex.
            status_name('video_transcripts', Scraper.Status.IN_PROGRESS)
            >>> 'crawl_statuses:video_transcripts:in_progress'
        '''
        status = cls.Status.discern_status(status_code)
        return "crawl_statuses:" + collection_kind + ":" + status


class SearchEngine(object):
    '''
    Used to keep track of the TDxIDF calculations for each type of doc:

        - (fdt) Sorted sets to record the frequency of a term t in a document d.

        - (ft)  Hashes to record the number of documents containing a term t.

        - (wd)  Hashes to record the magnitude of the vector of weights of
                the terms in a document.

        - (s)   Hashes to signal whether a document has been fully indexed:


    Relevant collection kinds (collections whose documents are indexed):
        - video_transcripts


    Read for more reference:
        - http://dl.acm.org/citation.cfm?id=1132959
    '''

    @staticmethod
    def fdt_name(collection_kind, term):
        '''
        Returns the name of the fdt structure (see above) for the given
        collection kind.

        - ex.: "video_transcripts:my_term 4 7"
            - there are 4 instances of "my_term" in document 7.
        '''
        return "fdt:" + collection_kind + ":" + term

    @staticmethod
    def ft_name(collection_kind):
        '''
        Returns the name of the ft structure (see above) for the given
        collection kind.
        '''
        return "ft:" + collection_kind

    @staticmethod
    def wd_name(collection_kind):
        '''
        Returns the name of the wd structure (see above) for the given
        collection kind.
        '''
        return "wd:" + collection_kind

    @staticmethod
    def s_name(collection_kind):
        '''
        Returns the name of the s structure (see above) for the given
        collection kind.

        Once a document is fully indexed, a flag is set on Redis to signal
        that said document does not need to be indexed again.
        '''
        return "s:" + collection_kind
