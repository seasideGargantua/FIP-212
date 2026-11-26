import random
import time
from bisect import bisect_left, insort


class BSTNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def insert(root, val):
    if not root:
        return BSTNode(val)
    if val < root.val:
        root.left = insert(root.left, val)
    elif val > root.val:
        root.right = insert(root.right, val)
    return root


def build(values):
    root = None
    for v in values:
        root = insert(root, v)
    return root


def search(root, val, path=None):
    if path is None:
        path = []
    if not root:
        return None, path
    path.append(root.val)
    if val == root.val:
        return root, path
    if val < root.val:
        return search(root.left, val, path)
    return search(root.right, val, path)


def inorder(node, out=None):
    if out is None:
        out = []
    if not node:
        return out
    inorder(node.left, out)
    out.append(node.val)
    inorder(node.right, out)
    return out


def height(node):
    if not node:
        return 0
    return 1 + max(height(node.left), height(node.right))


def count_nodes(node):
    if not node:
        return 0
    return 1 + count_nodes(node.left) + count_nodes(node.right)


def is_bst(node, low=float("-inf"), high=float("inf")):
    if not node:
        return True
    if not (low < node.val < high):
        return False
    return is_bst(node.left, low, node.val) and is_bst(node.right, node.val, high)


def show(node, prefix="", is_left=None, out=None):
    if out is None:
        out = []
    if not node:
        return out
    if is_left is None:
        out.append(str(node.val))
    else:
        out.append(prefix + ("├── " if is_left else "└── ") + str(node.val))
    nxt = "" if is_left is None else prefix + ("│   " if is_left else "    ")
    if node.left:
        show(node.left, nxt, True, out)
    if node.right:
        show(node.right, nxt, False, out)
    return out


def show_tree(node, title=""):
    if title:
        print(title)
    for line in show(node):
        print(line)


def insert_trace(values):
    root = None
    for i, v in enumerate(values, 1):
        root = insert(root, v)
        print(f"-- 第 {i} 次插入 {v} --")
        show_tree(root)
        print()


def search_trace(root, targets):
    print("== 查找路径 ==")
    for t in targets:
        node, path = search(root, t)
        arrow = " → ".join(map(str, path)) if path else "（空树）"
        if node:
            print(f"  查 {t}：{arrow}   ✔ 找到，比较了 {len(path)} 次")
        else:
            print(f"  查 {t}：{arrow} → None   ✘ 没找到，比较了 {len(path)} 次")


def bench(sizes=(20000, 100000), seed=2026):
    print()
    print("== 插入 / 查找 对比（随机不重复整数）==")
    print(f"  {'n':>7}  {'BST 建树':>10}  {'数组 insort':>12}  {'BST 查找':>10}  {'数组 bisect':>12}")
    for n in sizes:
        random.seed(seed)
        data = random.sample(range(n * 10), n)

        t0 = time.perf_counter()
        root = build(data)
        t1 = time.perf_counter()
        for v in data:
            search(root, v)
        t2 = time.perf_counter()

        arr = []
        t3 = time.perf_counter()
        for v in data:
            insort(arr, v)
        t4 = time.perf_counter()
        for v in data:
            i = bisect_left(arr, v)
            _ = i < len(arr) and arr[i] == v
        t5 = time.perf_counter()

        print(f"  {n:>7}  {(t1 - t0) * 1000:8.1f}ms  {(t4 - t3) * 1000:10.1f}ms  "
              f"{(t2 - t1) * 1000:8.1f}ms  {(t5 - t4) * 1000:10.1f}ms")
    print("  读法：插入 BST 赢（只改指针，不搬数据）；查找数组赢（连续内存 + C 实现二分）。")
    print("        数据常变 → BST；数据不变只查 → 排序数组，正好对应课件里的静态/动态选型。")


def main():
    values = [50, 30, 70, 20, 40, 60, 80]
    print("== 项目 A：BST 构建（按顺序插入 %s）==" % values)
    print()
    insert_trace(values)
    root = build(values)

    print("== 最终树 ==")
    show_tree(root)
    print()
    print(f"  结点数：{count_nodes(root)}；高度：{height(root)}")
    print(f"  中序遍历：{' '.join(map(str, inorder(root)))}")
    print(f"  中序升序（BST 性质成立）：{inorder(root) == sorted(inorder(root))}；is_bst()：{is_bst(root)}")

    print()
    search_trace(root, [40, 65, 80])

    print()
    bench()


if __name__ == "__main__":
    main()
