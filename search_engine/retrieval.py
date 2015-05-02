from heapq import heappush, heappop
from search_engine.stats import get_document_frequency_pairs_for_term, \
    get_weight_of_term_in_document, get_weight_of_term_in_query, \
    get_magnitude_of_weights_vector


'''
Uses the inverted index to rank the document collection
with regard to a query and identifies the top matching docs
following the vector model.
'''
def retrieve_using_vector_model(collection_kind, tokenized_query, limit=None):
    documents = {}
    for qterm in tokenized_query:
        qterm_weight = get_weight_of_term_in_query(collection_kind, qterm)
        inverted_list = get_document_frequency_pairs_for_term(collection_kind, qterm)

        for doc_ID, frequency in inverted_list:
            dterm_weight = get_weight_of_term_in_document(frequency)

            if doc_ID in documents:
                documents[doc_ID] += qterm_weight * dterm_weight
            else:
                documents[doc_ID] = qterm_weight * dterm_weight

    ranked_docs = []
    for doc_ID, accumulated in documents.iteritems():
        weights_mag = get_magnitude_of_weights_vector(collection_kind, doc_ID)
        similarity_score = accumulated / weights_mag
        # Multiply score by -1 to implement a max-heap
        # (see http://stackoverflow.com/a/2501527/2708484 )
        heappush(ranked_docs, (similarity_score * -1, doc_ID))

    # Number of retrieved results specified by 'limit'
    most_relevant_doc_IDs = []
    limit = limit if limit else len(ranked_docs)
    for i in range(limit):
        if ranked_docs:
            most_relevant_doc_IDs.append(heappop(ranked_docs)[1])
        else: break

    return most_relevant_doc_IDs
