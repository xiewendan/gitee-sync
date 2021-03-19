# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2019/5/15 17:11

# desc: 针对os.path提供功能的补充或做一层封装

import os


# "a/b/c.txt -> .txt"
def FileExt(szPath):
    return os.path.splitext(szPath)[1]


# "a/b/c.txt -> a/b"
# "a/b/c -> a/b"
def ParseDir(szPath):
    return os.path.split(szPath)[0]


# "a/b/c.txt -> c"
# "a/b/c     -> c"
def FileName(szPath):
    szBaseName = os.path.basename(szPath)
    return os.path.splitext(szBaseName)[0]


# "a/b/c.txt -> c.txt"
def FileNameWithExt(szPath):
    return os.path.basename(szPath)


def CreateFileDir(szFilePath):
    szDir = ParseDir(szFilePath)
    if not os.path.exists(szDir):
        os.makedirs(szDir)


def ClearEmptyDir(szRootFPath):
    """
    清理所有空文件夹
    空文件的定义：递归子目录下没有文件，可以有文件夹
    """
    import os
    import shutil

    dictDirToDel = []
    dictDirHasFile = {szRootFPath: True}
    nLenRootFPath = len(szRootFPath)

    for szParentFPath, _, listFileName in os.walk(szRootFPath):
        if len(listFileName) != 0:  # 空文件夹
            szParentRPath = szParentFPath[nLenRootFPath + 1:]
            szParentRPath = szParentRPath.replace("\\", "/")
            listDirName = szParentRPath.split("/")

            szCurFPath = szRootFPath
            for nIndex in range(0, len(listDirName)):
                szCurFPath += "/" + listDirName[nIndex]
                if szCurFPath not in dictDirHasFile:
                    dictDirHasFile[szCurFPath] = True

    for szParentFPath, _, _ in os.walk(szRootFPath):
        szParentFPath = szParentFPath.replace("\\", "/")
        if szParentFPath not in dictDirHasFile:
            dictDirToDel.append(szParentFPath)

    for szPath in dictDirToDel:
        if os.path.exists(szPath):
            shutil.rmtree(szPath)
