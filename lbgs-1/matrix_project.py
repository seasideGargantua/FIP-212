"""W10 研讨课二 项目 A：图像几何变换（用矩阵乘法搬动矩形的 4 个顶点）。

核心：点集是 (N, 2)，而变换矩阵是 (2, 2)，左乘要求点集是 (2, N)，所以先 .T。
矩阵从右往左作用：S @ R @ v 表示先旋转、再缩放。

用法：python matrix_project.py
"""

import numpy as np

try:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
    plt.rcParams["axes.unicode_minus"] = False
except ModuleNotFoundError as exc:
    plt = None
    print(f"[提示] 缺少 {exc.name}：用 python -m pip install matplotlib 后再试，本次跳过出图。")

# 每行一个点 (x, y)：左下、右下、右上、左上
points = np.array([
    [0, 0],
    [2, 0],
    [2, 1],
    [0, 1],
])

S = np.array([[2, 0], [0, 3]])   # 题目 1 的缩放
R = np.array([[0, -1], [1, 0]])  # 逆时针 90°
S2 = np.array([[2, 0], [0, 2]])  # 题目 3 的缩放 (2, 2)


def transform(M, pts):
    """(2,2) @ (2,N) → (2,N)，再转回 (N,2)：每行一个变换后的点。"""
    return (M @ pts.T).T


def show_table(title, pts):
    print(f"\n{title}")
    print(f"  shape: {pts.shape}")
    for (x, y) in pts:
        print(f"  ({x:>5.2f}, {y:>5.2f})")


def task1():
    scaled = transform(S, points)
    show_table("== 任务 1：缩放 S=[[2,0],[0,3]] ==", scaled)
    print(f"  S @ points.T 的 shape: {(S @ points.T).shape}")
    return scaled


def task2():
    rotated = transform(R, points)
    show_table("== 任务 2：逆时针旋转 90°，R=[[0,-1],[1,0]] ==", rotated)
    return rotated


def task3():
    composite = transform(S2 @ R, points)
    print("\n== 任务 3：复合变换（先旋转 90°，再缩放 2 倍）==")
    print(f"  S(2,2) @ R =\n{S2 @ R}")
    print(f"  R @ S(2,2) =\n{R @ S2}")
    print(f"  (2,2) 这种等比缩放与旋转可交换吗？{np.allclose(S2 @ R, R @ S2)}"
          "——等比缩放把两个轴放大同样倍数，先转后放和先放后转碰巧一样。")
    show_table("  先旋转后缩放（S @ R @ points.T）", composite)
    print(f"  (S @ R) @ points.T 的 shape: {(S2 @ R @ points.T).shape}"
          f" → .T 之后 {(S2 @ R @ points.T).T.shape}")

    # 换成非等比缩放 (2,3)，顺序就真的有区别了
    sr = transform(S @ R, points)
    rs = transform(R @ S, points)
    print(f"\n  换成非等比缩放 S(2,3)：S @ R 与 R @ S 相同吗？{np.allclose(S @ R, R @ S)}")
    print(f"  S @ R =\n{S @ R}\n  R @ S =\n{R @ S}")
    show_table("  先旋转后缩放 (2,3)（S @ R）", sr)
    show_table("  先缩放后旋转 (2,3)（R @ S）", rs)
    return composite, sr, rs


def task4(composite):
    """手算两个点，与程序结果对照。"""
    print("\n== 任务 4：手算验证（先 R 再 S）==")
    # (x, y) -> R: (-y, x) -> 再乘 S2: (-2y, 2x)
    hand = [(0, 0), (0, 4)]    # (0,0)->(0,0)；(2,0)->(0,2)->(0,4)
    ok = True
    for i, (hx, hy) in enumerate(hand):
        px, py = composite[i]
        same = np.isclose(px, hx) and np.isclose(py, hy)
        ok = ok and same
        print(f"  点{i}: 程序 ({px:.2f}, {py:.2f})  手算 ({hx}, {hy})  "
              f"{'一致' if same else '不一致'}")
    print(f"  → 手算与程序{'完全一致' if ok else '有出入'}："
          f"(0,0) 不动；(2,0) 旋转到 (0,2)，再放大 2 倍到 (0,4)。")
    return ok


def plot_shapes(scaled, rotated, composite, path="transform_rectangle.png"):
    if plt is None:
        print("\n[跳过出图] 当前解释器没有 matplotlib。")
        return False

    fig, axes = plt.subplots(1, 4, figsize=(13, 3.2))
    panels = [
        ("原矩形", points, "#444444"),
        ("缩放 (2,3)", scaled, "#1f77b4"),
        ("旋转 90°", rotated, "#2ca02c"),
        ("旋转+缩放 (2,2)", composite, "#d62728"),
    ]
    for ax, (title, pts, color) in zip(axes, panels):
        closed = np.vstack([pts, pts[0]])
        ax.plot(closed[:, 0], closed[:, 1], marker="o", color=color)
        for (x, y) in pts:
            ax.annotate(f"({x:g},{y:g})", (x, y), textcoords="offset points",
                        xytext=(4, 4), fontsize=8)
        ax.set_title(title)
        ax.axhline(0, color="gray", lw=0.6)
        ax.axvline(0, color="gray", lw=0.6)
        ax.set_aspect("equal", adjustable="datalim")
        ax.grid(alpha=0.3)

    fig.suptitle("项目 A：同一个矩形经三种 2×2 变换")
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)
    print(f"\n[出图] 已保存 {path}")
    return True


def main():
    print("== shape 追踪 ==")
    print(f"  points {points.shape} → points.T {points.T.shape}")
    print(f"  S@R {np.shape(S2 @ R)}；结果 (S@R)@points.T {np.shape((S2 @ R) @ points.T)}")

    scaled = task1()
    rotated = task2()
    composite, sr, rs = task3()
    ok = task4(composite)
    print(f"  顺带确认：非等比缩放时 S@R ≠ R@S → {not np.allclose(sr, rs)}")
    plot_shapes(scaled, rotated, composite)
    print("\n完成：" + ("手算与程序一致。" if ok else "手算与程序不一致，需检查。"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
