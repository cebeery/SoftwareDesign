# -*- coding: utf-8 -*-
"""
Created on Sun Feb  2 11:24:42 2014

@author: Claire E Beery
"""

# you may find it useful to import these variables (although you are not required to use them)
from amino_acids import aa, codons
import random

def collapse(L):
    """ Converts a list of strings to a string by concatenating all elements of the list """
    output = ""
    for s in L:
        output = output + s
    return output

   
def index_nested_list(element, outerList):
    """ Returns the index of the nest list which hold the desired element """
    
    for i in range(len(outerList)):
        nestedList = outerList[i]
        if element in nestedList:
            return i

def coding_strand_to_AA(dna):
    """ Computes the Protein encoded by a sequence of DNA.  This function
        does not check for start and stop codons (it assumes that the input
        DNA sequence represents an protein coding region).
        
        dna: a DNA sequence represented as a string
        returns: a string containing the sequence of amino acids encoded by the
                 the input DNA fragment
    """
    
    AA = []
    DNA = list(dna)
    
    #denotes how many codons are in the sequence
    num_codons = int(len(dna)/3) 
    
    # make a list with each entry an amino acid
    for i in range(1,num_codons + 1):
        
        #creates list of subsequent codons as i increases
        localCodon =  str( DNA[3*i - 3] ) + str( DNA[3*i -2]) + str( DNA[3*i -1] ) 
        
        #turns codons into animo acids
        indexCodon = index_nested_list(localCodon, codons)
        AA.append(aa[indexCodon])  
  
        
    aaString = collapse(AA)
    
    return aaString
    

def coding_strand_to_AA_unit_tests():
    """ Unit tests for the coding_strand_to_AA function """
        
    sample_dna = "ATGGCTAAGGAACTTATTGTTATCAACGGGTGTCGGTATAGCACGGCGCTGAGC"
    aa_of_dna = "makelivingcrystals"
    
    foundAA = coding_strand_to_AA(sample_dna)
    
    print 'input: ', sample_dna, ', expected output: ', aa_of_dna, ', actual output: ', foundAA
    
def get_reverse_complement(dna):
    """ Computes the reverse complementary sequence of DNA for the specfied DNA
        sequence
    
        dna: a DNA sequence represented as a string
        returns: the reverse complementary DNA sequence represented as a string
    """
    
    DNA = list(dna) 
    
    
    for i in range(len(dna)):
        # Adenine and Thymine are complimentary nucleotides
        if DNA[i] == 'T':
            DNA[i] = 'A'
        elif DNA[i] == 'A':
            DNA[i] = 'T'
        # Cytosine and Guanine are complimentary nucleotides
        elif DNA[i] == 'C':
            DNA[i] = 'G' 
        elif DNA[i] == 'G':
            DNA[i] = 'C'
            
    return collapse(DNA)
    
    
def get_reverse_complement_unit_tests():
    """ Unit tests for the get_complement function """
        
    sample_dna = "GTACTAATTCG"    
    reverse_dna = "CATGATTAAGC"
    
    found_dna = get_reverse_complement(sample_dna)
    
    print 'input: ', sample_dna, ', expected output: ', reverse_dna, ', actual output: ', found_dna

def rest_of_ORF(dna):
    """ Takes a DNA sequence that is assumed to begin with a start codon and returns
        the sequence up to but not including the first in frame stop codon.  If there
        is no in frame stop codon, returns the whole string.
        
        dna: a DNA sequence
        returns: the open reading frame represented as a string
    """
    
    ORF = []
    DNA = list(dna)
    
    # denotes location of stop codons
    stopList = codons[10]
    
    #denotes how many codons are in the sequence
    num_codons = int(len(dna)/3) 
    
    # make a list with each entry a codon until a stop codon is found 
    for i in range(1,num_codons + 1):
        
        #creates list of subsequent codons as i increases
        localCodon =  str( DNA[3*i - 3] ) + str( DNA[3*i -2]) + str( DNA[3*i -1] ) 
        
        # stops adding codons if stop codon is reached
        if localCodon in stopList:
            break;
        
        ORF.append(localCodon)
    
    # return entire sequence if no stop codon is found
    else:
        return dna
        
    # returns codons up to the break triggering  
    return collapse(ORF)
    
    

def rest_of_ORF_unit_tests():
    """ Unit tests for the rest_of_ORF function """
    
    sample1 = "ATGTACGATTAGGCTA"   
    exp1 = "ATGTACGAT"
    
    sample2 = "ATGATACCATCGTTGCATG"
    exp2 = "ATGATACCATCGTTGCATG"
    
    found_dna1 = rest_of_ORF(sample1)
    found_dna2 = rest_of_ORF(sample2)
    
    print 'input: ', sample1, ', expected output: ', exp1, ', actual output: ', found_dna1
    print 'input: ', sample2, ', expected output: ', exp2, ', actual output: ', found_dna2
        
