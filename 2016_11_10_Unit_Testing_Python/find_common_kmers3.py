from __future__ import print_function
import sys
from collections import Counter

def find_common_kmers(dna, k, threshold):
    c = Counter([ dna[n:n+k] for n in range(len(dna) - k + 1) ])
    return [ kmer for kmer in c if c[kmer] >= threshold ]

def main():
    dna, k, threshold = sys.argv[1:]

    ofh = open("list_of_%smers.txt" % k, 'w')
    for kmer in find_common_kmers(dna, int(k), int(threshold)):
        print( kmer, file=ofh )

if __name__ == '__main__': main()
