import math

NOT_FOUND = -1
RID_INDEX = 0
PTR_INDEX = 1

class BPlusNode():
    def __init__(self, is_leaf=True) -> None:
        self.parent = None
        self.is_leaf = is_leaf
        self.size = 0
        self.children = [self.nodeify(float('inf'), None)]
        self.next = None
        self.prev = None

    def nodeify(self, value, ptr):
        """ This Defines the Schema of a BPlusNode. """
        return [value, ptr]

    def add(self, value, ptr=None):
        self.children.append(self.nodeify(value, ptr))
        self.children.sort(key=lambda x: x[0])                   # Sort by rid.
        self.size += 1                                        # The node grows!
        return None 

    def pop(self, index=0):
        self.children.pop(index)
        self.size -= 1                                      # The node shrinks!
        return None 

    def get_index_of(self, search_key):
        if isinstance(search_key, BPlusNode):
            search_index = PTR_INDEX     # We are searching by using BPlusNode.
        else:
            search_index = RID_INDEX     # We are searching by using rid <int>.
        for i, child in enumerate(self.children):
            if search_key == child[search_index]:
                return i               # Return index where we found the match.
        return NOT_FOUND
    
    def get_siblings(self):
        result = [None, None]
        if not self.parent:                           # No parent, no siblings.
            return result
        ptr = self.parent.get_index_of(self)
        if ptr - 1 >= 0:                 # Ptr arithmetic to find the lsibling.
            result[0] = self.parent.children[ptr - 1][PTR_INDEX]
        if ptr + 1 <= self.parent.size:  # Ptr arithmetic to find the rsibling.
            result[1] = self.parent.children[ptr + 1][PTR_INDEX]
        return result

    def get_max(self, mode: str):
        if mode == "r": # Return the max rid which is the second to last child.
            return self.children[-2][RID_INDEX] 
        if mode == "p":     # Return the max BPlusNode which is the last child.
            return self.children[-1][PTR_INDEX]
        raise Exception("Invalid mode")
    
    def get_min(self, mode: str):
        if mode == "r":          # Return the min rid which is the first child.
            return self.children[0][RID_INDEX]
        if mode == "p":    # Return the min BPlusNode which is the first child.
            return self.children[0][PTR_INDEX]
        raise Exception("Invalid mode")

    # ----------------------------------------------------------------------- #
    #                             NODE DEV TOOLS                              #
    # ----------------------------------------------------------------------- #

    def __repr__(self) -> str:
        if self.is_leaf:
            return self.__leaf_repr__()
        string = f"BPlusNode("
        string += str(self.children[0][RID_INDEX])
        for child in self.children[1:]:
            string += f", {child[RID_INDEX]}"
        string += ")"
        return string
    
    def __leaf_repr__(self) -> str:
        string = "BPlusNode(["
        string += str(self.children[0][RID_INDEX]) + ", "
        string += str(self.children[0][PTR_INDEX]) + "]"
        for child in self.children[1:self.size]:
            string += f", [{child[RID_INDEX]}, "
            string += f"{child[PTR_INDEX]}]"
        string += ")"
        return string


