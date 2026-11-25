class Node:
    def __init__(self, patient_id, patient_name):
        self.patient_id = patient_id
        self.patient_name = patient_name
        self.left = None
        self.right = None


class BST:
    def __init__(self):
        self.root = None
        self.comparisons = 0

    def insert(self, patient_id, patient_name):
        new_node = Node(patient_id, patient_name)

        if self.root is None:
            self.root = new_node
            return

        current = self.root

        while True:
            self.comparisons += 1

            if patient_id < current.patient_id:
                if current.left is None:
                    current.left = new_node
                    return
                current = current.left

            elif patient_id > current.patient_id:
                if current.right is None:
                    current.right = new_node
                    return
                current = current.right

            else:
                current.patient_name = patient_name
                return


    def search(self, patient_id):
        current = self.root

        while current is not None:
            self.comparisons += 1

            if patient_id == current.patient_id:
                return current.patient_name

            elif patient_id < current.patient_id:
                current = current.left

            else:
                current = current.right

        return None

    
    def delete(self, patient_id):
        self.root = self._delete(self.root, patient_id)

    def _delete(self, node, patient_id):
        if node is None:
            return None

        self.comparisons += 1

        if patient_id < node.patient_id:
            node.left = self._delete(node.left, patient_id)

        elif patient_id > node.patient_id:
            node.right = self._delete(node.right, patient_id)

        else:
            # Case 1: No child
            if node.left is None and node.right is None:
                return None

            # Case 2: One child
            elif node.left is None:
                return node.right

            elif node.right is None:
                return node.left

            # Case 3: Two children
            successor = self._min_value_node(node.right)

            node.patient_id = successor.patient_id
            node.patient_name = successor.patient_name

            node.right = self._delete(
                node.right, successor.patient_id
            )

        return node

    def _min_value_node(self, node):
        current = node

        while current.left is not None:
            current = current.left

        return current


    def inorder(self, node):
        if node is not None:
            self.inorder(node.left)
            print(node.patient_id, "-", node.patient_name)
            self.inorder(node.right)


    def height(self, node):
        if node is None:
            return -1

        left_height = self.height(node.left)
        right_height = self.height(node.right)

        return 1 + max(left_height, right_height)


if __name__ == "__main__":

    tree3 = BST()

    tree3.insert(50, "Alice")
    tree3.insert(30, "Bob")
    tree3.insert(20, "Charlie")

    print("\nBefore deleting 30:")
    tree3.inorder(tree3.root)

    tree3.delete(30)

    print("\nAfter deleting 30:")
    tree3.inorder(tree3.root)