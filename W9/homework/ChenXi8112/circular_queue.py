class CircularQueue:
    def __init__(self, capacity=5):
        self.items = [None] * capacity
        self.capacity = capacity
        self.front = self.rear = 0
        self.count = 0

    def enqueue(self, item):
        if self.count == self.capacity:
            return  # 满
        self.items[self.rear] = item
        self.rear = (self.rear + 1) % self.capacity     # 绕回
        self.count += 1

    def dequeue(self):
        if self.count == 0:
            return None # 空
        item = self.items[self.front]
        self.front = (self.front + 1) % self.capacity   # 绕回
        self.count -= 1
        return item

    def __repr__(self):
        return f'CircularQueue(items={self.items}, front={self.front}, rear={self.rear}, count={self.count})'


if __name__ == "__main__":
    q = CircularQueue(4)

    print("初始", q)

    q.enqueue(1)
    print("enqueue(1)", q)

    q.enqueue(2)
    print("enqueue(2)", q)

    print("dequeue()", q.dequeue())
    print("dequeue()后", q)

    q.enqueue(3)
    print("enqueue(3)", q)

    q.enqueue(4)
    print("enqueue(4)", q)

    q.enqueue(5)
    print("enqueue(5)", q)

    q.enqueue(6)  # 队满，失败
    print("enqueue(6)", q)
