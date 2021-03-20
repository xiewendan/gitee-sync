# import os
# import shutil
#
# dictDirHasFile = {}
# szRootFPath = "C:/Users/gzxiejinchun/Desktop/a"
# dictDirHasFile[szRootFPath] = True
# nLenRootFPath = len(szRootFPath)
#
# dictDirToDel = []
#
# for szParentFPath, _, listFileName in os.walk(szRootFPath):
#     if len(listFileName) != 0:  # 空文件夹
#         szParentRPath = szParentFPath[nLenRootFPath + 1:]
#         szParentRPath = szParentRPath.replace("\\", "/")
#         listDirName = szParentRPath.split("/")
#
#         szCurFPath = szRootFPath
#         for nIndex in range(0, len(listDirName)):
#             szCurFPath += "/" + listDirName[nIndex]
#             if szCurFPath not in dictDirHasFile:
#                 dictDirHasFile[szCurFPath] = True
#
# for szParentFPath, listDirName, listFileName in os.walk(szRootFPath):
#     szParentFPath = szParentFPath.replace("\\", "/")
#     if szParentFPath not in dictDirHasFile:
#         dictDirToDel.append(szParentFPath)
#
# for szPath in dictDirToDel:
#     if os.path.exists(szPath):
#         shutil.rmtree(szPath)
#
#

def GetFile(szPath):
    return open(szPath, "w")


szFile = "d:/aa.txt"
with GetFile(szFile) as fp:
    fp.write("xjc")

import os
os.remove(szFil
