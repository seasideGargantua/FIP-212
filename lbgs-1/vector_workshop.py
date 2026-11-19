"""W10 研讨课一：向量运算工作坊。

任务 1：用户相似度（余弦 / 欧氏）
任务 2：最近邻推荐（给 Carol 找最像的人，再推科幻）
任务 3：文档相似度（选做）

用法：
    python vector_workshop.py             # 任务 1→2→3，并生成 alice_bob.png
    python vector_workshop.py --no-plot   # 只算数值，不出图
"""

import itertools
import sys

import numpy as np

# 只接 ModuleNotFoundError，并且明确告诉使用者怎么修；
# 不写 try/except: pass ，否则后面全变成 NameError（W5 的坑）。
try:
    import matplotlib

    matplotlib.use("Agg")          # 无窗口/远程环境也能存图
    import matplotlib.pyplot as plt

    plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
    plt.rcParams["axes.unicode_minus"] = False
except ModuleNotFoundError as exc:
    plt = None
    print(f"[提示] 缺少 {exc.name}：请用同一个解释器执行 "
          f"python -m pip install matplotlib 后再运行，本次跳过出图。")

users = {
    "Alice": np.array([5, 1, 2, 4]),
    "Bob": np.array([4, 2, 1, 5]),
    "Carol": np.array([1, 5, 5, 1]),
    "Dave": np.array([5, 1, 2, 4]),
    "Eve": np.array([3, 3, 3, 3]),
}

GENRES = ["科幻", "爱情", "喜剧", "动作"]   # 第 0 类是科幻


def cosine_similarity(u, v):
    """余弦相似度：只看向量方向，不受长度（评分尺度）影响。"""
    return np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))


def euclidean_distance(u, v):
    """欧氏距离：看两点之间的直线距离，受长度影响。"""
    return np.linalg.norm(u - v)


def task1():
    """Alice 与其他 4 人的两种度量，并比较结论。"""
    print("== 任务 1：Alice 与其他用户的相似度 ==")
    print(f"{'用户':<6}{'cos':>8}{'dist':>10}")
    rows = []
    for name, vec in users.items():
        if name == "Alice":
            continue
        cos = cosine_similarity(users["Alice"], vec)
        dist = euclidean_distance(users["Alice"], vec)
        rows.append((name, cos, dist))
        print(f"{name:<6}{cos:>8.3f}{dist:>10.3f}")

    by_cos = sorted(rows, key=lambda r: -r[1])
    by_dist = sorted(rows, key=lambda r: r[2])
    print(f"余弦最相似：{by_cos[0][0]}（cos={by_cos[0][1]:.3f}）")
    print(f"欧氏最近　：{by_dist[0][0]}（dist={by_dist[0][2]:.3f}）")
    print(f"排序（余弦）：{[r[0] for r in by_cos]}")
    print(f"排序（欧氏）：{[r[0] for r in by_dist]}")
    same = [r[0] for r in by_cos] == [r[0] for r in by_dist]
    print(f"两种度量结论{'一致' if same else '不一致'}：本例都选中 {by_cos[0][0]}，"
          f"因为 Dave 与 Alice 向量完全相同。")
    return rows


def task2():
    """给 Carol 找最近邻，再看对方最喜欢的类别是不是科幻。"""
    print("\n== 任务 2：给 Carol 的最近邻推荐 ==")
    carol = users["Carol"]
    best_name, best_cos = None, -1.0
    for name, vec in users.items():
        if name == "Carol":
            continue
        cos = cosine_similarity(carol, vec)
        print(f"  Carol–{name:<6} cos={cos:.3f}")
        if cos > best_cos:
            best_cos, best_name = cos, name

    favorite = int(np.argmax(users[best_name]))
    print(f"最相似用户：{best_name}（cos={best_cos:.3f}）")
    print(f"他最偏爱的类别：第 {favorite} 类（{GENRES[favorite]}），评分 {users[best_name][favorite]}")
    if favorite == 0:
        print(f"→ 推荐 Carol 去看“{GENRES[0]}”，参考评分 {users[best_name][0]} / 5")
    else:
        print(f"→ 他最爱的不是科幻；近邻法在数据稀疏时推荐不到目标类别，需要补规则")
    return best_name, best_cos, favorite


def task3():
    """选做：词袋向量的文档相似度。"""
    print("\n== 任务 3（选做）：文档相似度 ==")
    docs = {
        "doc1": np.array([3, 2, 1, 2, 1]),
        "doc2": np.array([2, 3, 2, 1, 2]),
        "doc3": np.array([0, 0, 0, 5, 0]),
    }
    for (name_a, vec_a), (name_b, vec_b) in itertools.combinations(docs.items(), 2):
        print(f"  cos({name_a}, {name_b}) = {cosine_similarity(vec_a, vec_b):.3f}")

    c12 = cosine_similarity(docs["doc1"], docs["doc2"])
    c13 = cosine_similarity(docs["doc1"], docs["doc3"])
    closer = "doc2" if c12 > c13 else "doc3"
    print(f"  doc1–doc2 = {c12:.3f}，doc1–doc3 = {c13:.3f} → doc1 与 {closer} 更相似")

    python_only = np.zeros(5)
    python_only[0] = 100          # 整篇只有 “Python” 重复 100 次
    print(f"  “Python”×100 与 doc1 的余弦 = {cosine_similarity(python_only, docs['doc1']):.3f}"
          f"（doc1 里 Python 只占约 1/3 的权重，所以远离 1）")


def plot_alice_bob(path="alice_bob.png"):
    """画 Alice / Bob 的评分折线并存成 PNG。"""
    if plt is None:
        print("\n[跳过出图] 当前解释器没有 matplotlib。")
        return False

    idx = list(range(len(GENRES)))
    fig, ax = plt.subplots(figsize=(5.4, 3.2))
    ax.plot(idx, users["Alice"], marker="o", label="Alice")
    ax.plot(idx, users["Bob"], marker="s", label="Bob")
    ax.set_xticks(idx, GENRES)
    ax.set_xlabel("电影类型")
    ax.set_ylabel("评分")
    ax.set_ylim(0, 6)
    ax.set_title("Alice vs Bob：四类电影评分")
    ax.grid(alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)
    print(f"\n[出图] 已保存 {path}（有窗口时把 savefig 换成 plt.show() 即可弹窗）")
    return True


def main(argv):
    task1()
    task2()
    task3()
    if "--no-plot" in argv:
        print("\n[跳过出图] 命令行给了 --no-plot。")
    else:
        plot_alice_bob()
    print("\n完成：任务 1–3 全部通过。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
