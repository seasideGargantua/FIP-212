import matplotlib.pyplot as plt

plt.plot([5, 1, 2, 4], marker="o")   # Alice
plt.plot([4, 2, 1, 5], marker="o")   # Bob

# 有窗口时 plt.show() 弹窗；无窗口（远程/沙箱）时用 savefig 出图验收
plt.savefig("alice_bob.png")
plt.show()
