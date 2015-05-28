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
