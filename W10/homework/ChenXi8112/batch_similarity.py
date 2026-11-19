import numpy as np

np.random.seed(42)
ratings = np.random.randint(1, 6, size=(10, 5))


def cosine_similarity(u, v):
    return np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))


if __name__ == "__main__":
    # 1. 按行归一化，每个用户变成单位向量
    norms = np.linalg.norm(ratings, axis=1, keepdims=True)
    normalized = ratings / norms

    # 2. 一次算出 10x10 相似度矩阵
    sim_matrix = normalized @ normalized.T
    print(sim_matrix.round(3))  # 四舍五入到三位小数输出预览（矩阵太长，不注结果）

    # 3. 用户 0 最相似的其他用户（排除自己）
    sim_0 = sim_matrix[0].copy()
    sim_0[0] = -1
    best = np.argmax(sim_0)
    print(f"与用户 0 最相似: 用户 {best}, sim={sim_0[best]:.3f}")  # 与用户 0 最相似: 用户 5, sim=0.993

    # 4. 用单对函数手动验证
    print(f"手动验证: {cosine_similarity(ratings[0], ratings[best]):.3f}")  # 手动验证: 0.993
