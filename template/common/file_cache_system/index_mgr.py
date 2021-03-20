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
    def __init__(self, szMd5, PreObj=None, NextObj=None):
        assert isinstance(szMd5, str)
        self.m_szMd5 = szMd5
        self.m_PreObj = PreObj
        self.m_NextObj = NextObj


class LinkMd5Queue:
    # 队头是pop，队尾是push
    def __init__(self):
        import common.my_log as my_log
        self.m_LoggerObj = my_log.MyLog(__file__)

        self.m_HeadObj = None
        self.m_TailObj = None

        self.m_dictMd5ToObj = {}

    def Push(self, szMd5):
        self.m_LoggerObj.debug("Md5:%s", szMd5)

        assert szMd5 is not None
        assert szMd5 not in self.m_dictMd5ToObj

        NewTailObj = Md5Node(szMd5, self.m_TailObj, None)
        self.m_dictMd5ToObj[szMd5] = NewTailObj

        if self.m_TailObj is not None:
            self.m_TailObj.m_NextObj = NewTailObj

        self.m_TailObj = NewTailObj

        if self.m_HeadObj is None:
            self.m_HeadObj = NewTailObj

    def Top(self):
        if self.m_HeadObj is None:
            return None
        else:
            return self.m_HeadObj.m_szMd5

    def _Tail(self):
        if self.m_TailObj is None:
            return None
        else:
            return self.m_TailObj.m_szMd5

    def Pop(self, szMd5=None):
        if szMd5 is None:
            if self.m_HeadObj is None:
                return None
            else:
                szMd5 = self.m_HeadObj.m_szMd5

        self.m_LoggerObj.debug("Md5:%s", szMd5)

        assert szMd5 in self.m_dictMd5ToObj
        CurNodeObj = self.m_dictMd5ToObj[szMd5]
        del self.m_dictMd5ToObj[szMd5]

        if CurNodeObj.m_PreObj is not None:
            CurNodeObj.m_PreObj.m_NextObj = CurNodeObj.m_NextObj

        if CurNodeObj.m_NextObj is not None:
            CurNodeObj.m_NextObj.m_PreObj = CurNodeObj.m_PreObj

        if self.m_TailObj == CurNodeObj:
            self.m_TailObj = CurNodeObj.m_PreObj

        if self.m_HeadObj == CurNodeObj:
            self.m_HeadObj = CurNodeObj.m_NextObj

        return szMd5

    def GetMd5QueueList(self):
        listRet = []
        CurObj = self.m_HeadObj
        while CurObj is not None:
            listRet.append(CurObj.m_szMd5)
            CurObj = CurObj.m_NextObj

        return listRet


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
        self.m_LinkMd5QueueObj = LinkMd5Queue()

    def __contains__(self, szMd5):
        return szMd5 in self.m_dictFileIndex

    def AddFileIndex(self, szMd5, szFileName, nSize, nLastUseTime=None):
        import math
        import time
        if nLastUseTime is None:
            nLastUseTime = math.floor(time.time() * 1000)

        FileIndexObj = FileIndex(szMd5, szFileName, nSize, nLastUseTime)

        assert szMd5 not in self.m_dictFileIndex
        self.m_dictFileIndex[szMd5] = FileIndexObj

        self._AddSize(nSize)
        self.m_LinkMd5QueueObj.Push(szMd5)

    def CheckExist(self, szMd5, szFileName, nSize):
        if szMd5 not in self.m_dictFileIndex:
            return False

        FileIndexObj = self.m_dictFileIndex[szMd5]
        return FileIndexObj.Md5 == szMd5 and FileIndexObj.FileName == szFileName and FileIndexObj.Size == nSize

    def GetAllFileIndex(self):
        return self.m_dictFileIndex

    def RemoveFileIndex(self, szMd5):
        assert szMd5 in self.m_dictFileIndex

        FileIndexObj = self.m_dictFileIndex[szMd5]
        self._AddSize(-FileIndexObj.Size)
        self.m_LinkMd5QueueObj.Pop(szMd5)

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

        listMd5Queue = self.m_LinkMd5QueueObj.GetMd5QueueList()
        for szMd5 in listMd5Queue:
            FileIndexObj = self.m_dictFileIndex[szMd5]
            listFileIndex.append(FileIndexObj.ToList())

        with open(self.m_szIndexFullPath, "w") as FileObj:
            json.dump(listFileIndex, FileObj)

    def CheckSpace(self, nSize):
        return self.m_nTotalSize + nSize < self.m_nMaxTotalSize

    def ClearSpace(self, nSize):
        listRemoveMd5 = []
        while self.m_LinkMd5QueueObj.Top() is not None:
            if self.CheckSpace(nSize):
                break
            else:
                szMd5 = self.m_LinkMd5QueueObj.Top()
                assert szMd5 is not None

                self.RemoveFileIndex(szMd5)
                listRemoveMd5.append(szMd5)

        return listRemoveMd5

    def _AddSize(self, nSize):
        nTotalSize = self.m_nTotalSize + nSize
        assert nTotalSize >= 0
        self.m_nTotalSize = nTotalSize
