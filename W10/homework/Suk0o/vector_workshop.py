import numpy as np

users = {
    "Alice":  np.array([5, 1, 2, 4]),
    "Bob":    np.array([4, 2, 1, 5]),
    "Carol":  np.array([1, 5, 5, 1]),
    "Dave":   np.array([5, 1, 2, 4]),
    "Eve":    np.array([3, 3, 3, 3]),
}
# TASK ONE
def cos_sim(u,v):
    n1 = np.linalg.norm(u)
    n2 = np.linalg.norm(v)
    if n1 == 0 or n2 == 0:
        return 0
    return np.dot(u,v) / (n1 * n2)
# TASK TWO
def best_match(user_name):
    if user_name not in users:
        return None
    user_vector = users[user_name]
    best_user = None
    best_sim = -1
    for other_name, other_vector in users.items():
        if other_name == user_name:
            continue
        sim = cos_sim(user_vector, other_vector)
        if sim > best_sim:
            best_sim = sim
            best_user = other_name
    return best_user
# TASK THREE
'''["Python", "AI", "数据", "编程", "算法"]'''

doc1 = np.array([3, 2, 1, 2, 1])
doc2 = np.array([2, 3, 2, 1, 2])
doc3 = np.array([0, 0, 0, 5, 0])   # 纯编程，无 AI/数据
# ACTIVITY ONE 两两计算余弦相似度
sim12 = cos_sim(doc1, doc2)
sim13 = cos_sim(doc1, doc3)
sim23 = cos_sim(doc2, doc3)
print("Cosine similarity between doc1 and doc2:", sim12)
print("Cosine similarity between doc1 and doc3:", sim13)
print("Cosine similarity between doc2 and doc3:", sim23)
# ACTIVITY TWO 找出与doc1相似的文档
most_similar = max(sim12, sim13)
if most_similar == sim12:
    print("Most similar to doc1:", "doc2")
else:
    print("Most similar to doc1:", "doc3")
# ACTIVITY THREE "Python"重复一百次
doc4 = np.array([100, 0, 0, 0, 0])
cos = cos_sim(doc1, doc4)
print("Cosine similarity between doc1 and doc4:", cos)
# PROJECT A 图像几何变换
points = np.array([
    [0, 0], [2, 0], [2, 1], [0, 1]
])   # shape (4, 2)
S = np.array([[2, 0], [0, 2]])
R = np.array([[0, -1], [1, 0]])
ans = (S @ R) @ points.T
print(ans.T)   