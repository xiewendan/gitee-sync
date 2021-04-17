import sys


def main(args):
    import pstats

    PStatsObj = pstats.Stats(args[1])
    PStatsObj.sort_stats("cumtime").print_stats(100, 1.0, ".*")

    pass


if __name__ == '__main__':
    main(sys.argv)

# p.sort_stats("cumulative")
# 输出累计时间报告
# p.print_stats()
# 输出调用者的信息
# p.print_callers()
# 输出哪个函数调用了哪个函数
# p.print_callees()
# p.strip_dirs().sort_stats("cumtime").print_stats(100, 1.0, ".*")
