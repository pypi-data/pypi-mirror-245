#!/usr/bin/env python3

from itaxotools.fitchi import compute_fitchi_tree

sequences = {

    'pop1_1': 'ACAACCTTAATGG',
    'pop1_2': 'ACAACCGTAAAGG',
    'pop1_3': 'AATACATTCATGG',
    'pop1_4': 'GCAACCTTAATTG',
    'pop1_5': 'ACAACCGTAAAGG',
    'pop1_6': 'GCAACCTGAATGG',
    'pop1_7': 'GCAACCTGAATGG',
    'pop1_8': 'AATACCTTCATGG',
    'pop1_9': 'GCAACCTTAATGG',
    'pop1_10': 'ACAACCTTAATGG',
    'pop1_11': 'GCAACCTGAATGG',
    'pop1_12': 'GCAACCTGAATGG',
    'pop1_13': 'GCAACCTTACTGG',
    'pop1_14': 'AATACATTCATGG',
    'pop1_15': 'AATACCTTCATGG',
    'pop2_1': 'AATACCTTCATGG',
    'pop2_2': 'ACAACCTTAATGG',
    'pop2_3': 'AATACCTTCATGG',
    'pop2_4': 'ACACCCTTAATGG',
    'pop2_5': 'ACAACCTTAATGG',
    'pop2_6': 'AATAGCTTCATGG',
    'pop2_7': 'AATACCTTCATGG',
    'pop2_8': 'AATAGCTTCATGG',
    'pop2_9': 'ACACCCTTAATGG',
    'pop2_10': 'AATACCTTCATGG',
    'pop2_11': 'ACAACCTTAATGG',
    'pop2_12': 'ACACCCTTAATGG',
    'pop2_13': 'AATACCTTCATGG',
    'pop2_14': 'AATACCTTCATGG',
    'pop2_15': 'ACAACCTTAATGC',

}

classifications = {

    'pop1_1': 'pop1',
    'pop1_2': 'pop1',
    'pop1_3': 'pop1',
    'pop1_4': 'pop1',
    'pop1_5': 'pop1',
    'pop1_6': 'pop1',
    'pop1_7': 'pop1',
    'pop1_8': 'pop1',
    'pop1_9': 'pop1',
    'pop1_10': 'pop1',
    'pop1_11': 'pop1',
    'pop1_12': 'pop1',
    'pop1_13': 'pop1',
    'pop1_14': 'pop1',
    'pop1_15': 'pop1',
    'pop2_1': 'pop2',
    'pop2_2': 'pop2',
    'pop2_3': 'pop2',
    'pop2_4': 'pop2',
    'pop2_5': 'pop2',
    'pop2_6': 'pop2',
    'pop2_7': 'pop2',
    'pop2_8': 'pop2',
    'pop2_9': 'pop2',
    'pop2_10': 'pop2',
    'pop2_11': 'pop2',
    'pop2_12': 'pop2',
    'pop2_13': 'pop2',
    'pop2_14': 'pop2',
    'pop2_15': 'pop2',

}

newick_string = '(((pop2_11,(pop2_2,pop2_5)),((((pop1_3,pop1_14),((pop2_6,pop2_8),(((pop2_7,(pop2_13,((pop2_3,pop2_10),(pop1_15,pop1_8)))),pop2_1),pop2_14))),(pop1_13,((pop1_4,(((pop1_11,pop1_7),pop1_12),pop1_6)),pop1_9))),(pop2_15,((pop2_4,(pop2_9,pop2_12)),(pop1_2,pop1_5))))),pop1_10,pop1_1)'


if __name__ == '__main__':

    haplo_tree = compute_fitchi_tree(sequences, classifications, newick_string)
    haplo_tree.print()
