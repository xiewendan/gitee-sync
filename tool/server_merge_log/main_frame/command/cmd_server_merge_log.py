# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2022/4/24 20:55

# desc:

import os
import re
import time

import common.my_log as my_log
import main_frame.cmd_base as cmd_base


class CmdServerMergeLog(cmd_base.CmdBase):
    def __init__(self):
        super().__init__()
        self.m_LoggerObj = my_log.MyLog(__file__)

    @staticmethod
    def GetName():
        return "server_merge_log"

    def _OnInit(self):
        pass

    def Do(self):
        """执行命令"""
        self.m_LoggerObj.info("Start")

        szCWD = self.m_AppObj.ConfigLoader.CWD

        szFDir = self.m_AppObj.CLM.GetArg(1)

        import common.my_path as my_path
        szOutputFPath = my_path.ParseDir(szFDir) + "/merge.log"

        if not os.path.exists(szFDir):
            self.m_LoggerObj.info("input error, not exit: %s", szFDir)
            return

        listFPath = self.GetFileList(szFDir)
        listFileNode = []
        for szFPath in listFPath:
            FileNodeObj = FileNode(szFPath)
            if FileNodeObj.HasLog():
                listFileNode.append(FileNode(szFPath))

        FileNodeHeapObj = Heap(listFileNode)

        with open(szOutputFPath, "w") as fp:
            while not FileNodeHeapObj.Empty():
                szLog = FileNodeHeapObj.Top()
                FileNodeHeapObj.Pop()
                fp.write(szLog)

    def GetFileList(self, szFDir):
        listFPath = []
        for szParentPath, _, listFileName in os.walk(szFDir):
            for szFileName in listFileName:
                szFullPath = os.path.join(szParentPath, szFileName)
                listFPath.append(szFullPath)
        return listFPath


class Heap:
    def __init__(self, listFileNode):
        self.m_listFileNode = listFileNode

        self._Build()

    def _Build(self):
        nHeapLen = len(self.m_listFileNode)

        nLastIndex = nHeapLen - 1
        nLastParent = (nLastIndex - 1) // 2

        for nCurParent in range(nLastParent, -1, -1):
            self._Heapify(nCurParent, nLastIndex)

    def _Heapify(self, nRoot, nLastIndex):
        nC1 = 2 * nRoot + 1
        nC2 = 2 * nRoot + 2

        nMinRoot = nRoot

        if nC1 <= nLastIndex and self.m_listFileNode[nC1].Compare(self.m_listFileNode[nMinRoot]):
            nMinRoot = nC1

        if nC2 <= nLastIndex and self.m_listFileNode[nC2].Compare(self.m_listFileNode[nMinRoot]):
            nMinRoot = nC2

        if nMinRoot != nRoot:
            self._Swap(nMinRoot, nRoot)
            self._Heapify(nMinRoot, nLastIndex)

    def _Swap(self, nIndex1, nIndex2):
        self.m_listFileNode[nIndex1], self.m_listFileNode[nIndex2] = self.m_listFileNode[nIndex2], self.m_listFileNode[nIndex1]

    def Empty(self):
        return len(self.m_listFileNode) == 0

    def Top(self):
        return self.m_listFileNode[0].GetLog()

    def Pop(self):
        self.m_listFileNode[0].NextLog()
        if self.m_listFileNode[0].HasLog():
            pass
        else:
            self.m_listFileNode[0].Destroy()
            self._Swap(0, len(self.m_listFileNode) - 1)
            self.m_listFileNode.pop()

        self._Heapify(0, len(self.m_listFileNode) - 1)


class FileNode:
    def __init__(self, szFPath):
        self.m_szFPath = szFPath

        import common.my_path as my_path
        self.m_szFileName = my_path.FileName(szFPath)

        assert os.path.exists(szFPath), "文件目录必须存在: {0}".format(szFPath)
        self.m_fp = open(self.m_szFPath, 'r', encoding='utf-8')

        self.m_szCurLine = None
        self.m_nCurTime = None
        self.m_szNextLine = None

        self.m_TimeReObj = re.compile("^([0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}),([0-9]{3})")

        self.NextLog()

    def Destroy(self):
        self.m_fp.close()

    def Compare(self, FileNodeObj) -> bool:
        # self小，返回true，self大返回false
        return self.m_nCurTime < FileNodeObj.m_nCurTime

    def _IsRecordStart(self, szLine):
        return self._ParseTime(szLine) >= 0

    def _IsEnd(self, szLine):
        return szLine is ''

    def _ParseTime(self, szLine):
        MatchObj = self.m_TimeReObj.match(szLine)
        if MatchObj is None:
            return -1

        szTime = MatchObj.groups()[0]
        szValue = MatchObj.groups()[1]

        TimeStructObj = time.strptime(szTime, "%Y-%m-%d %H:%M:%S")
        nTimeStamp = int(time.mktime(TimeStructObj))

        nMS = int(szValue) * 0.001
        return nTimeStamp + nMS

    def GetLog(self):
        return self.m_szFileName.ljust(25) + self.m_szCurLine

    def NextLog(self):
        if self.m_szNextLine is None:
            self.m_szNextLine = self.m_fp.readline()

        if self._IsEnd(self.m_szNextLine):
            self.m_szCurLine = ""
            self.m_nCurTime = 0
            return

        szCurLine = self.m_szNextLine
        while True:
            szLine = self.m_fp.readline()
            if self._IsEnd(szLine):
                self.m_szNextLine = szLine
                break

            elif self._IsRecordStart(szLine):
                self.m_szNextLine = szLine
                break

            else:
                szCurLine += szLine

        self.m_szCurLine = szCurLine
        self.m_nCurTime = self._ParseTime(szCurLine)

    def HasLog(self):
        return self.m_nCurTime > 0
