class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


# ---------------- 递归版本 ----------------

def preorder(node):
    """前序遍历（递归）：根 -> 左 -> 右，直接打印。"""
    if node is None:                         # Base Case：空树
        return
    print(node.val, end=' ')                 # 先访问自己
    preorder(node.left)                      # 再递归左子树
    preorder(node.right)                     # 最后递归右子树


def inorder(node):
    """中序遍历（递归）：左 -> 根 -> 右，直接打印。"""
    if node is None:                         # Base Case：空树
        return
    inorder(node.left)                       # 先递归左子树
    print(node.val, end=' ')                 # 再访问自己
    inorder(node.right)                      # 最后递归右子树


def postorder(node):
    """后序遍历（递归）：左 -> 右 -> 根，直接打印。"""
    if node is None:                         # Base Case：空树
        return
    postorder(node.left)                     # 先递归左子树
    postorder(node.right)                    # 再递归右子树
    print(node.val, end=' ')                 # 最后访问自己


# ---------------- 栈版本（非递归，函数名以 _stack 结尾） ----------------

def preorder_stack(node):
    """前序遍历（栈）：根 -> 左 -> 右，直接打印。"""
    if node is None:
        return
    stack = [node]
    while stack:
        node = stack.pop()
        print(node.val, end=' ')             # 出栈即访问
        # 栈是后进先出：先压右子树、再压左子树，左子树才会先出栈
        if node.right is not None:
            stack.append(node.right)
        if node.left is not None:
            stack.append(node.left)


def inorder_stack(node):
    """中序遍历（栈）：左 -> 根 -> 右，直接打印。"""
    stack = []
    while node is not None or stack:
        # 一路向左，把沿途结点压栈，直到最左结点
        while node is not None:
            stack.append(node)
            node = node.left
        # 弹出并访问最左结点，然后转向它的右子树
        node = stack.pop()
        print(node.val, end=' ')
        node = node.right


def postorder_stack(node):
    """后序遍历（双栈）：左 -> 右 -> 根，直接打印。"""
    if not node:
        return
    s1, s2 = [node], []
    while s1:
        node = s1.pop()
        s2.append(node)
        if node.left:                        # 左子树先入 s1，后出
            s1.append(node.left)
        if node.right:                       # 右子树后入 s1，先出
            s1.append(node.right)
    # 此时 s2 中为“根 -> 右 -> 左”，依次弹出即为“左 -> 右 -> 根”
    while s2:
        print(s2.pop().val, end=' ')


if __name__ == "__main__":
    # 任务 2 的二叉树：
    #       10
    #      /  \
    #     5    15
    #    / \   / \
    #   3   7 12  20
    root = TreeNode(10)
    root.left = TreeNode(5)
    root.right = TreeNode(15)
    root.left.left = TreeNode(3)
    root.left.right = TreeNode(7)
    root.right.left = TreeNode(12)
    root.right.right = TreeNode(20)

    print("前序遍历（递归）:", end=' ')
    preorder(root)
    print()

    print("前序遍历（栈）:", end=' ')
    preorder_stack(root)
    print()

    print("中序遍历（递归）:", end=' ')
    inorder(root)
    print()

    print("中序遍历（栈）:", end=' ')
    inorder_stack(root)
    print()

    print("后序遍历（递归）:", end=' ')
    postorder(root)
    print()

    print("后序遍历（栈）:", end=' ')
    postorder_stack(root)
    print()
