def find_common_kmers(dna, k, threshold):
    result = []
    for start in range(len(dna)-k):
        kmer = dna[start:start+k]
        if dna.count(kmer) >= threshold:
            result.append(kmer)
    return result

#>>> from find_common_kmers import find_common_kmers
#>>> print(find_common_kmers('atgaatgc', 3, 2))
#>>> print(find_common_kmers('atgaatcg', 3, 2))
