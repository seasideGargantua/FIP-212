from collections import deque
import heapq
import random
import sys
import time


def max_sliding_window(nums, k, trace=None):
    if k <= 0 or not nums:
        return []
    dq = deque()
    result = []
    for i, x in enumerate(nums):
        if dq and dq[0] <= i - k:
            dq.popleft()
        while dq and nums[dq[-1]] <= x:
            dq.pop()
        dq.append(i)
        if i >= k - 1:
            result.append(nums[dq[0]])
        if trace is not None:
            trace.append((i, x, list(dq), list(result)))
    return result


def max_sliding_window_brute(nums, k):
    if k <= 0 or not nums:
        return []
    return [max(nums[i:i + k]) for i in range(len(nums) - k + 1)]


def schedule_tasks(priorities, log=None):
    heap = []
    for i, p in enumerate(priorities):
        task = f"任务{i}"
        heapq.heappush(heap, (p, i, task))
        if log is not None:
            log.append(("push", p, i, task, list(heap)))
    order = []
    while heap:
        p, i, task = heapq.heappop(heap)
        order.append((p, i, task))
        if log is not None:
            log.append(("pop", p, i, task, list(heap)))
    return order


def schedule_tasks_bad(priorities):
    heap = []
    for i, p in enumerate(priorities):
        heapq.heappush(heap, (p, {"name": f"任务{i}"}))
    return [heapq.heappop(heap) for _ in range(len(heap))]


def show_trace(nums, k):
    trace = []
    result = max_sliding_window(nums, k, trace)
    print(f"滑动窗口最大值：nums={nums}, k={k}")
    print(f"  {'i':>2} {'x':>4}  {'dq（存索引）':<14} {'result':<12}")
    for i, x, dq, res in trace:
        print(f"  {i:>2} {x:>4}  {str(dq):<14} {str(res):<12}")
    print(f"  结果：{result}（暴力法核对：{max_sliding_window_brute(nums, k)}）")
    return result


def show_schedule(priorities):
    log = []
    order = schedule_tasks(priorities, log)
    print(f"任务调度：优先级={priorities}（heapq 小根堆，从低到高出队）")
    for op, p, i, task, heap in log:
        head = "入堆" if op == "push" else "出堆"
        print(f"  {head} ({p}, {i}, {task:<6})  堆内={heap}")
    print(f"  处理顺序：{[f'{t[2]}(p={t[0]})' for t in order]}")
    return order


def show_tiebreak_problem():
    print("同优先级但不加序号：")
    try:
        schedule_tasks_bad([2, 2])
        print("  未报错")
    except TypeError as e:
        print(f"  TypeError: {e}")


def check(name, ok, detail=""):
    print(f"[{'通过' if ok else '失败'}] {name}{('：' + detail) if detail else ''}")
    return ok


def test_fixed_cases():
    cases = [
        ([5, 3, 4, 1, 2], 3, [5, 4, 4]),
        ([1], 1, [1]),
        ([9, 8, 7, 6], 2, [9, 8, 7]),
        ([1, 2, 3, 4], 4, [4]),
        ([4, 4, 4], 2, [4, 4]),
        ([2, 1], 3, []),
    ]
    passed = 0
    for nums, k, want in cases:
        got = max_sliding_window(nums, k)
        passed += check(f"滑动窗口 {nums} k={k}", got == want, f"得到 {got}，期望 {want}")
    return check("固定用例合计", passed == len(cases), f"{passed}/{len(cases)}")


def test_against_brute(trials=200):
    random.seed(20261112)
    for _ in range(trials):
        n = random.randint(1, 30)
        nums = [random.randint(-20, 20) for _ in range(n)]
        k = random.randint(1, n + 2)
        if max_sliding_window(nums, k) != max_sliding_window_brute(nums, k):
            return check("随机对照暴力法", False, f"{nums} k={k}")
    return check("随机对照暴力法", True, f"{trials} 组随机数据全部一致")


def test_schedule_fixed():
    order = schedule_tasks([3, 1, 4, 1, 5])
    want = [(1, 1, "任务1"), (1, 3, "任务3"), (3, 0, "任务0"), (4, 2, "任务2"), (5, 4, "任务4")]
    return check("调度顺序（课件样例）", order == want, f"得到 {[(p, i) for p, i, _ in order]}")


def test_schedule_stability(trials=100):
    random.seed(7)
    for _ in range(trials):
        priorities = [random.randint(1, 4) for _ in range(random.randint(1, 12))]
        order = schedule_tasks(priorities)
        keys = [(p, i) for p, i, _ in order]
        if keys != sorted(keys):
            return check("调度稳定性", False, f"{priorities} → {keys}")
    return check("调度稳定性", True, f"{trials} 组随机优先级，先比优先级再比到达序号")


def test_tiebreak_error():
    try:
        schedule_tasks_bad([2, 2])
    except TypeError:
        return check("不加序号会 TypeError", True, "元组第三项是 dict，堆比较失败")
    return check("不加序号会 TypeError", False, "没有抛出 TypeError")


def bench(n, k):
    random.seed(1)
    nums = [random.randint(0, 10 ** 6) for _ in range(n)]
    print(f"复杂度对比：n={n}, k={k}（随机数组）")
    for name, fn in (("单调队列 O(n)", max_sliding_window), ("暴力法 O(nk)", max_sliding_window_brute)):
        start = time.perf_counter()
        result = fn(nums, k)
        cost = (time.perf_counter() - start) * 1000
        print(f"  {name:<14}: {cost:9.3f} ms  头 {result[:3]} 尾 {result[-3:]}")


def main():
    print("=" * 56)
    print("W9 项目 B：滑动窗口最大值 + heapq 优先队列调度")
    print("=" * 56)
    if "--bench" in sys.argv:
        bench(2000, 50)
        bench(20000, 50)
        bench(20000, 500)
        return
    show_trace([5, 3, 4, 1, 2], 3)
    print()
    show_schedule([3, 1, 4, 1, 5])
    print()
    show_tiebreak_problem()
    print()
    print("-" * 56)
    print("测试")
    print("-" * 56)
    results = [
        test_fixed_cases(),
        test_against_brute(),
        test_schedule_fixed(),
        test_schedule_stability(),
        test_tiebreak_error(),
    ]
    print("-" * 56)
    print(f"汇总：必做测试 {sum(results)}/{len(results)} 项通过")


if __name__ == "__main__":
    main()
