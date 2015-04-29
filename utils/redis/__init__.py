import redis

redis = redis.Redis(host='localhost', port=6379)


'''
Sorted sets containing the inverted indexes for each term
ex.:
    "ii_video_transcripts:quicksort" is the name, the keys
    are document IDs and the scores are the frequencies of
    the terms in said documents.
'''
inverted_index_sorted_sets = [
    'ii_video_transcripts',
]

'''
Hashes containing the total term counts.
ex.:
    "ttc_video_transcripts" is the name of the hash, the
    keys are the terms present in the video transcripts
    and the values are the total frequencies of said terms.
'''
total_term_counts_hashes = [
    'ttc_video_transcripts',
]

'''
Hashes signaling which documents in redis have been fully indexed.
ex.:
    "fi_video_transcripts",
'''
fully_indexed_signal_hashes = [
    'fi_video_transcripts',
]

'''
REDIS COMMANDS:
---------------


SORTED SET
--------------
for a sorted set "friends"...
zadd friends 3 "bob" ---> add key "bob" with score "3"
zscore friends bob ---> 3
zincrby friends 1 "pepe" --> creates "pepe" key if it doesn't exist and sets to 1


HASH
--------------
for a hash "papers"...
hmset papers "yeygeniv" 3
hmget papers "yeygeniv" ---> 3
hlen papers ---> number of keys in "papers"
hincrby papers "yeygeniv" 5 ---> increment key "yeygeniv" by 5
hvals papers
'''
