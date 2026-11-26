class TreeNode:
    def __init__(self, val):
        self.val = val
        self.children = []

    def add_child(self, val):
        self.children.append(val)


if __name__ == "__main__":
    # 任务 1：公司组织架构树（一般树，每个结点用 children 保存其所有子树）
    ceo = TreeNode("CEO")
    cto = TreeNode("CTO")
    cfo = TreeNode("CFO")

    frontend = TreeNode("前端组")
    frontend.add_child(TreeNode("页面1组"))
    frontend.add_child(TreeNode("页面2组"))

    backend = TreeNode("后端组")
    backend.add_child(TreeNode("API组"))
    backend.add_child(TreeNode("数据库组"))

    ai = TreeNode("AI组")

    cto.add_child(frontend)
    cto.add_child(backend)
    cto.add_child(ai)

    accounting = TreeNode("会计组")
    auditing = TreeNode("审计组")
    cfo.add_child(accounting)
    cfo.add_child(auditing)

    ceo.add_child(cto)
    ceo.add_child(cfo)

    print("公司树已建立，根结点:", ceo.val)
