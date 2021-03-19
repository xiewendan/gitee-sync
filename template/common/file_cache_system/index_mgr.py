class FileIndex:
    """"""

    def __init__(self, szMd5, szFileName, nSize, nLastUseTime):
        assert nSize >= 0
        assert nLastUseTime > 0
        assert isinstance(szMd5, str) and len(szMd5) > 0
        assert isinstance(szFileName, str)

        self.m_szMd5 = szMd5
        self.m_szFileName = szFileName
        self.m_nSize = nSize
        self.m_nLastUseTime = nLastUseTime  # 单位毫秒

    @property
    def Md5(self):
        return self.m_szMd5

    @property
    def FileName(self):
        return self.m_szFileName

    @property
    def Size(self):
        return self.m_nSize

    @property
    def LastUseTime(self):
        return self.m_nLastUseTime

    def ToList(self):
        return [self.m_szMd5, self.m_szFileName, self.m_nSize, self.m_nLastUseTime]


class Md5Node:
    def __init__(self, szMd5, PreObj, NextObj):
        assert isinstance(szMd5, str)
        self.m_szMd5 = szMd5
        self.m_PreObj = PreObj
        self.m_NextObj = NextObj


class LinkMd5Queue:
    # 队头是pop，队尾是push
    def __init__(self):
        self.m_HeadObj = None
        self.m_TailObj = None

        self.m_dictMd5ToObj = {}

    def Push(self, szMd5):
        pass

    def Pop(self, szMd5=None):
        pass

    def MoveToTail(self, sMd5):
        pass

    def _AddMd5Obj(self, szMd5):
        pass

    def _RemoveMd5Obj(self, szMd5):
        pass


class IndexMgr:
    """"""

    def __init__(self, szIndexFullPath, nMaxTotalSize):
        assert nMaxTotalSize > 0

        import common.my_log as my_log
        self.m_LoggerObj = my_log.MyLog(__file__)

        self.m_LoggerObj.debug("szIndexFullPath:%s, MaxTotalSize:%d", szIndexFullPath, nMaxTotalSize)

        self.m_dictFileIndex = {}  # [szMd5] = FileIndex

        self.m_szIndexFullPath = szIndexFullPath

        self.m_nTotalSize = 0
        self.m_nMaxTotalSize = nMaxTotalSize

    def AddFileIndex(self, szMd5, szFileName, nSize, nLastUseTime=None):
        import math
        import time
        if nLastUseTime is None:
            nLastUseTime = math.floor(time.time() * 1000)

        FileIndexObj = FileIndex(szMd5, szFileName, nSize, nLastUseTime)

        assert szMd5 not in self.m_dictFileIndex
        self.m_dictFileIndex[szMd5] = FileIndexObj

        self._AddSize(nSize)

    def GetAllFileIndex(self):
        return self.m_dictFileIndex

    def RemoveFileIndex(self, szMd5):
        assert szMd5 in self.m_dictFileIndex

        FileIndexObj = self.m_dictFileIndex[szMd5]
        self._AddSize(-FileIndexObj.Size)

        del self.m_dictFileIndex[szMd5]

    def LoadIndex(self):
        self.m_LoggerObj.debug("")

        import os
        import json

        if os.path.exists(self.m_szIndexFullPath):
            with open(self.m_szIndexFullPath, "r") as FileObj:
                listFileIndex = json.load(FileObj)
                for listData in listFileIndex:
                    szMd5 = listData[0]
                    szFileName = listData[1]
                    nSize = listData[2]
                    nLastUseTime = listData[3]

                    self.AddFileIndex(szMd5, szFileName, nSize, nLastUseTime)

    def SaveIndex(self):
        self.m_LoggerObj.debug("")

        import json

        listFileIndex = []
        for _, FileIndexObj in self.m_dictFileIndex.items():
            listFileIndex.append(FileIndexObj.ToList())

        with open(self.m_szIndexFullPath, "w") as FileObj:
            json.dump(listFileIndex, FileObj)

    def CheckSpace(self, nSize):
        return self.m_nTotalSize + nSize < self.m_nMaxTotalSize

    def ClearSpace(self, nSize):
        pass

    def _AddSize(self, nSize):
        nTotalSize = self.m_nTotalSize + nSize
        assert nTotalSize >= 0
        self.m_nTotalSize = nTotalSize
