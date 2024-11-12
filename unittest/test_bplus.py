import os
import sys
import unittest
import random
from time import process_time
from random import choice, randrange

# Add parent directory to PATH
current_directory = os.path.dirname(os.path.realpath(__file__))  # pwd
parent_directory = os.path.dirname(current_directory)            # cd ..
sys.path.append(parent_directory)     

from src.bplus import *

class Test(unittest.TestCase):

    def setUp(self):
        self.out = os.path.join(current_directory, "output", "out.txt")
        self.tree = BPlusTree(3)
        self.size = 2**10

    def test_bplus_tree(self):
        fp = open(self.out, "w")
        sys.stdout = fp
        sys.stderr = fp
        print(f"Test inserting {self.size} elements into the BTree...", end="")        
        for _ in range(self.size):
            status = False
            while not status:
                random_rid = random.randint(0, 2**40)
                status = self.tree.insert(random_rid, random_rid)
        self.assertEqual(len(self.tree.rid_set), self.size)
        print("PASS")

        print(f"Test inorder list of BTree...", end="")
        inorder = self.tree.inorder()
        self.assertEqual(len(inorder), self.size)
        for i in range(1, self.size):
            self.assertGreater(inorder[i], inorder[i-1])
        print("PASS")

        print(f"Test deleting/searching {self.size} elements in the Btree...")
        old_size = len(self.tree.rid_set)
        for i in range(self.size):
            population = sorted(self.tree.rid_set)
            random_rid = random.sample(population, 1)[0]
            self.assertEqual(self.tree.search(random_rid), random_rid)
            self.assertTrue(self.tree.delete(random_rid))
            new_size = len(self.tree.rid_set)
            self.assertGreater(old_size, new_size)
            old_size = new_size
        print("PASS")
        fp.close()

if __name__ == '__main__':
    unittest.main()