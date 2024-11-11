import random
from bplus import *

def main():
    # tree = BPlusTree(3)
    # tree.insert(1)
    # tree.delete(1)

    SIZE = 2**15
    tree = BPlusTree(3)

    for _ in range(SIZE):
        status = False
        while not status:
            status = tree.insert(random.randint(0, 2**40))
            if status == False:
                print("Duplicate key!")
    print("Pass insertion")
    
    def test_inorder_quick(tree, size):
        inorder_quick_array = tree.inorder_quick()
        if len(inorder_quick_array) != size:
            raise Exception(f"Quick Inorder({len(inorder_quick_array)}) != {size}")
        for i in range(1, len(inorder_quick_array)):
            if inorder_quick_array[i] < inorder_quick_array[i - 1]:
                raise Exception(f"{inorder_quick_array[i]} is lesser than {inorder_quick_array[i - 1]}")
    test_inorder_quick(tree, SIZE)
    print("Pass quick inorder traversal")

    inorder_array = tree.inorder()
    if len(inorder_array) != SIZE:
        raise Exception(f"Inorder list is not the correct size")
    for i in range(1, len(inorder_array)):
        if inorder_array[i] < inorder_array[i - 1]:
            raise Exception(f"{inorder_array[i]} is lesser than {inorder_array[i - 1]}")
    print("Pass inorder traversal")

    old_size = len(tree.rid_set)
    for i in range(SIZE):
        test_inorder_quick(tree, SIZE - i)
        print(f"Passed inorder traversal: {len(tree.rid_set)}")
        population = sorted(tree.rid_set)
        random_rid = random.sample(population, 1)[0]
        if tree.delete(random_rid) == False:
            raise Exception("Couldn't find key")
        new_size = len(tree.rid_set)
        if old_size <= new_size:
            raise Exception("Deletion error")
        old_size = new_size


    print("pass deletion")
    print(tree.rid_set)

if __name__ == "__main__":
    main()