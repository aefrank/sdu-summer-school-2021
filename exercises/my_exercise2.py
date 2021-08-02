# Exercise 2
# Author: Andrea Frank <aefrank17@gmail.com>
# Date: 02 August, 2021 
# SDU Summer School 2021, Odense Denmark

import math
import numpy as np



def NEAREST_NEIGHBOR(q,tree):
    dists = np.linalg.norm(q-tree["nodes"])
    index = np.argmin(dists)
    return tree["nodes"][index], dists[index]

step = 0.01
def STEER(q,qnear,dist=None):
    if dist is None:
        dist = np.linalg.norm(q-qnear)
    if dist > step:
        q = qnear + step * (q-qnear)/dist
    return q
    

def EXTEND(tree,q):
    qnear, dist = NEAREST_NEIGHBOR(q,tree)
    qnew = STEER(q,qnear,dist)
    if (qnew is not None):
        ADD_VERTEX(tree,q)
        ADD_EDGE(tree,q,qnew)
        if (q == qnear):
            return "reached"
        else:
            return "advanced"
    return "trapped"


def CONNECT(tree,q):
    state = "advanced"
    while(state=="advanced"):
        state = EXTEND(tree,q)
    return state

MAX_ITERS=1000

def RRT_CONNECT():
    for _ in range(MAX_ITERS):
        qs = SAMPLE()
        if (not EXTEND(tree_a,qs)=="trapped"):
            if (CONNECT(tree_b,qnew)=="reached"):
                return PATH(tree_a,tree_b)
        SWAP(tree_a,tree_b)
    return None