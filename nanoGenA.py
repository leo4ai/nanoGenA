#!/usr/bin/env python3

import random
import time


class Candidate():
    
    def __init__(self, chrom=None):

        self.target = [c for c in "It was the best of times, it was the worst of times, " +
                                    "it was the age of wisdom, it was the age of foolishness, " +
                                    "it was the epoch of belief."]

        self.alphabet = [chr(c) for c in range(ord(' '), ord('z')+1)]

        self.alphabet_N = len(self.alphabet)
        self.target_N = len(self.target)
        
        if (chrom == None):
            self.chrom = [ self.alphabet[random.randint(0, self.alphabet_N-1)] for i in range(self.target_N) ]
        else:
            self.chrom = chrom
            
        self.fit = sum(1 for (a,b) in zip(self.chrom, self.target) if a != b)
        
        
    def __lt__(self, other):
        return self.fit < other.fit

        
    def __str__(self):
        return "fit {fit}  {candidate}".format(fit = self.fit, candidate = ''.join([i for i in self.chrom ]))


    def swap(self, a, b, prob):
        return (b if random.random() < prob else a)


    def crossover(self, other_candidate, prob):
        new_chrom = [ self.swap(a, b, prob) for (a,b) in zip(self.chrom, other_candidate.chrom) ]
        return Candidate(new_chrom)



class Evolution():
    
    def __init__(self):
        self.maxGen = 250*1000

    def offspring(self, candidates, p_cross):
        evo0 = [ candidates[i].crossover(candidates[i+2], p_cross) for i in range(3) ]
        evo1 = [ candidates[i].crossover(Candidate(), p_cross * 2) for i in range(5) ]
        
        evo = [candidates[0]] + evo0 + evo1
        evo.sort()
        
        return evo[:5]        
    
    def evolve(self):
        candidates = ([ Candidate() for i in range(5) ])
        candidates.sort()
        
        p_cross = 0.2
        i = 0

        while i < self.maxGen and candidates[0].fit > 0:
            candidates = self.offspring(candidates, p_cross)            
            if (i % 3000 == 0): 
                print("generation {generation}  {candidate}".format(generation = i, candidate = candidates[0]))
            p_cross = p_cross + 5e-7
            i = i + 1
        
        return (i, candidates[0])
    

if __name__ == '__main__':

    start = time.time()
    (i, candidate) = Evolution().evolve()
    elapsed = time.time() - start
    print("\n" + str(i) + "  " + str(candidate))
    print(str(elapsed) + " sec.")
