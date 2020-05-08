# -*- coding:utf-8 -*-
__author__ = 'gzxiejinchun'

import os
import shutil
import time
import re


def xor(bInput1, bInput2):
    return (bInput1 and bInput2) or (not bInput1 and not bInput2)


def deleteFileInDirWithLeftFile(szDirPath, szMatchStr, nLeftFileCount, bDir=False):
    """
    :param szDirPath: 目录的路径
    :param szMatchStr: 匹配的字符串
    :param nLeftFileCount: 保留的文件
    :return:
    """
    # 客户端包路径
    if not os.path.exists(szDirPath):
        print("xjcprint---------------cleardisk.deleteFileInDirWithLeftFile:file path not exist", szDirPath)
        return
    listDirName = os.listdir(szDirPath)
    dictName2ModifyTime = {}

    # 文件名到修改时间的映射表

    szLineCompile = re.compile(szMatchStr)
    for szDirName in listDirName:
        szFileFullPath = r"{0}\{1}".format(szDirPath, szDirName)
        if xor(bDir, os.path.isdir(szFileFullPath)) and szLineCompile.match(szDirName):
            nModifyTime = os.path.getmtime(szFileFullPath)
            dictName2ModifyTime[szFileFullPath] = nModifyTime

    # 按照修改时间逆序排序
    listFileSorted = sorted(dictName2ModifyTime.items(), key=lambda d: d[1], reverse=True)

    # 删除比较早的文件，仅保留n个
    for nIndex in xrange(nLeftFileCount, len(listFileSorted)):
        print "client pkg is deleted:", nIndex, listFileSorted[nIndex][0]
        if bDir:
            shutil.rmtree(listFileSorted[nIndex][0])
        else:
            os.remove(listFileSorted[nIndex][0])


def deleteFileInDirWithLeftDay(szDirPath, szMatchStr, nLeftDay, bDir=False):
    """
    :param szDirPath: 目录
    :param nLeftDay: 需要保留的天数
    :return:
    """
    if not os.path.exists(szDirPath):
        print("xjcprint---------------cleardisk.deleteFileInDirWithLeftFile", szDirPath)
        return
    listDirName = os.listdir(szDirPath)
    dictName2ModifyTime = {}
    nLeftSec = nLeftDay * 86400

    # 文件名到修改时间的映射表
    szLineCompile = re.compile(szMatchStr)
    for szDirName in listDirName:
        szFileFullPath = r"{0}\{1}".format(szDirPath, szDirName)
        if xor(bDir, os.path.isdir(szFileFullPath)) and szLineCompile.match(szDirName):
            nModifyTime = os.path.getmtime(szFileFullPath)
            dictName2ModifyTime[szFileFullPath] = nModifyTime

    for szPath, nModifyTime in dictName2ModifyTime.iteritems():
        if time.time() - nModifyTime > nLeftSec:
            print "client pkg is deleted:", szPath
            if bDir:
                shutil.rmtree(szPath)
            else:
                os.remove(szPath)


def TestReg():
    szLineCompile = re.compile(r"^[0-9]+.[0-9]+.[0-9]+.[0-9]+$")
    print(szLineCompile.match("1.0.0.1"))


if __name__ == '__main__':
    # ############################# 清除android
    deleteFileInDirWithLeftFile(r"E:\g87\Package\android\trunk", r"g87-full-[0-9]*-[0-9]*.apk", 5, False)
    deleteFileInDirWithLeftFile(r"E:\g87\Package\android\trunk\patch", r"^[0-9]+.[0-9]+.[0-9]+.[0-9]+$", 2, True)
    deleteFileInDirWithLeftDay(r"E:\g87\Package\android\release", r"g87r-full-[0-9]*-[0-9]*.apk", 8, False)
    deleteFileInDirWithLeftDay(r"E:\g87\Package\android\release\patch", r"^[0-9]+.[0-9]+.[0-9]+.[0-9]+$", 8, True)

    # ############################# 清除ios
    deleteFileInDirWithLeftFile(r"E:\g87\Package\ios\trunk", r"g87-full-[0-9]*-[0-9]*.apk", 5, False)
    deleteFileInDirWithLeftFile(r"E:\g87\Package\ios\trunk\patch", r"^[0-9]+.[0-9]+.[0-9]+.[0-9]+$", 2, True)
    deleteFileInDirWithLeftDay(r"E:\g87\Package\ios\release", r"g87r-full-[0-9]*-[0-9]*.apk", 8, False)
    deleteFileInDirWithLeftDay(r"E:\g87\Package\ios\release\patch", r"^[0-9]+.[0-9]+.[0-9]+.[0-9]+$", 8, True)

    # ############################# 清除系统
