#!/usr/bin/env python3

import ray
import numpy as np
from numba import jit
import time
from itertools import chain


targetStr = "It was the best of times, it was the worst of times, " \
                "it was the age of wisdom, it was the age of foolishness, " \
                "it was the epoch of belief."

target = np.array([ord(c) for c in targetStr])
targetLen = len(target)
lower = ord(' ')
upper = ord('z')
    

@jit(nopython=True)
def fit(chrom):
    return np.count_nonzero(chrom-target)


@jit(nopython=True)
def crossover(chrom1, chrom2, prob):
    return \
        np.array( [ (chrom2[i] if np.random.random() < prob else chrom1[i]) \
            for i in np.arange(chrom1.size)] )
    

def toString(chrom):
    return "fit {fit}  {candidate}" \
                .format(fit = fit(chrom), candidate = ''.join(list(map(chr, chrom))))


@jit(nopython=True)
def randomChrom(n = targetLen):
    return np.random.randint(lower, upper, size=n)


@ray.remote
def evolve(candidates, p_cross, max_iter):
    i = 0
    while i < max_iter and fit(candidates[0]) > 0:
        evo0 = [ crossover(candidates[i], candidates[i+2], p_cross) for i in range(3) ]
        evo = [candidates[0]] + evo0 + [ randomChrom() for _ in range(5)]
        evo.sort(key=fit)
        
        candidates = evo[:5]
        i = i + 1
    
    return candidates  


def cycles(pool_N = 2):
    
    candidates = [ randomChrom() for i in range(5) ]
    candidates.sort(key=fit)
    p_cross = 0.1
    i = 0
    
    while fit(candidates[0]) > 0:
        max_iter = (1 + i/2) * 10
        print("Cycle {cycle} (#{pop})  {candidate}" \
                .format(cycle = i, pop = int(max_iter), candidate = toString(candidates[0])))
        
        subpopulations = ray.get( [evolve.remote(candidates, p_cross, max_iter) for _ in range(pool_N)] )
        subpopulations = list(chain.from_iterable(subpopulations))
        subpopulations.sort(key=fit)
        
        candidates = subpopulations[:5]
        
        p_cross = p_cross + 5e-7
        i = i + 1
        
    return candidates[0]
        
    

if __name__ == '__main__':

    ray.init()
    
    start = time.time()
    candidate = cycles(2)
    elapsed = time.time() - start
    
    print("solution  " + toString(candidate))
    print(str(elapsed) + " sec.")
