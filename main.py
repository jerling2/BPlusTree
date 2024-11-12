import random
from bplus import *

def main():
    SIZE = 2**15
    tree = BPlusTree(3)

    for _ in range(SIZE):
        status = False
        while not status:
            r = random.randint(0, 2**40)
            status = tree.insert(r, r)
            if status == False:
                print("Duplicate key!")
    print("Pass insertion")
    
    def test_inorder(tree, size):
        inorder_quick_array = tree.inorder()
        if len(inorder_quick_array) != size:
            raise Exception(f"Inorder({len(inorder_quick_array)}) != {size}")
        for i in range(1, len(inorder_quick_array)):
            if inorder_quick_array[i] < inorder_quick_array[i - 1]:
                raise Exception(f"{inorder_quick_array[i]} is lesser than {inorder_quick_array[i - 1]}")
    test_inorder(tree, SIZE)
    print("Pass quick inorder traversal")

    inorder_array = tree.inorder_slow()
    if len(inorder_array) != SIZE:
        raise Exception(f"Slow inorder list is not the correct size")
    for i in range(1, len(inorder_array)):
        if inorder_array[i] < inorder_array[i - 1]:
            raise Exception(f"{inorder_array[i]} is lesser than {inorder_array[i - 1]}")
    print("Pass inorder_slow traversal")

    
    old_size = len(tree.rid_set)
    for i in range(SIZE):
        test_inorder(tree, SIZE - i)
        population = sorted(tree.rid_set)
        random_rid = random.sample(population, 1)[0]
        if tree.search(r) != r:
            raise Exception("Search failed!")
        if tree.delete(random_rid) == False:
            raise Exception("Couldn't find key")
        new_size = len(tree.rid_set)
        if old_size <= new_size:
            raise Exception("Deletion error")
        old_size = new_size

    print("pass deletion and search")
    print(tree.rid_set)

if __name__ == "__main__":
    main()