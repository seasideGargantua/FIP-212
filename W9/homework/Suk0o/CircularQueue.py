class CircularQueue:
    def __init__(self, capacity=5):
        self.items = [None] * capacity
        self.capacity = capacity
        self.front = self.rear = 0
        self.count = 0
    # 补全 enqueue / dequeue
    def enqueue(self, _):
        if self.count == self.capacity:
            return "满队列"
        self.items[self.rear] = _
        self.rear = (self.rear + 1) % self.capacity
        self.count += 1
    def dequeue(self):
        if self.count == 0:
            return "空队列"
        _ = self.items[self.front]
        self.items[self.front] = None
        self.front = (self.front + 1) % self.capacity
        self.count -= 1
        return _