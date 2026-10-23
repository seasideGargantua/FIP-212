import sys
import time
# 记录 pascal_bad 里每个 n 被调用的次数，用来回答“pascal_bad(3) 时 pascal_bad(2) 出现几次”
CALL_LOG = {}
def pascal(n):
    if n < 0:
        raise ValueError("n必须是非负整数")
    if n == 0:
        return [1]
    prev = pascal(n - 1)
    row = [1]
    for i in range(len(prev) - 1):
        row.append(prev[i] + prev[i + 1])
    row.append(1)
    return row
def pascal_bad(n):
    CALL_LOG[n] = CALL_LOG.get(n, 0) + 1
    if n == 0:
        return [1]
    row = [1]
    for i in range(n - 1):
        row.append(pascal_bad(n - 1)[i] + pascal_bad(n - 1)[i + 1])
    row.append(1)
    return row
def pascal_iter(n):
    if n < 0:
        raise ValueError("n 必须是非负整数")
    row = [1]
    for _ in range(n):
        new_row = [1]
        for j in range(len(row) - 1):
            new_row.append(row[j] + row[j + 1])
        new_row.append(1)
        row = new_row
    return row
def good_calls_theory(n):
    """好写法调 pascal 的次数（理论推导）：T(0)=1，T(n)=T(n-1)+1 → n+1 次。"""
    return n + 1
def bad_calls_theory(n):
    """坏写法调 pascal_bad 的次数（理论推导）：T(0)=1，T(n)=1+2(n-1)T(n-1)。"""
    total = 1
    for k in range(1, n + 1):
        total = 1 + 2 * (k - 1) * total
    return total
CASES = [(0, [1]), (1, [1, 1]), (3, [1, 3, 3, 1]), (4, [1, 4, 6, 4, 1])]
def check(func, name):
    """按 CASES 逐个核对，返回通过个数；打印预期/实际/结论。"""
    passed = 0
    print(f"[{name}]")
    print(f"  {'n':>2} | {'预期':<24} | {'实际':<24} | 结论")
    print("  " + "-" * 62)
    for n, expect in CASES:
        try:
            actual = func(n)
        except Exception as exc:                     # 出错也要如实打印
            actual = f"{type(exc).__name__}: {exc}"
        ok = actual == expect
        passed += ok
        print(f"  {n:>2} | {str(expect):<24} | {str(actual):<24} | {'通过' if ok else '不通过'}")
    print(f"  → {passed}/{len(CASES)} 通过\n")
    return passed
def check_consistent():
    """补充检查：好写法与迭代版在 n = 0..12 上一致；坏写法只对到 n = 7（再大太慢）。"""
    bad = []
    for n in range(13):
        if not (pascal(n) == pascal_iter(n)) or len(pascal(n)) != n + 1:
            bad.append(n)
    print(f"[一致性检查] n=0..12 好写法 == 迭代版：{'通过' if not bad else f'不通过 {bad}'}")
    bad_small = [n for n in range(8) if pascal_bad(n) != pascal(n)]
    print(f"[一致性检查] n=0..7  坏写法 == 好写法："
          f"{'通过' if not bad_small else f'不通过 {bad_small}'}\n")
    return not bad and not bad_small
def show_bad_call_counts():
    """坏写法：pascal_bad(3) 里 pascal_bad(2) 出现几次（实测，不是理论）。"""
    CALL_LOG.clear()
    pascal_bad(3)
    print("[坏写法调用计数] 实测 CALL_LOG")
    for n in sorted(CALL_LOG, reverse=True):
        print(f"  pascal_bad({n}) 被调用 {CALL_LOG[n]} 次")
    print(f"  合计 {sum(CALL_LOG.values())} 次函数调用"
          f"（理论推导 {bad_calls_theory(3)} 次）")
    print(f"  → pascal_bad(3) 时 pascal_bad(2) 出现 {CALL_LOG.get(2, 0)} 次\n")
def bench(func, n, runs=1, repeat=1):
    """计时：内部调用 runs 次取最慢/平均值，外层 repeat 次取最小（降低噪声）。"""
    best = None
    for _ in range(repeat):
        t0 = time.perf_counter()
        for _ in range(runs):
            func(n)
        dt = (time.perf_counter() - t0) / runs
        best = dt if best is None else min(best, dt)
    return best
def show_speed(slow=False):
    """坏写法 vs 好写法 vs 迭代：实际测量（默认输入很小，避免卡住）。"""
    print("[速度对比] 实测（time.perf_counter，取多次中最快一次）")
    print(f"  {'实现':<14}{'n':>3}{'调用次数(理论)':>16}{'耗时':>14}")
    rows = [
        ("坏写法", pascal_bad, 7, bad_calls_theory(7), 1, 3),
        ("坏写法", pascal_bad, 8, bad_calls_theory(8), 1, 1),
        ("好写法", pascal, 7, good_calls_theory(7), 2000, 3),
        ("好写法", pascal, 8, good_calls_theory(8), 2000, 3),
        ("好写法", pascal, 16, good_calls_theory(16), 2000, 3),
        ("迭代", pascal_iter, 7, None, 2000, 3),
        ("迭代", pascal_iter, 8, None, 2000, 3),
        ("迭代", pascal_iter, 16, None, 2000, 3),
    ]
    if slow:
        rows.insert(2, ("坏写法", pascal_bad, 9, bad_calls_theory(9), 1, 1))
    for label, func, n, calls, runs, repeat in rows:
        dt = bench(func, n, runs, repeat)
        calls_s = f"{calls:,}" if calls is not None else "—"
        print(f"  {label:<14}{n:>3}{calls_s:>16}{dt * 1000:>13.3f}ms")
    print(f"  坏写法 n=16 未测量：理论推导约 {bad_calls_theory(16):.3g} 次函数调用，"
          f"按上表速度需以年计，无法运行\n")
def main():
    print("=" * 68)
    print("W6 作业：杨辉三角整行 pascal(n)")
    print("=" * 68 + "\n")
    ok = []
    ok.append(check(pascal, "递归版 pascal(n)") == len(CASES))
    ok.append(check(pascal_iter, "迭代版 pascal_iter(n)") == len(CASES))
    ok.append(check_consistent())
    show_bad_call_counts()
    show_speed(slow="--slow" in sys.argv)
    print(f"汇总：必做测试 {sum(ok)}/{len(ok)} 项通过")
if __name__ == "__main__":
    main()