import redis

redis = redis.Redis(host='localhost', port=6379)



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
