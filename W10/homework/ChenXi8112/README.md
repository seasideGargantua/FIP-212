# W10 二组作业

## 研讨课一：向量运算工作坊

1. 代码：`vector_workshop.py`（任务 1–2 必做；任务 3 文档相似度选做也一并完成）。
2. 出图结果：`alice_bob.png`（由 `plt_test.py` 中 `plt.savefig` 生成，本机 GUI 运行时 `plt.show()` 也会弹窗）。
3. 一句话易错点：余弦相似度忘记除以 `np.linalg.norm(u) * np.linalg.norm(v)` 会算出大于 1 的值，且 `np.linalg.norm` 是平方和开根号，误写成 `np.sum` 会让结果整体偏大。
4. 报错记录：本机未出现 `ModuleNotFoundError`；`.venv` 内已装 numpy 2.5.5、matplotlib 3.11.2，用 `python -c "import sys; print(sys.executable)"` 与 `python -m pip -V` 确认过两者指向同一套 Python（`FIP-212\.venv`）。

## 研讨课二：矩阵变换项目

1. 项目代码：项目 B（批量相似度计算，`batch_similarity.py`）。
2. 项目选择说明：我们二组选项目 B，因为它把“逐个算相似度”的双重循环压成一次 `normalized @ normalized.T`，还能顺带把归一化、`axis=1` 和广播一次练到，正好接上研讨课一的余弦任务。
3. 反思：矩阵乘法把 n×n 次函数调用换成一次 `(10,5) @ (5,10)`，不用写两层循环、两行就够，且底层走 BLAS 更快——矩阵思维是用更高层的数学描述计算，而不是把循环写短；把“每个用户一行”想成行向量后，`axis=1` 配 `keepdims=True` 的广播方向也就有几何直觉了。

## 仓库

git@github.com:ChenXi8112/FIP-212.git
