# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2018/12/17 20:59

# desc: 统计函数

import time
from common.my_exception import MyException


class TimeTag(object):
    """"""

    def __init__(self, lSecond, szTag):
        self.m_lSecond = int(lSecond)
        self.m_szTag = szTag

    def Minus(self, timeTag):
        return self.Second - timeTag.Second

    @property
    def Second(self):
        return self.m_lSecond

    @property
    def Tag(self):
        return self.m_szTag


class StatMgr(object):
    def __init__(self):
        self.m_listTimeTag = []

    def Reset(self):
        self.m_listTimeTag = []

    def LogTimeTag(self, szTag):
        if szTag == "":
            raise MyException("sz tag name is empty")

        timeTagObj = TimeTag(time.time(), szTag)
        self.m_listTimeTag.append(timeTagObj)

    def GetTimeTagStat(self):
        listTimeTagStr = ["FromStart".ljust(15) + "FromLast".ljust(15) + "TagName".ljust(30)]

        if len(self.m_listTimeTag) == 0:
            return "\n".join(listTimeTagStr)

        firstTimeTag = self.m_listTimeTag[0]
        lastTimeTag = self.m_listTimeTag[0]
        for _, timeTag in enumerate(self.m_listTimeTag):
            listTimeTagStr.append(
                str(timeTag.Minus(firstTimeTag)).ljust(15) +
                str(timeTag.Minus(lastTimeTag)).ljust(15) +
                timeTag.Tag.ljust(30)
            )
            lastTimeTag = timeTag

        return "\n".join(listTimeTagStr)


def main():
    StatMgrObj = StatMgr()
    StatMgrObj.LogTimeTag("xjc")
    StatMgrObj.LogTimeTag("xjc1")
    print(StatMgrObj.GetTimeTagStat())


if __name__ == '__main__':
    main()
