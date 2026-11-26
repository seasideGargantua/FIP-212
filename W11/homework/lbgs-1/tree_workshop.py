from collections import deque


class TreeNode:
    def __init__(self, val):
        self.val = val
        self.children = []


def build_company_tree():
    ceo = TreeNode("CEO")
    cto = TreeNode("CTO")
    cfo = TreeNode("CFO")
    ceo.children = [cto, cfo]

    fe = TreeNode("前端组")
    be = TreeNode("后端组")
    ai = TreeNode("AI组")
    cto.children = [fe, be, ai]

    fe.children = [TreeNode("页面1组"), TreeNode("页面2组")]
    be.children = [TreeNode("API组"), TreeNode("数据库组")]
    cfo.children = [TreeNode("会计组"), TreeNode("审计组")]
    return ceo


def print_tree(node, prefix="", is_last=True, is_root=True):
    if is_root:
        print(node.val)
    else:
        print(prefix + ("└── " if is_last else "├── ") + node.val)
    n = len(node.children)
    for i, child in enumerate(node.children):
        if is_root:
            child_prefix = ""
        else:
            child_prefix = prefix + ("    " if is_last else "│   ")
        print_tree(child, child_prefix, i == n - 1, is_root=False)


def depth_of(root, target):
    q = deque([(root, 0)])
    while q:
        node, d = q.popleft()
        if node.val == target:
            return d
        for child in node.children:
            q.append((child, d + 1))
    return -1


def height(node):
    if not node.children:
        return 0
    return 1 + max(height(child) for child in node.children)


def leaves(root, out=None):
    if out is None:
        out = []
    if not root.children:
        out.append(root.val)
        return out
    for child in root.children:
        leaves(child, out)
    return out


def count_nodes_multi(root):
    return 1 + sum(count_nodes_multi(child) for child in root.children)


class BinNode:
    def __init__(self, val=0):
        self.val = val
        self.left = None
        self.right = None


def build_task2_tree():
    root = BinNode(10)
    root.left = BinNode(5)
    root.right = BinNode(15)
    root.left.left = BinNode(3)
    root.left.right = BinNode(7)
    root.right.left = BinNode(12)
    root.right.right = BinNode(20)
    return root


def preorder(node, out=None):
    if out is None:
        out = []
    if not node:
        return out
    out.append(node.val)
    preorder(node.left, out)
    preorder(node.right, out)
    return out


def inorder(node, out=None):
    if out is None:
        out = []
    if not node:
        return out
    inorder(node.left, out)
    out.append(node.val)
    inorder(node.right, out)
    return out


def postorder(node, out=None):
    if out is None:
        out = []
    if not node:
        return out
    postorder(node.left, out)
    postorder(node.right, out)
    out.append(node.val)
    return out


def level_order(node):
    if not node:
        return []
    out, q = [], deque([node])
    while q:
        cur = q.popleft()
        out.append(cur.val)
        if cur.left:
            q.append(cur.left)
        if cur.right:
            q.append(cur.right)
    return out


def count_nodes(node):
    if not node:
        return 0
    return 1 + count_nodes(node.left) + count_nodes(node.right)


def count_leaves(node):
    if not node:
        return 0
    if not node.left and not node.right:
        return 1
    return count_leaves(node.left) + count_leaves(node.right)


def show_binary_tree(node, prefix="", is_left=None):
    if not node:
        return
    if is_left is None:
        print(node.val)
    else:
        print(prefix + ("├── " if is_left else "└── ") + str(node.val))
    nxt = prefix + ("│   " if is_left else "    ") if is_left is not None else ""
    if node.left or node.right:
        if node.left:
            show_binary_tree(node.left, nxt, True)
        else:
            print(nxt + "├── None")
        if node.right:
            show_binary_tree(node.right, nxt, False)
        else:
            print(nxt + "└── None")


def main():
    print("== 任务 1：公司组织架构树 ==")
    ceo = build_company_tree()
    print_tree(ceo)
    print()
    print(f"  结点总数：{count_nodes_multi(ceo)}")
    print(f"  API组 深度：{depth_of(ceo, 'API组')}")
    print(f"  AI组  深度：{depth_of(ceo, 'AI组')}")
    print(f"  树高（按边数）：{height(ceo)}；层数：{height(ceo) + 1}")
    print(f"  叶子结点：{'、'.join(leaves(ceo))}")
    print(f"  根结点：{ceo.val}")

    print()
    print("== 任务 2：遍历手算（四个答案）==")
    root = build_task2_tree()
    show_binary_tree(root)
    pre = preorder(root)
    ino = inorder(root)
    post = postorder(root)
    lvl = level_order(root)
    print()
    print("  前序：" + " ".join(map(str, pre)))
    print("  中序：" + " ".join(map(str, ino)))
    print("  后序：" + " ".join(map(str, post)))
    print("  层序：" + " ".join(map(str, lvl)))
    print(f"  中序是否升序（是不是 BST）：{ino == sorted(ino)}")
    print(f"  结点数：{count_nodes(root)}；叶子数：{count_leaves(root)}")

    print()
    print("== 变式：空树与单结点（Base Case）==")
    for name, tree in (("空树", None), ("单结点", BinNode(1))):
        print(f"  {name}：preorder={preorder(tree)} inorder={inorder(tree)} "
              f"postorder={postorder(tree)} 结点数={count_nodes(tree)} 叶子数={count_leaves(tree)}")


if __name__ == "__main__":
    main()
