# -*- coding: utf-8 -*-
"""W10 研讨课一：向量运算工作坊（任务 1-3，任务 3 选做也完成）

运行：python W10/homework/202698/vector_workshop.py
依赖：numpy（出图需要 matplotlib，缺失时跳过出图并提示）
"""

import numpy as np

# ---------------- 公共函数 ----------------

def cosine_similarity(u, v):
    """余弦相似度：方向夹角的余弦，只看方向不看长度。"""
    denom = np.linalg.norm(u) * np.linalg.norm(v)
    if denom == 0:                       # 除零保护：零向量方向无定义
        return 0.0
    return np.dot(u, v) / denom


def euclidean_distance(u, v):
    """欧几里得距离：直线距离，同时受方向与长度影响。"""
    return np.linalg.norm(u - v)


# ---------------- 任务 1：用户相似度 ----------------

users = {
    "Alice": np.array([5, 1, 2, 4]),
    "Bob":   np.array([4, 2, 1, 5]),
    "Carol": np.array([1, 5, 5, 1]),
    "Dave":  np.array([5, 1, 2, 4]),
    "Eve":   np.array([3, 3, 3, 3]),
}


def task1():
    print("=" * 60)
    print("任务 1：Alice 与其他用户的相似度 / 距离")
    print("=" * 60)
    alice = users["Alice"]
    print(f"{'用户':<8}{'余弦相似度':>12}{'欧氏距离':>12}")
    for name, vec in users.items():
        if name == "Alice":
            continue
        cos = cosine_similarity(alice, vec)
        dist = euclidean_distance(alice, vec)
        print(f"{name:<8}{cos:>12.3f}{dist:>12.3f}")

    # 两种度量各自的最相似者
    others = [(n, v) for n, v in users.items() if n != "Alice"]
    best_cos = max(others, key=lambda kv: cosine_similarity(alice, kv[1]))[0]
    best_dist = min(others, key=lambda kv: euclidean_distance(alice, kv[1]))[0]
    print(f"\n余弦最相似：{best_cos}；欧氏最近：{best_dist}；结论一致：{best_cos == best_dist}")
    print("说明：Dave 与 Alice 向量完全相同 -> cos=1, dist=0，两种度量都判定最相似。")


# ---------------- 任务 2：最近邻推荐 ----------------

def task2():
    print("\n" + "=" * 60)
    print("任务 2：给 Carol 推荐「科幻」（第 0 类）")
    print("=" * 60)
    carol = users["Carol"]
    best_name, best_cos = None, -1
    for name, vec in users.items():
        if name == "Carol":
            continue
        cos = cosine_similarity(carol, vec)
        if cos > best_cos:
            best_cos, best_name = cos, name
    print(f"与 Carol 最相似：{best_name}，cos={best_cos:.3f}")

    fav = int(np.argmax(users[best_name]))
    print(f"该用户评分最高的类别：第 {fav} 类（评分 {users[best_name][fav]}）")
    genres = ["科幻", "动作", "喜剧", "爱情"]
    fav_name = genres[fav]
    if fav == 0:
        print(f"最高分正是「科幻」-> 推荐：把 {best_name} 的第 0 类（科幻）评分 "
              f"{users[best_name][0]} 推荐给 Carol")
    else:
        print(f"最高分是「{fav_name}」而非科幻（第 0 类），按任务规则不推荐科幻。")
        print(f"供参考：{best_name} 的科幻（第 0 类）评分为 {users[best_name][0]}")

    # 为什么用余弦而不是欧氏
    print("思考：余弦只看方向、不受评分尺度影响（宽松用户整体打高分、严格用户整体打低分，"
          "偏好方向仍可比）；欧氏距离会把整体尺度差异算进去，尺度不同的人被误判为不相似。")


# ---------------- 任务 3：文档相似度（选做，已完成） ----------------

def task3():
    print("\n" + "=" * 60)
    print("任务 3：文档词袋相似度")
    print("=" * 60)
    vocab = ["Python", "AI", "数据", "编程", "算法"]
    doc1 = np.array([3, 2, 1, 2, 1])
    doc2 = np.array([2, 3, 2, 1, 2])
    doc3 = np.array([0, 0, 0, 5, 0])
    docs = {"doc1": doc1, "doc2": doc2, "doc3": doc3}

    for a in docs:
        for b in docs:
            if a < b:  # 每对只打印一次
                print(f"{a} vs {b}: cos={cosine_similarity(docs[a], docs[b]):.3f}, "
                      f"dist={euclidean_distance(docs[a], docs[b]):.3f}")

    c12 = cosine_similarity(doc1, doc2)
    c13 = cosine_similarity(doc1, doc3)
    print(f"\ndoc1 更相似于：{'doc2' if c12 > c13 else 'doc3'}（cos12={c12:.3f}, cos13={c13:.3f}）")
    print("符合直觉：doc3 只谈编程、没有 AI/数据，主题单一，与 doc1 的多元主题方向差异大。")

    pure_python = np.array([100, 0, 0, 0, 0])
    c = cosine_similarity(pure_python, doc1)
    print(f"纯 Python×100 与 doc1 的余弦：{c:.3f}")
    print("注意：课件提示说「方向几乎相同 → 接近 1」，但实测只有 0.688。"
          "原因是 doc1=[3,2,1,2,1] 并非只沿 Python 轴，它还有 AI/数据/编程/算法分量；"
          "只有当另一篇文档也几乎只讲 Python 时，余弦才接近 1。"
          "把 100 换成 1e6 结果仍约 0.688 —— 余弦与尺度无关，放大某一维不会让方向改变。")


# ---------------- 出图：alice_bob.png ----------------

def plot():
    print("\n" + "=" * 60)
    print("出图：alice_bob.png")
    print("=" * 60)
    try:
        import matplotlib
        matplotlib.use("Agg")            # 无窗口环境也能保存图片
        import matplotlib.pyplot as plt

        # 中文字体：优先微软雅黑 / 黑体，避免中文显示为方块
        plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "SimSun", "DejaVu Sans"]
        plt.rcParams["axes.unicode_minus"] = False
    except ModuleNotFoundError:
        print("未安装 matplotlib，跳过出图。安装：python -m pip install matplotlib")
        return

    alice = users["Alice"]
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))

    # 左图：各用户 4 类电影评分（折线）
    genres = ["科幻", "动作", "喜剧", "爱情"]
    x = np.arange(len(genres))
    for name, vec in users.items():
        axes[0].plot(x, vec, marker="o", label=name, linewidth=2)
    axes[0].set_xticks(x, genres)
    axes[0].set_title("各用户电影评分")
    axes[0].set_ylabel("评分")
    axes[0].legend(fontsize=8)
    axes[0].grid(alpha=0.3)

    # 左图补充：Alice 与 Bob 的评分对比条形图（呼应文件名）
    width = 0.35
    axes[1].bar(x - width / 2, alice, width, label="Alice")
    axes[1].bar(x + width / 2, users["Bob"], width, label="Bob")
    axes[1].set_xticks(x, genres)
    axes[1].set_title(f"Alice vs Bob  (cos={cosine_similarity(alice, users['Bob']):.3f}, "
                      f"dist={euclidean_distance(alice, users['Bob']):.3f})")
    axes[1].set_ylabel("评分")
    axes[1].legend()
    axes[1].grid(alpha=0.3, axis="y")

    fig.suptitle("W10 向量运算工作坊 — 用户相似度")
    fig.tight_layout()
    out = "alice_bob.png"
    fig.savefig(out, dpi=150)
    print(f"已保存：{out}")


if __name__ == "__main__":
    task1()
    task2()
    task3()
    plot()
