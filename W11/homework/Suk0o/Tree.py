#TASK 1
class TreeNode():
    def __init__(self,val):
        self.val = val
        self.children = []
def preorder(root):
    if not root:
        return
    print(root.val)
    for child in root.children:
        preorder(child)
def inorder(root):
    if not root:
        return
    if len(root.children) > 0:
        inorder(root.children[0])
    print(root.val)
    for child in root.children[1:]:
        inorder(child)
def postorder(root):
    if not root:
        return
    for child in root.children:
        postorder(child)
    print(root.val)
CEO = TreeNode("CEO")
CTO = TreeNode("CTO")
CFO = TreeNode("CFO")
前端组 = TreeNode("前端组")
后端组 = TreeNode("后端组")
AI组 = TreeNode("AI组")
CEO.children.append(CTO)
CEO.children.append(CFO)
CTO.children.append(前端组)
CTO.children.append(后端组)
CTO.children.append(AI组)
CFO.children.append(TreeNode("会计组"))
CFO.children.append(TreeNode("审计组"))
前端组.children.append(TreeNode("页面1组"))
前端组.children.append(TreeNode("页面2组"))
后端组.children.append(TreeNode("API组"))
后端组.children.append(TreeNode("数据库组"))
print("前序遍历:")
preorder(CEO)
print("中序遍历:")
inorder(CEO)
print("后序遍历:")
postorder(CEO)
class TreeNode2():
    def __init__(self,val):
        self.val = val
        self.left = None
        self.right = None
def preorder2(root):
    if not root:
        return
    print(root.val)
    preorder2(root.left)
    preorder2(root.right)
def inorder2(root):
    if not root:
        return
    inorder2(root.left)
    print(root.val)
    inorder2(root.right)
def postorder2(root):
    if not root:
        return
    postorder2(root.left)
    postorder2(root.right)
    print(root.val)
# TASK 2 BST delete
def find_successor(node):   # 找以 node 为根的树的最小值
    while node.left:
        node = node.left
    return node
def delete_node(root, key):
    if not root:
        return None
    if key < root.val:
        root.left = delete_node(root.left, key)
    elif key > root.val:
        root.right = delete_node(root.right, key)
    else:  
        if not root.left:  
            return root.right
        elif not root.right:  
            return root.left
        else:  
            successor = find_successor(root.right)  
            root.val = successor.val 
            root.right = delete_node(root.right, successor.val)  
    return root