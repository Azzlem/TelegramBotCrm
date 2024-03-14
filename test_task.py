class TreeNode:
    def __init__(self, val):
        self.val = val
        self.children = []


def build_tree(input_str):
    input_str = input_str.strip()

    def helper(s):
        if not s:
            return None

        stack = []
        root = None
        i = 0
        while i < len(s):
            if s[i] == '(':
                if root is not None:
                    stack.append(root)
                root = TreeNode('')
            elif s[i].isdigit() or s[i] == '-':
                start = i
                while i < len(s) and (s[i].isdigit() or s[i] == '-'):
                    i += 1
                val = int(s[start:i])
                node = TreeNode(val)
                if root:
                    root.children.append(node)
                i -= 1
            elif s[i] == ')':
                if stack:
                    parent = stack.pop()
                    parent.children.append(root)
                    root = parent
            i += 1

        return root

    index = 0
    return helper(input_str)


def print_tree(root, indent=0):
    if root:
        print(" " * indent + str(root.val))
        for child in root.children:
            print_tree(child, indent + 4)


def main():
    input_str = input("Введите текстовое представление дерева: ")
    root = build_tree(input_str)
    print_tree(root)


if __name__ == "__main__":
    main()
