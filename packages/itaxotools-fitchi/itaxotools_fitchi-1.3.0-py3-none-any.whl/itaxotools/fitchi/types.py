from __future__ import annotations

from collections import Counter
from sys import stdout


class HaploNode:
    """
    Simplified datatype for the Haplotype genealogy graph produced by Fitchi.
    The tree hierarchy is contained in `self.parent` and `self.children`.
    The distance between a node and its parent is `self.mutations`.
    """

    def __init__(self, id):
        self.id = id
        self.children = []
        self.parent = None
        self.mutations = 0
        self.pops = Counter()
        self.members = set[str]()

    def add_child(self, node: HaploNode, mutations: int = 0):
        self.children.append(node)
        node.mutations = mutations
        node.parent = self

    def add_pops(self, pops: list[str]):
        self.pops.update(pops)

    def add_members(self, members: iter[str]):
        self.members.update([member for member in members])

    def get_size(self):
        if self.pops:
            return self.pops.total()
        if self.members:
            return len(self.members)
        return 0

    def __str__(self):
        total = self.pops.total()
        per_pop_strings = (f'{v} \u00D7 {k}' for k, v in self.pops.items())
        all_pops_string = ' + '.join(per_pop_strings)
        members_string = ', '.join(self.members)
        return f"<{self.id}: {total} = {all_pops_string}; {members_string}>"

    def print(self, level=0, length=5, file=stdout):
        mutations_string = str(self.mutations).center(length, '\u2500')
        decoration = ' ' * (length+1) * (level - 1) + f"\u2514{mutations_string}" if level else ''
        print(f"{decoration}{str(self)}", file=file)
        for child in self.children:
            child.print(level + 1, length, file)