def find_all_ORFs_oneframe(dna):
    """ Finds all non-nested open reading frames in the given DNA sequence and returns
        them as a list.  This function should only find ORFs that are in the default
        frame of the sequence (i.e. they start on indices that are multiples of 3).
        By non-nested we mean that if an ORF occurs entirely within
        another ORF, it should not be included in the returned list of ORFs.
        
        dna: a DNA sequence
        returns: a list of non-nested ORFs
    """
    
    ORF = []
    in_ORF = False #used to avoid nested ORF
    DNA = list(dna)
    
    # denotes location of stop/start codons
    startList = codons[3]
    stopList = codons[10]
    
    #denotes how many codons are in the sequence
    num_codons = int(len(dna)/3) 
    
    
    for i in range(1,num_codons + 1):
        
        # notes next codon in sequence
        localCodon =  str( DNA[3*i -3] ) + str( DNA[3*i -2]) + str( DNA[3*i -1] ) 
                
        # checks if current codon is in open ref frame
        if (in_ORF) and (localCodon in stopList):
            in_ORF = False #allows new ORF to be found
        elif (in_ORF != True) and (localCodon in startList):
            in_ORF = True #stops code from reading nested ORFs          
            
            #find ORF extreme
            listToEnd = list(DNA[(3*i-3):])
            strToEnd = collapse(listToEnd)
            newORF = rest_of_ORF(strToEnd) 
            
            ORF.append(newORF)
            
    return ORF
     
def find_all_ORFs_oneframe_unit_tests():
    """ Unit tests for the find_all_ORFs_oneframe function """
    sample_dna = "GTAATGTTTATGGGGTAGCTAATGTAAATGTCGAAA"    
    ORFs = ['ATGTTTATGGGG','ATG','ATGTCGAAA']
    
    found_ORFs = find_all_ORFs_oneframe(sample_dna)
    
    print 'input: ', sample_dna, ', expected output: ', ORFs, ', actual output: ', found_ORFs

def find_all_ORFs(dna):
    """ Finds all non-nested open reading frames in the given DNA sequence in all 3
        possible frames and returns them as a list.  By non-nested we mean that if an
        ORF occurs entirely within another ORF and they are both in the same frame,
        it should not be included in the returned list of ORFs.
        
        dna: a DNA sequence
        returns: a list of non-nested ORFs
    """
    
    ORFs = []
    DNA = list(dna)
    
    for i in [0,1,2]:
        newDNA = collapse(list(DNA[i:]))
        ORFs.extend(find_all_ORFs_oneframe(newDNA))
     
    return ORFs

def find_all_ORFs_unit_tests():
    """ Unit tests for the find_all_ORFs function """
    sample_dna = "GTAATGTTTATGGGGTAGCTAATGTAAATGTCATG"    
    ORFs = ['ATGTTTATGGGG','ATG','ATGTCG','ATG']
    
    found_ORFs = find_all_ORFs(sample_dna)
    
    print 'input: ', sample_dna, ', expected output: ', ORFs, ', actual output: ', found_ORFs

def find_all_ORFs_both_strands(dna):
    """ Finds all non-nested open reading frames in the given DNA sequence on both
        strands.
        
        dna: a DNA sequence
        returns: a list of non-nested ORFs
    """
    
    ORF = find_all_ORFs(dna) 
    rev = get_reverse_complement(dna)
    ORF.extend(find_all_ORFs(rev))
    
    return ORF
    

def find_all_ORFs_both_strands_unit_tests():
    """ Unit tests for the find_all_ORFs_both_strands function """

    sample_dna = "ATGCGTTAAATTACACCATGATC"    
    ORFs = ['ATGCGT', 'ATGATC', 'ATGTGGTAC']
    
    found_ORFs = find_all_ORFs_both_strands(sample_dna)
    
    print 'input: ', sample_dna, ', expected output: ', ORFs, ', actual output: ', found_ORFs

def longest_ORF(dna):
    """ Finds the longest ORF on both strands of the specified DNA and returns it
        as a string"""

    return max(find_all_ORFs_both_strands(dna), key=len)
    

def longest_ORF_unit_tests():
    """ Unit tests for the longest_ORF function """

    sample_dna = "ATGCGTTAAATTACACCATGATC"    
    ORF = 'ATGTGGTAC'
    
    found_ORFs = longest_ORF(sample_dna)
    
    print 'input: ', sample_dna, ', expected output: ', ORF, ', actual output: ', found_ORFs

def longest_ORF_noncoding(dna, num_trials):
    """ Computes the maximum length of the longest ORF over num_trials shuffles
        of the specfied DNA sequence
        
        dna: a DNA sequence
        num_trials: the number of random shuffles
        returns: the maximum length longest ORF """
    ORF = []    

    DNA = list(dna) 
    for i in range(num_trials):
        random.shuffle(DNA)
        randDNA = collapse(DNA) 
        singORF = longest_ORF(randDNA)
        ORF.append(singORF)
    
    return len(max(ORF, key=len))
         

def gene_finder(dna, threshold):
    """ Returns the amino acid sequences coded by all genes that have an ORF
        larger than the specified threshold.
        
        dna: a DNA sequence
        threshold: the minimum length of the ORF for it to be considered a valid
                   gene.
        returns: a list of all amino acid sequences whose ORFs meet the minimum
                 length specified.
    """

    ORFs = find_all_ORFs_both_strands(dna) 
    num_ORFs = int(len(ORFs))
    AA = []  
    
    for i in range(num_ORFs):
        if len(ORFs[i]) >= threshold:            
            AA.append(coding_strand_to_AA(ORFs[i]))
            
    return AA
    