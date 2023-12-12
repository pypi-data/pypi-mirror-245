#!/usr/bin/env python3

from itaxotools.fitchi import compute_fitchi_tree


def test_basic():

    sequences = {
        "pop1_1": "ACAACCTTAATGG",
        "pop1_2": "ACAACCGTAAAGG",
        "pop2_1": "AATACCTTCATGG",
        "pop2_2": "ACAACCTTAATGG",
    }

    classifications = {
        "pop1_1": "pop1",
        "pop1_2": "pop1",
        "pop2_1": "pop2",
        "pop2_2": "pop2",
    }

    newick_string = "(((pop1_1,pop1_2),pop2_1),pop2_2)"

    haplo_tree = compute_fitchi_tree(sequences, classifications, newick_string)
    haplo_tree.print()

    assert "pop1_1" in haplo_tree.members
    assert "pop2_2" in haplo_tree.members
    node1, node2 = haplo_tree.children
    if node1.mutations > node2.mutations:
        node1, node2 = node2, node1
    assert node1.mutations == 2
    assert node2.mutations == 3
    assert "pop1_2" in node1.members
    assert "pop2_1" in node2.members
