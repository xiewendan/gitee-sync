# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2021/3/14 18:28

# desc: 单元测试辅助函数


def CompareDict(dictData1, dictData2):
    return _CompareAInB(dictData1, dictData2) and _CompareAInB(dictData2, dictData1)


def _CompareAInB(dictDataA, dictDataB):
    for KeyObj, ValueObj in dictDataA.items():
        if KeyObj not in dictDataB:
            return False
        if ValueObj != dictDataB[KeyObj]:
            return False

    return True
