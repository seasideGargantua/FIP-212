# -*- coding: utf-8 -*-
"""W10 研讨课二：矩阵变换项目（项目 A + 项目 B 都实现并跑通）

运行：python W10/homework/202698/matrix_project.py
依赖：numpy
"""

import numpy as np

np.set_printoptions(precision=3, suppress=True)


# ================= 项目 A：图像几何变换 =================

def project_a():
    print("=" * 62)
    print("项目 A：图像几何变换")
    print("=" * 62)

    # 矩形 4 顶点，每行一个点 (x, y)，shape (4, 2)
    points = np.array([
        [0, 0],   # 左下
        [2, 0],   # 右下
        [2, 1],   # 右上
        [0, 1],   # 左上
    ])
    print("原始顶点 points (4,2)：\n", points)

    # A1 缩放 S = [[2,0],[0,3]]
    S13 = np.array([[2, 0], [0, 3]])
    scaled = (S13 @ points.T).T
    print("\nA1 缩放 S=[[2,0],[0,3]] 后：\n", scaled)
    print("   x 放大 2 倍、y 放大 3 倍。")

    # A2 旋转 90° 逆时针 R = [[0,-1],[1,0]]
    R = np.array([[0, -1], [1, 0]])
    rotated = (R @ points.T).T
    print("\nA2 旋转 90° (R=[[0,-1],[1,0]]) 后：\n", rotated)
    print("   映射规则 (x,y) -> (-y, x)：(2,0)->(0,2)。")

    # A3 复合：先旋转 90°，再缩放 (2,2)  -> (S22 @ R) @ points.T
    S22 = np.array([[2, 0], [0, 2]])
    M = S22 @ R                      # 矩阵从右向左作用：先 R 后 S
    transformed = (M @ points.T).T
    print("\nA3 复合 S22 @ R =\n", M)
    print("   (S22 @ R) @ points.T 转置回 (4,2)：\n", transformed)

    # A4 手算验证：第一个点 (0,0) 和第二个点 (2,0)
    print("\nA4 手算验证：")
    p0 = points[0]                   # [0,0]
    p1 = points[1]                   # [2,0]
    # 先旋转 R：(x,y)->(-y,x)，再缩放 S22：(x,y)->(2x,2y)
    # p0: (0,0) -> R (0,0) -> S (0,0)
    # p1: (2,0) -> R (0,2) -> S (0,4)
    print("   [0,0] -> R [0,0] -> S22 [0,0]  ；程序：", transformed[0])
    print("   [2,0] -> R [0,2] -> S22 [0,4]  ；程序：", transformed[1])
    assert np.allclose(transformed[0], [0, 0])
    assert np.allclose(transformed[1], [0, 4])
    print("   手算与程序一致 ✓")

    # 思考 2：S @ R 和 R @ S 一样吗？
    print("\n思考 2：S22 @ R vs R @ S22")
    print("   S22 @ R =\n", S22 @ R)
    print("   R @ S22 =\n", R @ S22)
    print("   本例 S22 是均匀缩放（x、y 同比放大 2 倍），恰好与旋转 R 可交换，故两者相同。")
    print("   但矩阵乘法一般不满足交换律：S@R 先旋转后缩放，R@S 先缩放后旋转。")
    print("   换成非均匀缩放 S13=[[2,0],[0,3]]（x、y 放大倍数不同）就不再可交换：")
    print("   验证 S13：\n   S13@R=\n", S13 @ R, "\n   R@S13=\n", R @ S13)


# ================= 项目 B：批量相似度矩阵 =================

def cosine_similarity(u, v):
    denom = np.linalg.norm(u) * np.linalg.norm(v)
    return 0.0 if denom == 0 else np.dot(u, v) / denom


def project_b():
    print("\n" + "=" * 62)
    print("项目 B：批量相似度矩阵")
    print("=" * 62)

    np.random.seed(42)
    ratings = np.random.randint(1, 6, size=(10, 5))   # (10,5)
    print("评分矩阵 ratings (10,5)：\n", ratings)

    # B1 按行归一化：每个用户向量范数 -> 1
    norms = np.linalg.norm(ratings, axis=1, keepdims=True)   # (10,1)
    normalized = ratings / norms                              # 广播 (10,5)/(10,1)
    print("\nB1 按行范数 norms (10,1)：\n", norms.T.ravel())
    print("归一化后各行范数：\n", np.linalg.norm(normalized, axis=1))
    print("（全部为 1，验证归一化正确）")

    # B2 相似度矩阵
    sim_matrix = normalized @ normalized.T                   # (10,5)@(5,10)=(10,10)
    print("\nB2 sim_matrix (10,10) =\n", sim_matrix)
    print("对角线：", np.round(np.diag(sim_matrix), 3), "（全为 1：向量与自身余弦 = 1）")

    # B3 为用户 0 找最相似的其他用户（排除自己）
    sim_0 = sim_matrix[0].copy()
    sim_0[0] = -1
    best = int(np.argmax(sim_0))
    print(f"\nB3 与用户 0 最相似：用户 {best}，sim={sim_0[best]:.3f}")

    # B4 手动验证
    manual = cosine_similarity(ratings[0], ratings[best])
    print(f"B4 手动 cosine_similarity(ratings[0], ratings[{best}]) = {manual:.3f}")
    print("   与矩阵结果一致 ✓" if np.isclose(manual, sim_0[best]) else "   不一致 ✗")
    assert np.isclose(manual, sim_0[best])

    # 思考 2：不归一化会怎样
    raw = ratings @ ratings.T
    print("\n思考 2：未归一化 ratings @ ratings.T 是【内积矩阵】，不是余弦。")
    print(f"   内积 [0,{best}] = {raw[0,best]:.3f}，而余弦 = {sim_matrix[0,best]:.3f} —— 内积被向量长度放大。")

    # 复杂度说明
    print("\n思考 3：矩阵法与双重循环同为 O(n²·m)，但 @ 底层调用 BLAS/C 优化，实际快得多，且代码一行代替两层循环。")


if __name__ == "__main__":
    project_a()
    project_b()
