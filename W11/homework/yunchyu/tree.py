# W11 研讨一：树的建模与递归遍历
# 第1组 记录员：yunchyu

class TreeNode:
    def __init__(self, val):
        self.val = val
        self.children = []


# ---------- 任务1：公司组织架构树 ----------
ceo = TreeNode("CEO")
cto = TreeNode("CTO")
cfo = TreeNode("CFO")
ceo.children.extend([cto, cfo])

frontend = TreeNode("前端组")
backend = TreeNode("后端组")
ai = TreeNode("AI组")
cto.children.extend([frontend, backend, ai])

frontend.children.extend([TreeNode("页面1组"), TreeNode("页面2组")])
backend.children.extend([TreeNode("API组"), TreeNode("数据库组")])

accounting = TreeNode("会计组")
audit = TreeNode("审计组")
cfo.children.extend([accounting, audit])

# 若 AI组 新增 NLP组，只需一行，不必改结构：
# ai.children.append(TreeNode("NLP组"))


def show(node, level=0):
    """打印树状结构，便于核对"""
    print("  " * level + node.val)
    for c in node.children:
        show(c, level + 1)


def find(node, name):
    """按名字找结点，找不到返回 None"""
    if node is None:
        return None
    if node.val == name:
        return node
    for c in node.children:
        r = find(c, name)
        if r:
            return r
    return None


def depth_of(root, name):
    """返回结点的深度（根深度=0），找不到返回 -1"""
    def dfs(node, d):
        if node is None:
            return -1
        if node.val == name:
            return d
        for c in node.children:
            r = dfs(c, d + 1)
            if r != -1:
                return r
        return -1
    return dfs(root, 0)        # ← 这里要传 0，不是 name



def height(root):
    """树高：按层数计（单结点为1）"""
    if root is None:
        return 0
    if not root.children:
        return 1
    return 1 + max(height(c) for c in root.children)


# ---------- 任务2/3：二叉树的三种递归遍历 ----------
class BiNode:
    def __init__(self, val=0):
        self.val = val
        self.left = None
        self.right = None


def preorder(node):
    if node is None:
        return
    print(node.val, end=" ")
    preorder(node.left)
    preorder(node.right)


def inorder(node):
    if node is None:
        return
    inorder(node.left)
    print(node.val, end=" ")
    inorder(node.right)


def postorder(node):
    if node is None:
        return
    postorder(node.left)
    postorder(node.right)
    print(node.val, end=" ")


def build_demo_tree():
    """构建任务2 的树：10 根，左5(3,7)，右15(12,20)"""
    root = BiNode(10)
    root.left = BiNode(5)
    root.right = BiNode(15)
    root.left.left = BiNode(3)
    root.left.right = BiNode(7)
    root.right.left = BiNode(12)
    root.right.right = BiNode(20)
    return root


if __name__ == "__main__":
    print("=== 组织架构树 ===")
    show(ceo)

    print("\n=== 深度与高度 ===")
    print("API组 深度 =", depth_of(ceo, "API组"))
    print("AI组 深度 =", depth_of(ceo, "AI组"))
    print("树的高度 =", height(ceo))

    print("\n=== 三种遍历（应等于手算结果）===")
    root = build_demo_tree()
    print("前序：", end=""); preorder(root); print()
    print("中序：", end=""); inorder(root); print()
    print("后序：", end=""); postorder(root); print()
