class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def insert(root, val):
    """向 BST 插入 val，返回插入后的根结点；已存在则不重复插入。"""
    if root is None:                         # 空位置：新建结点
        return TreeNode(val)
    if val < root.val:                       # 比根小，插入左子树
        root.left = insert(root.left, val)
    elif val > root.val:                     # 比根大，插入右子树
        root.right = insert(root.right, val)
    return root


def search(root, val):
    """在 BST 中查找 val，找到返回 True，没找到返回 False。"""
    if not root:                            # Base Case：空树，没找到
        return False
    if root.val == val:                     # 找到了
        return True
    if val < root.val:                      # 比根小，去左子树找
        return search(root.left, val)
    return search(root.right, val)          # 比根大，去右子树找


def search_path(root, val):
    """返回查找 val 时依次经过的结点值（没找到时到空位置前为止）。"""
    path = []
    node = root
    while node is not None:
        path.append(node.val)
        if node.val == val:                  # 找到了
            break
        node = node.left if val < node.val else node.right
    return path


def inorder(node):
    """中序遍历：左 -> 根 -> 右，直接打印（BST 的结果应递增）。"""
    if node is None:
        return
    inorder(node.left)
    print(node.val, end=' ')
    inorder(node.right)


if __name__ == "__main__":
    # 项目 A：按顺序插入 values 构建 BST
    values = [50, 30, 70, 20, 40, 60, 80]
    tree = None
    for value in values:
        tree = insert(tree, value)

    print("依次插入:", " ".join(str(v) for v in values))

    # 中序遍历应输出 20 30 40 50 60 70 80，递增说明 BST 性质成立
    print("中序遍历:", end=' ')
    inorder(tree)
    print()

    # 查找 40、65、80，并打印经过的路径
    for target in (40, 65, 80):
        found = search(tree, target)
        result_path = search_path(tree, target)
        print(f"查找 {target}: {' -> '.join(str(v) for v in result_path)}（{found}）")