class BPlusTree():
    def __init__(self, deg) -> None:
        self.rid_set = set()
        self.deg = deg
        self.min_node_size = math.ceil(deg / 2) - 1
        self.root = None

    def insert(self, rid, data=True):
        if rid in self.rid_set:           # Check if rid already exist in tree.
            return False
        self.rid_set.add(rid)
        self.root = self.root or BPlusNode()
        leaf, _ = self.find_nodes(rid)   # Find a leaf that to contain the rid.
        leaf.add(rid, data)                     # Add rid and data to the leaf.
        if leaf.size == self.deg:            # Check if leaf has too many keys.
            self.split(leaf)           # Split leaf (propogates split upwards).
        return True

    def split(self, node):
        if not node.parent:       # Make a parent if this node didn't have one.
            node.parent = BPlusNode(is_leaf=False)    
            node.parent.children[0][PTR_INDEX] = node    
        if node == self.root:
            self.root = node.parent              # Grow the height of the tree.
        lchild = BPlusNode(is_leaf=node.is_leaf)       # Create a left sibling.
        lchild.parent = node.parent
        if node.is_leaf and node.prev:          # (1) Link leaf nodes together.
            lchild.prev = node.prev
            node.prev.next = lchild
        if node.is_leaf:                        # (2) Link leaf nodes together.
            lchild.next = node
            node.prev = lchild
        self.rotate(node, lchild)    # Shuffle keys around to balance the tree.
        if node.parent.size == self.deg:
            self.split(node.parent)                  # Propogate split upwards.
        return None
    
    def rotate(self, node, lchild):
        mid = node.size // 2 
        mrid, mchild = node.children[mid]
        node.parent.add(mrid, lchild)
        for child in node.children[0:mid]:   # mv half the nodes to the lchild.
            lchild.add(child[RID_INDEX], child[PTR_INDEX])
            node.pop()
        if not node.is_leaf:               # Check if node is an internal node.
            node.pop()                                 # Pop ref. to min child.
            lchild.children[-1][PTR_INDEX] = mchild   # lchild inherits mchild.
            lchild.children[-1][PTR_INDEX].parent = lchild     # Update parent.
            for child in lchild.children:      # Attach children to new parent.
                if child[PTR_INDEX]:
                    child[PTR_INDEX].parent = lchild           # Update parent.
        return None

    def delete(self, rid):
        if not self.root:                             # Check if tree is empty.
            return False
        if rid not in self.rid_set:               # Check if rid exist in tree.
            return False
        node, inode = self.find_nodes(rid)    # These nodes might have the rid.
        rid_index = node.get_index_of(rid) 
        if rid_index == -1:                          # Check if rid is in node.
            raise Exception("Rid not found where it was supposed to be.")
        node.pop(rid_index)                  # Remove the record from the tree.
        self.rid_set.remove(rid)
        self.merge_leaf(rid, node, inode)               # restructure the tree.
        return True

    def merge_leaf(self, rid, node, inode):
        if node is self.root and node.size == 0:      # Check if tree is empty.
            self.root = None
            return
        if node is self.root:
            return
        if not inode and node.size >= self.min_node_size:      # Simple delete.
            return
        if node.size >= self.min_node_size:             # Almost simple delete.
            k = inode.get_index_of(rid)
            inode.children[k][RID_INDEX] = node.get_min("r")
            return
        p = node.parent
        ls, rs = node.get_siblings() 
        if ls and ls.size > self.min_node_size:        # Case I: steal from ls.
            srid = ls.get_max("r")                   # "Stolen" ls' node's rid.
            sdat = ls.get_max("p")                  # "Stolen" ls' node's data.
            ls.pop(-2)                          # Pop(-2) to pop maximum child.
            node.add(srid, sdat)
        elif rs and rs.size > self.min_node_size:     # Case II: steal from rs.
            srid = rs.get_min("r")                   # "Stolen" rs' node's rid.
            sdat = rs.get_min("p")
            rs.pop()                              # Pop() to pop minimum child.
            node.add(srid, sdat)
            k = p.get_index_of(node)
            p.children[k][RID_INDEX] = rs.get_min("r")  # Update key in parent.
        elif ls:                                     # Case III: merge with ls.
            for i in range(ls.size):             # cp children from ls to node.
                node.add(ls.children[i][RID_INDEX], ls.children[i][PTR_INDEX])
            node.prev = ls.prev                  # Detach ls from other leaves.
            if node.prev:                         
                node.prev.next = node            # Detach ls from other leaves.
            k = p.get_index_of(ls)
            p.pop(k)                                   # Detach ls from parent.
        elif rs:                                      # Case IV: merge with rs.
            for i in range(rs.size):             # cp children from rs to node.
                node.add(rs.children[i][RID_INDEX], rs.children[i][PTR_INDEX])
            node.next = rs.next                  # Detach rs from other leaves.
            if node.next:
                node.next.prev = node            # Detach rs from other leaves.
            node_index = p.get_index_of(node) 
            srid = p.children[node_index + 1][RID_INDEX] # Steal rs search rid.
            p.children[node_index][RID_INDEX] = srid       # Update parent rid.
            p.pop(node_index + 1)        # Remove connection from parent to rs.
        else:
            raise Exception("Leaf does not have any siblings")
        if inode and inode.get_index_of(rid) != NOT_FOUND: # Complicated sorry.
            k = inode.get_index_of(rid)
            inode.children[k][RID_INDEX] = node.get_min("r")
        return self.merge_internal(p)

    def merge_internal(self, node):
        if node == self.root and node.size == 0:      # Check if root is empty.
            self.root = node.children[0][PTR_INDEX]
            return
        if node == self.root:        # Ignore root (as long as it's not empty).
            return
        if node.size >= self.min_node_size:     # Pass if node is large enough.
            return
        p = node.parent
        ls, rs = node.get_siblings() 
        if ls and ls.size > self.min_node_size:        # Case I: steal from ls.
            ls_index = p.get_index_of(ls)
            prid = p.children[ls_index][RID_INDEX]         # Demote parent rid.
            lschild = ls.get_max("p")                    # Steal child from ls.
            node.add(prid, lschild)          # Node inherits (rid, child) pair.
            lschild.parent = node # Make sure stolen child knows its new daddy.
            lsrid = ls.get_max("r")
            p.children[ls_index][RID_INDEX] = lsrid       # Promote ls max rid.
            ls.pop(-1)                # Pop -1 on internal node to pop max key.
            ls.children[-1][RID_INDEX] = float('inf')  # 'inf' for new max key.
        elif rs and rs.size > self.min_node_size:     # Case II: steal from rs.
            n_index = p.get_index_of(node)
            prid = p.children[n_index][RID_INDEX] 
            node.children[-1][RID_INDEX] = prid            # Demote parent rid.
            rschild = rs.get_min("p")                      
            node.add(float('inf'), rschild)              # Steal child from rs.
            rschild.parent = node                      # Update child's parent.
            rsrid = rs.get_min("r") 
            p.children[n_index][RID_INDEX] = rsrid        # Promote rs min rid.
            rs.pop()                                     # Remove rs min child.
        elif ls:                                     # Case III: merge with ls.
            ls_index = p.get_index_of(ls)
            prid = p.children[ls_index][RID_INDEX]
            ls.children[-1][RID_INDEX] = prid        # Demote parent rid to ls.
            p.pop(ls_index)                                # Remove ref. to ls.
            for i in range(ls.size + 1):         # cp children from ls to node.
                node.add(ls.children[i][RID_INDEX], ls.children[i][PTR_INDEX])
                if ls.children[i][PTR_INDEX]:
                    ls.children[i][PTR_INDEX].parent = node # Update child's p.
        else:                                         # Case VI: merge with rs.
            n_index = p.get_index_of(node)
            prid = p.children[n_index][RID_INDEX]
            node.children[-1][RID_INDEX] = prid    # Demote parent rid to node.
            rs_index = p.get_index_of(rs)
            p.children[rs_index][PTR_INDEX] = node    # node become the rchild. 
            p.pop(n_index)                    # remove ref. to parent's lchild.
            for i in range(rs.size + 1):         # cp children from rs to node.
                node.add(rs.children[i][RID_INDEX], rs.children[i][PTR_INDEX])
                if rs.children[i][PTR_INDEX]:
                    rs.children[i][PTR_INDEX].parent = node # Update child's p.
        return self.merge_internal(p)
    
    def search(self, rid):
        node, _ = self.find_nodes(rid)
        k = node.get_index_of(rid)
        return node.children[k][PTR_INDEX] # TODO: This should be a DATA_INDEX.

    def find_nodes(self, rid):
        if not self.root:                             # Check if tree is empty.
            return (None, None)
        node = self.root
        inode = None
        while not node.is_leaf:     # Traverse down the tree to the right leaf.
            for i in range(node.size + 1):
                if rid < node.children[i][RID_INDEX]:
                    node = node.children[i][PTR_INDEX]        # Follow the ptr.
                    break 
                if rid == node.children[i][RID_INDEX]:
                    inode = node  # Inode has the target rid, but isn't a leaf.
        return (node, inode)

    def inorder(self):
        if not self.root:                             # Check if tree is empty.
            return []
        result = []
        node = self.root                                       # Start at root.
        while not node.is_leaf:          # Traverse to the very left leaf node.
            node = node.children[0][PTR_INDEX]
        while node is not None:             # Use next ptr to get inorder list.
            for i in range(node.size):
                result.append(node.children[i][RID_INDEX])
            node = node.next
        return result

    # ----------------------------------------------------------------------- #
    #                             TREE DEV TOOLS                              #
    # ----------------------------------------------------------------------- #

    def inorder_slow(self):
        if not self.root:
            return []
        queue = [self.root]
        result = []
        while queue:
            node = queue.pop(0)
            for child in node.children:
                if isinstance(child[PTR_INDEX], BPlusNode):
                    queue.append(child[PTR_INDEX])
                elif child[RID_INDEX] != float('inf'):
                    result.append(child[RID_INDEX])
        return result

    def __repr__(self) -> str:
        if not self.root:
            return "BPlusTree: <empty>"
        level = 0
        string = "-~ BPlusTree ~-\n"
        string += "\t" * level + f"Level {level}: "
        string += repr(self.root)
        queue = [(c[PTR_INDEX], level + 1) for c in self.root.children]
        while queue:
            node, l = queue.pop(0)
            if not isinstance(node, BPlusNode):
                continue
            for c in node.children:
                queue.append((c[PTR_INDEX], l + 1))
            if l > level:
                level = l
                string += "\n" + f"Level {level}: {node}"
            else:
                string += ", " + repr(node)
        return string