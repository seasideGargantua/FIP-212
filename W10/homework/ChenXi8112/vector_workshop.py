import numpy as np

users = {
    "Alice": np.array([5, 1, 2, 4]),
    "Bob":   np.array([4, 2, 1, 5]),
    "Carol": np.array([1, 5, 5, 1]),
    "Dave":  np.array([5, 1, 2, 4]),
    "Eve":   np.array([3, 3, 3, 3]),
}


def cosine_similarity(u, v):
    return np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))


def euclidean_distance(u, v):
    return np.linalg.norm(u - v)


if __name__ == "__main__":
    # 任务 1：Alice 与其他 4 人的余弦相似度与欧氏距离
    print("任务 1")
    for name, vec in users.items():
        if name != "Alice":
            cos = cosine_similarity(users["Alice"], vec)
            dist = euclidean_distance(users["Alice"], vec)
            print(f"{name}: cos={cos:.3f}, dist={dist:.3f}")

    # 任务 2：与 Carol 最相似的用户及其最高分类别
    print("\n任务 2")
    best_name, best_cos = "", -1
    for name, vec in users.items():
        if name == "Carol":
            continue    # 自己不算
        cos = cosine_similarity(users["Carol"], vec)
        if cos > best_cos:
            best_cos, best_name = cos, name
    print(f"与 Carol 最相似: {best_name}, cos={best_cos:.3f}")  # 与 Carol 最相似: Eve, cos=0.832
    # 事实上 Eve 四类都是 3 分，并列最高。
    # np.flatnonzero(a)：把 a 展平成一维，返回所有“非零”元素的下标，等价于 np.nonzero(np.ravel(a))[0]。
    # 这里 a 是“评分 == 最高分”的布尔数组，True 在 numpy 里也算非零，于是拿到全部并列最高的类别；
    # 换成 argmax 只返回第一个最大值，会丢掉并列信息；tolist() 把数组转成普通列表。
    best_genres = np.flatnonzero(users[best_name] == users[best_name].max()).tolist()
    print(f"最高分类别: {best_genres}")  # 最高分类别: [0, 1, 2, 3]
    if 0 in best_genres:    # 最高分类别包含科幻，就把该用户的科幻评分推荐给 Carol
        print(f"推荐给 Carol 的科幻评分: {users[best_name][0]}")  # 推荐给 Carol 的科幻评分: 3

    # 任务 3（选做）：文档相似度
    print("\n任务 3")  # 空行 + 任务 3
    doc1 = np.array([3, 2, 1, 2, 1])
    doc2 = np.array([2, 3, 2, 1, 2])
    doc3 = np.array([0, 0, 0, 5, 0])
    print(f"doc1-doc2: {cosine_similarity(doc1, doc2):.4f}")  # doc1-doc2: 0.8804
    print(f"doc1-doc3: {cosine_similarity(doc1, doc3):.4f}")  # doc1-doc3: 0.4588
    print(f"doc2-doc3: {cosine_similarity(doc2, doc3):.4f}")  # doc2-doc3: 0.2132
    python100 = np.array([100, 0, 0, 0, 0])
    print(f"python100-doc1: {cosine_similarity(python100, doc1):.4f}")  # python100-doc1: 0.6882
