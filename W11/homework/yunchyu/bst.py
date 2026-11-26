# W11 研讨二：项目A · BST 构建与查找
# 第1组 记录员：yunchyu

class BSTNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def insert(root, val):
    if root is None:
        return BSTNode(val)
    if val < root.val:
        root.left = insert(root.left, val)
    elif val > root.val:
        root.right = insert(root.right, val)
    return root


def search(root, val, path=None):
    """返回 (是否找到, 经过的结点列表)"""
    if path is None:
        path = []
    node = root
    while node:
        path.append(node.val)
        if val == node.val:
            return True, path
        node = node.left if val < node.val else node.right
    return False, path


def inorder_vals(node, out=None):
    if out is None:
        out = []
    if node is None:
        return out
    inorder_vals(node.left, out)
    out.append(node.val)
    inorder_vals(node.right, out)
    return out


if __name__ == "__main__":
    values = [50, 30, 70, 20, 40, 60, 80]
    root = None
    for v in values:
        root = insert(root, v)

    print("中序遍历（应为升序）：", inorder_vals(root))

    for target in (40, 65, 80):
        ok, path = search(root, target)
        route = " → ".join(map(str, path))
        print(f"查 {target}：{'找到' if ok else '未找到'}，路径 {route}")
