class AVLNode:
    def __init__(self, patient_id, patient_name):
        self.patient_id = patient_id
        self.patient_name = patient_name
        self.left = None
        self.right = None
        self.height = 0

class AVL:
    def __init__(self):
        self.root = None
        self.comparisons = 0
        self.rotations = 0

    def get_height(self, node):
        if node is None:
            return -1
        return node.height

    def get_balance(self, node):
        if node is None:
            return 0

        return (
            self.get_height(node.left)
            - self.get_height(node.right)
        )

    def update_height(self, node):
        node.height = 1 + max(
            self.get_height(node.left),
            self.get_height(node.right)
        )

    def right_rotate(self, y):
        x = y.left
        T2 = x.right

        x.right = y
        y.left = T2

        self.update_height(y)
        self.update_height(x)

        self.rotations += 1

        return x

    def left_rotate(self, x):
        y = x.right
        T2 = y.left

        y.left = x
        x.right = T2

        self.update_height(x)
        self.update_height(y)

        self.rotations += 1

        return y

    def left_right_rotate(self, node):
        node.left = self.left_rotate(node.left)
        return self.right_rotate(node)

    def right_left_rotate(self, node):
        node.right = self.right_rotate(node.right)
        return self.left_rotate(node)


    def insert(self, patient_id, patient_name):
        self.root = self._insert(
            self.root, patient_id, patient_name
        )

    def _insert(self, node, patient_id, patient_name):

        # Normal BST insertion
        if node is None:
            return AVLNode(patient_id, patient_name)

        self.comparisons += 1

        if patient_id < node.patient_id:
            node.left = self._insert(
                node.left, patient_id, patient_name
            )

        elif patient_id > node.patient_id:
            node.right = self._insert(
                node.right, patient_id, patient_name
            )

        else:
            node.patient_name = patient_name
            return node

        # Update height
        self.update_height(node)

        # Calculate balance factor
        balance = self.get_balance(node)

        # Case 1: LL
        if balance > 1 and patient_id < node.left.patient_id:
            return self.right_rotate(node)

        # Case 2: RR
        if balance < -1 and patient_id > node.right.patient_id:
            return self.left_rotate(node)

        # Case 3: LR
        if balance > 1 and patient_id > node.left.patient_id:
            return self.left_right_rotate(node)

        # Case 4: RL
        if balance < -1 and patient_id < node.right.patient_id:
            return self.right_left_rotate(node)

        return node
    
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

    def inorder(self, node):
        if node is not None:
            self.inorder(node.left)
            print(node.patient_id, "-", node.patient_name)
            self.inorder(node.right)

    
    def min_value_node(self, node):
        current = node

        while current.left is not None:
            current = current.left

        return current

    def delete(self, patient_id):
        self.root = self._delete(self.root, patient_id)

    def _delete(self, node, patient_id):

        if node is None:
            return None

        self.comparisons += 1

        # Search for the node
        if patient_id < node.patient_id:
            node.left = self._delete(node.left, patient_id)

        elif patient_id > node.patient_id:
            node.right = self._delete(node.right, patient_id)

        else:
            # Case 1 and 2: Zero or one child
            if node.left is None:
                return node.right

            elif node.right is None:
                return node.left

            # Case 3: Two children
            successor = self.min_value_node(node.right)

            node.patient_id = successor.patient_id
            node.patient_name = successor.patient_name

            node.right = self._delete(
                node.right, successor.patient_id
            )

        # If the node was a leaf
        if node is None:
            return None

        # Update height
        self.update_height(node)

        # Calculate balance factor
        balance = self.get_balance(node)

        # Case 1: LL
        if balance > 1 and self.get_balance(node.left) >= 0:
            return self.right_rotate(node)

        # Case 2: LR
        if balance > 1 and self.get_balance(node.left) < 0:
            return self.left_right_rotate(node)

        # Case 3: RR
        if balance < -1 and self.get_balance(node.right) <= 0:
            return self.left_rotate(node)

        # Case 4: RL
        if balance < -1 and self.get_balance(node.right) > 0:
            return self.right_left_rotate(node)

        return node

    def is_balanced(self):
        def check(node):
            if node is None:
                return True, -1

            left_balanced, left_height = check(node.left)
            right_balanced, right_height = check(node.right)

            actual_height = 1 + max(
                left_height, right_height
            )

            balance = left_height - right_height

            balanced = (
                left_balanced
                and right_balanced
                and abs(balance) <= 1
                and node.height == actual_height
            )

            return balanced, actual_height

        return check(self.root)[0]

    def is_bst(self):
        def check(node, min_value, max_value):
            if node is None:
                return True

            if min_value is not None and node.patient_id <= min_value:
                return False

            if max_value is not None and node.patient_id >= max_value:
                return False

            return (
                check(node.left, min_value, node.patient_id)
                and
                check(node.right, node.patient_id, max_value)
            )

        return check(self.root, None, None)


if __name__ == "__main__":
    tree = AVL()

    values = [
        (10, "Alice"),
        (20, "Bob"),
        (30, "Charlie"),
        (40, "David"),
        (50, "Eva"),
        (25, "Frank")
    ]

    for patient_id, name in values:
        tree.insert(patient_id, name)

    print("Before Deletion:")
    print("Root:", tree.root.patient_id)
    print("Height:", tree.root.height)

    tree.delete(25)

    print("\nAfter Deleting Patient ID 25:")
    print("Root:", tree.root.patient_id)
    print("Height:", tree.root.height)

    print("\nIn-order Traversal:")
    tree.inorder(tree.root)

    print("\nSearch Patient ID 25:", tree.search(25))


    print("\nValidation:")
    print("Is Balanced:", tree.is_balanced())
    print("Is BST:", tree.is_bst())

    assert tree.is_balanced()
    assert tree.is_bst()

    print("All assertions passed!")
