#! /usr/bin/env python3
# coding=utf-8

class UnionFind(object):
    """
    Weighted union (by size) with path compression.
    Amortized cost: inverse Ackermann function.
    """
    def __init__(self, N):
        self._count = N
        self._id = [i for i in range(N)]
        self._sz = [1] * N

    def count(self):
        return count

    def find(self, p):
        root = p
        while root != self._id[root]:
            root = self._id[root]
        # path compression
        while root != p: 
            new_p = self._id[p]
            self._id[p] = root
            p = new_p

        return root

    def connected(self, p, q):
        return self.find(p) == self.find(q)

  
    def union(self, p, q):
        i = self.find(p)
        j = self.find(q)
        if i == j: return
        # weighted union by size
        if self._sz[i] < self._sz[j]:  
            self._id[i] = j 
            self._sz[j] += self._sz[i]
        else:
            self._id[j] = i 
            self._sz[i] += self._sz[j]
        self._count -= 1
