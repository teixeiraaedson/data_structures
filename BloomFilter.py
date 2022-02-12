# Python 3.9.7
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 11 10:23:23 2022

@author: teixeiraedson
"""


import hashlib


# Defining the Bloom Filter lenght
bf_lenght = 10
# Setting its values to 0
bf = [0] * bf_lenght

# Converting hash values into integers
def bytes_to_int(hash_value):
    return int.from_bytes(hash_value, byteorder='big')

# The integers are then modulo divided by the length of the Bloom Filter to find the indices that need to be set inside the Bloom Filter
def bf_index(hashint):
    return hashint % bf_lenght

def fill_percent():
    return bf.count(1) / bf_lenght * 100;

# Filtering the Query - Checking if the query is new or not, to determine if the username probably already exists or not
def new_query(indices):
    new = False
    for i in indices:
        if bf[i] == 0:
            new = True
            break

    return new

def set_bloom(indices):
    for i in indices:
        bf[i] = 1

# Resetting the Filter 
# As the # of queries increase, the values in the filter-list are updated and this will increase the rate of false positives
# For the sake of this demonstration our list we'll be reset automatically if  the number of 1s in the list is greater 
# than 90% of the total elements in the list
while True:
    if fill_percent() > 90.0:
        print("Bloom Filter List reset")
        bf = [0] * bf_lenght

# Capturing username input and encoding it in 'utf-8' for hashing next 
    username = str(input("Please enter your username: ")).encode('utf-8')

# Hashing - The outputs of the hash functions (md5, sha224 and sha1) are stored in a list for further processing.
    hash1 = hashlib.md5()
    hash2 = hashlib.sha224()
    hash3 = hashlib.sha1()

    hash1.update(username)
    hash2.update(username)
    hash3.update(username)

# Maping input data to the defined output length
    hash_values = [hash1.digest(), hash2.digest(), hash3.digest()]

# Storing the integers (converted hash values) in a list
    hashintegers = list(map(bytes_to_int, hash_values))
    indices = list(map(bf_index, hashintegers))

# Username is available
    if new_query(indices):
        print("The username is available")
        set_bloom(indices)
# The username probably is not available
    else:
        print("The username probably is not available")