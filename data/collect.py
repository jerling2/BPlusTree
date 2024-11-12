import os
import sys
import random
from time import process_time
import random


# Add parent directory to PATH
current_directory = os.path.dirname(os.path.realpath(__file__))  # pwd
parent_directory = os.path.dirname(current_directory)            # cd ..
sys.path.append(parent_directory)     


from src.bplus import *


def populate_tree(tree, size):
    for _ in range(size):
        status = False
        while not status:
            random_rid = random.randint(0, 2**40)
            status = tree.insert(random_rid, random_rid)
    return


def main():
    ID = random.randint(100000, 999999) # 6 digit number
    try:
        DEG = int(input("Enter degree of BTree <int> (default=3):"))
    except:
        DEG = 3
    try:
        ITERATIONS = int(input("Enter sample size <int> (default=20):"))
    except:
        ITERATIONS = 20
    
    out = os.path.join(current_directory, "output", f"out_deg{DEG}_avg{ITERATIONS}_id{ID}.csv")
    fp = open(out, "w")
    sys.stdout = fp

    # ELEMENTS = [2**i for i in range(1, 16)]
    ELEMENTS = [10*i for i in range(1, 500)]

    print(f"DEG={DEG}\tSample={ITERATIONS}")

    print("Elements", end="")
    for n in ELEMENTS:
        print(f"\t{n}", end="")
    print("")

    print("Gathering data for insertion...", file=sys.stderr)
    print("Insertion", end="")    
    for n in ELEMENTS:
        print(f"    n={n}..", end="", file=sys.stderr)
        avg_elapsed_time = 0
        for i in range(ITERATIONS):
            print(f".{i+1}", end="", file=sys.stderr)
            sys.stderr.flush()
            tree = BPlusTree(DEG)
            populate_tree(tree, n)
            status = False
            elapsed_time = 0
            while not status:
                random_rid = random.randint(0, 2**40)
                t0 = process_time()
                status = tree.insert(random_rid, random_rid)
                t1 = process_time()
                elapsed_time = t1 - t0
            avg_elapsed_time += elapsed_time
        avg_elapsed_time /= ITERATIONS
        print(f"\t{avg_elapsed_time}", end="")
        print("", file=sys.stderr)
    print("")
    print("", file=sys.stderr)

    print("Gathering data for deletion...", file=sys.stderr)
    print("Deletion", end="")    
    for n in ELEMENTS:
        print(f"    n={n}..", end="", file=sys.stderr)
        avg_elapsed_time = 0
        for i in range(ITERATIONS):
            print(f".{i+1}", end="", file=sys.stderr)
            sys.stderr.flush()
            tree = BPlusTree(DEG)
            populate_tree(tree, n)
            population = sorted(tree.rid_set)
            random_rid = random.sample(population, 1)[0]
            t0 = process_time()
            tree.delete(random_rid)
            t1 = process_time()
            avg_elapsed_time += t1 - t0
        avg_elapsed_time /= ITERATIONS 
        print(f"\t{avg_elapsed_time}", end="")
        print("", file=sys.stderr)
    print("")
    print("", file=sys.stderr)

    print("Gathering data for search...", file=sys.stderr)
    print("Search", end="")    
    for n in ELEMENTS:
        print(f"    n={n}..", end="", file=sys.stderr)
        avg_elapsed_time = 0
        for i in range(ITERATIONS):
            print(f".{i+1}", end="", file=sys.stderr)
            sys.stderr.flush()
            tree = BPlusTree(DEG)
            populate_tree(tree, n)
            population = sorted(tree.rid_set)
            random_rid = random.sample(population, 1)[0]
            t0 = process_time()
            tree.search(random_rid)
            t1 = process_time()
            avg_elapsed_time += t1 - t0
        avg_elapsed_time /= ITERATIONS 
        print(f"\t{avg_elapsed_time}", end="")
        print("", file=sys.stderr)
    print("")
    print("", file=sys.stderr)

    print("Gathering data for inorder...", file=sys.stderr)
    print("Inorder", end="")    
    for n in ELEMENTS:
        print(f"    n={n}..", end="", file=sys.stderr)
        avg_elapsed_time = 0
        for i in range(ITERATIONS):
            print(f".{i+1}", end="", file=sys.stderr)
            sys.stderr.flush()
            tree = BPlusTree(DEG)
            populate_tree(tree, n)
            t0 = process_time()
            tree.inorder()
            t1 = process_time()
            avg_elapsed_time += t1 - t0
        avg_elapsed_time /= ITERATIONS 
        print(f"\t{avg_elapsed_time}", end="")
        print("", file=sys.stderr)
    print("", file=sys.stderr)

    fp.close()    

if __name__ == "__main__":
    main()