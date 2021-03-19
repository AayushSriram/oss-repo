# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 21:30:07 2021

@author: sriraa
"""
from string import ascii_lowercase as lower
from itertools import permutations

count = 0
cands = set([])

cand = 'chaos'
print(cand)
for num in range(5):
    for ber in range(26):
        c = lower[ber]
        word = list(cand[:num] + c + cand[num+1:])
        for perm in permutations(word):
            cands.add(perm)
print(len(cands))