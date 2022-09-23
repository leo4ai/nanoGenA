# nanoGenA
Nanogenetic algorithm - a tiny implementation of a microgenetic algorithm.

The goal is to learn this sentence

> It was the best of times, it was the worst of times, 
> it was the age of wisdom, it was the age of foolishness, 
> it was the epoch of belief.

Thus the fitness function is as simple as comparing a candidate (random) sentence against the goal sentence. Here, zero fit means optimal fit meaning that a candidate sentence is identical, character by character, to the goal sentence. 

Evolve a small population of five candidate solutions at any given generation. In the selection stage, first sort by fittest first, and then crossover the first and third, and second and fourth, and then include 5 totally random additional candidate solutions. Then sort again by fittest first and select the top 5 fittest for the next round. Iterate until the (absolute) optimum is reached.

The non-parallel version is an object based implementation with no parallelism. On the other hand, the parallel version is implemented in a functional approach which includes performance optimizations derived from the inclusion of Ray, for distributed computing, and Numba, for JIT optimizations. By using the parallel version with 2 cores, a 20 fold runtime improvement may be noticed.

## Installation and execution

Create and initialize a virtual environment for instance with 
```
python3 -m venv venv
source venv/bin/activate
```

Then install the requirements for running the parallel version with
```
pip install -r requirements.txt
```

To run either version consider
```
./nanoGenA.py
```
and
```
./nanoGenA_parallel.py
```
