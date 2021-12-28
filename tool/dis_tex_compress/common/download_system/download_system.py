import os

from .index_mgr import IndexMgr
from .xx_file import XxFile


class DownloadSystem:
    """"""

    def __init__(self, szDownloadFDir=None, nMaxTotalSize=10000000000, nOverMilliSecond=300000, bFullCheck=False, nBlockSize=4000000):
        import common.my_log as my_log
        self.m_LoggerObj = my_log.MyLog(__file__)

        assert nMaxTotalSize > 0
        assert nBlockSize > 0

        self.m_szDownloadFDir = None
        self.m_szFilesFDir = None
        self.m_IndexMgrObj = None

        self.m_nBlockSize = nBlockSize

        self.m_bFullCheck = bFullCheck

        self.m_nOverMilliSecond = nOverMilliSecond

        self.m_nMaxTotalSize = nMaxTotalSize

        self.m_XxFileObj = None

        if szDownloadFDir is not None:
            self.Init(szDownloadFDir)

    def Init(self, szDownloadFDir):
        self.m_LoggerObj.info("Init download system! Base dir: %s", szDownloadFDir)
        szDownloadFDir = szDownloadFDir.replace("\\", "/")

        self.m_szDownloadFDir = szDownloadFDir

        self.m_szFilesFDir = szDownloadFDir + "/files"

        self.m_IndexMgrObj = IndexMgr(szDownloadFDir + "/index.json", self.m_nMaxTotalSize)

        self._CheckCacheFile()

    def _GetXxFile(self, szMd5, szFileFPath, nSize):
        if self.m_XxFileObj is not None:
            if not self.m_XxFileObj.CheckSame(szMd5, szFileFPath, nSize):
                self.m_XxFileObj.Close()
                self.m_XxFileObj = None

        if self.m_XxFileObj is None:
            self.m_XxFileObj = XxFile(szMd5, szFileFPath, nSize, "wb")

        return self.m_XxFileObj
    
    def _CloseXxFile(self):
        assert self.m_XxFileObj is not None
        self.m_XxFileObj.Close()
        self.m_XxFileObj = None

    def GetBlockSize(self):
        return self.m_nBlockSize

    def CheckExist(self, szMd5, szFileName, nSize):
        self.m_LoggerObj.debug("szMd5:%s, szFileName:%s, nSize:%d", szMd5, szFileName, nSize)

        return self.m_IndexMgrObj.CheckExistDownloaded(szMd5, szFileName, nSize)

    def Download(self, szMd5, szFileName, nSize, nCbID):
        self.m_LoggerObj.info("szMd5:%s, szFileName:%s, nSize:%d, nCbID:%d", szMd5, szFileName, nSize, nCbID)

        import common.my_path as my_path
        assert not self.CheckExist(szMd5, szFileName, nSize)

        if self.m_IndexMgrObj.CheckExistDownloading(szMd5, szFileName, nSize):
            self.m_LoggerObj.info("exist downloading")

            self.m_IndexMgrObj.AddCb(szMd5, nCbID)
            return self.m_IndexMgrObj.GetToDownloadBlockIndex(szMd5)

        # 删除相同Md5的旧文件
        szDestFPath = self._GenFPath(szMd5)
        if szMd5 in self.m_IndexMgrObj:
            listCb = self.m_IndexMgrObj.GetCbList(szMd5)
            self.m_IndexMgrObj.RemoveFileIndex(szMd5)
            self._CallCb(listCb)

            # noinspection PyBroadException
            try:
                os.remove(szDestFPath)
            except Exception as ExceptionObj:
                self.m_LoggerObj.error("remove file fail, szDestFPath:%s, exception:%s", szDestFPath, str(ExceptionObj))

        # 判断空间是否足够
        if not self.m_IndexMgrObj.CheckSpace(nSize):
            self._ClearSpace(nSize)

        # 创建空文件
        my_path.CreateFileDir(szDestFPath)
        XxFileObj = self._GetXxFile(szMd5, szDestFPath, nSize)
        XxFileObj.CheckSame(szMd5, szDestFPath, nSize)
        XxFileObj.Write(nSize - 1, b'e')

        # 创建索引
        import math
        listToDownloadBlockIndex = [nIndex for nIndex in range(0, math.ceil(nSize / self.m_nBlockSize))]

        self.m_IndexMgrObj.AddFileIndex(szMd5, szFileName, nSize, 0, self.m_nBlockSize, listToDownloadBlockIndex)
        self.m_IndexMgrObj.AddCb(szMd5, nCbID)
        self.m_LoggerObj.info("new downloading")

        return listToDownloadBlockIndex

    def Write(self, szMd5, szFileName, nSize, nBlockIndex, byteDataBlock):
        self.m_LoggerObj.info("szMd5:%s, szFileName:%s, nSize:%d, nBlockIndex:%d", szMd5, szFileName, nSize, nBlockIndex)

        assert self.m_IndexMgrObj.CheckExistDownloading(szMd5, szFileName, nSize), "发送到远端请求文件，结果本地下载缓存不够，把文件清除了就尴尬了"

        szDestFPath = self._GenFPath(szMd5)
        nBlockSize = self.m_IndexMgrObj.GetBlockSize(szMd5)

        nOffset = nBlockSize * nBlockIndex
        nDataSize = len(byteDataBlock)
        assert nDataSize == nBlockSize or nOffset + nDataSize == nSize

        # 更新文件
        XxFileObj = self._GetXxFile(szMd5, szDestFPath, nSize)
        XxFileObj.CheckSame(szMd5, szDestFPath, nSize)
        XxFileObj.Write(nOffset, byteDataBlock)

        # 更新索引
        self.m_IndexMgrObj.UpdateFileIndex(szMd5, nBlockIndex, nDataSize)

        # 检查是否完成
        if not self.m_IndexMgrObj.CheckExistDownloaded(szMd5, szFileName, nSize):
            return

        self._CloseXxFile()

        # 下载完成检查
        self.m_LoggerObj.info("file downloaded, md5:%s, filename:%s", szMd5, szFileName)

        bMd5Ok = True
        if self.m_bFullCheck:
            import common.md5 as md5
            szRealMd5 = md5.GetFileMD5(szDestFPath)
            bMd5Ok = szMd5 == szRealMd5
            if not bMd5Ok:
                self.m_LoggerObj.error("md5 not match, md5:%s, realmd5:%s, DestFPath:%s", szMd5, szRealMd5, szDestFPath)

        # 调用回调
        listCb = self.m_IndexMgrObj.GetCbList(szMd5)
        self.m_IndexMgrObj.RemoveCbList(szMd5)
        self._CallCb(listCb, bMd5Ok)

    def UseFile(self, szMd5, szFileName, nSize):
        self.m_LoggerObj.debug("Md5:%s, FileName:%s, Size:%d", szMd5, szFileName, nSize)
        szDestFPath = self._GenFPath(szMd5)
        if not self.m_IndexMgrObj.CheckExistDownloaded(szMd5, szFileName, nSize) and \
                not self.m_IndexMgrObj.CheckExistDownloading(szMd5, szFileName, nSize):
            return ""

        if not os.path.exists(szDestFPath):
            return ""

        self.m_IndexMgrObj.F_UpdateUseTime(szMd5)

        return szDestFPath

    def CheckOvertime(self):
        import time
        import math

        nCurTime = math.floor(time.time() * 1000)

        dictFileIndex = self.m_IndexMgrObj.GetAllFileIndex()
        for szMd5, FileIndexObj in dictFileIndex.items():
            if nCurTime - FileIndexObj.LastUseTime >= self.m_nOverMilliSecond:
                self.m_LoggerObj.error("over time file, szMd5:%s, filename:%s", szMd5, FileIndexObj.FileName)

                listCb = self.m_IndexMgrObj.GetCbList(szMd5)
                self.m_IndexMgrObj.RemoveCbList(szMd5)
                self._CallCb(listCb, False)

    def Destroy(self):
        self.m_LoggerObj.debug("")

        self.m_IndexMgrObj.SaveIndex()

    def T_GetDownloadData(self):
        """用于测试，获得所有下载的数据"""
        import json

        dictFileIndex = self.m_IndexMgrObj.GetAllFileIndex()
        listRet = []
        for _, FileIndexObj in dictFileIndex.items():
            listRet.append(FileIndexObj.T_ToList())

        szJsonData = json.dumps(listRet, indent=4)

        return szJsonData

    # ********************************************************************************
    # private
    # ********************************************************************************
    def _CallCb(self, listCb, bMd5Ok=False):
        import common.callback_mgr as callback_mgr
        for nCbID in listCb:
            callback_mgr.Call(nCbID, bOk=bMd5Ok)

    def _ClearSpace(self, nNeedSize):
        self.m_LoggerObj.info("NeedSize:%d", nNeedSize)

        listDelFile, listDelCb = self.m_IndexMgrObj.ClearSpace(nNeedSize)
        self._CallCb(listDelCb)

        self.m_LoggerObj.info("to del file:%s", str(listDelFile))

        for szMd5 in listDelFile:
            szFPath = self._GenFPath(szMd5)
            # noinspection PyBroadException
            try:
                os.remove(szFPath)
            except Exception as ExceptionObj:
                self.m_LoggerObj.fatal("clear space to remove file failed, file path:%s, ExceptionObj:%s", szFPath, str(ExceptionObj))
            else:
                self.m_LoggerObj.info("del file:%s", szFPath)

    def _CheckCacheFile(self):
        """
        确保索引和缓存文件两边一致
        所以索引，都有对应的缓存文件
        所有缓存文件，都可以在索引文件中找到记录
        """
        import os

        self.m_LoggerObj.debug("")

        dictFileIndex = self.m_IndexMgrObj.GetAllFileIndex()
        dictCacheFile = self._FindFiles(self.m_szFilesFDir)  # dictCacheFile[szMd5] = szFullPath

        # 清理没有索引的文件
        for szMd5, szFullPath in dictCacheFile.items():
            if szMd5 not in dictFileIndex:
                os.remove(szFullPath)
                self.m_LoggerObj.info("remove file without index:%s", szFullPath)

        # 清理空文件夹
        import common.my_path as my_path
        my_path.ClearEmptyDir(self.m_szFilesFDir)
        self.m_LoggerObj.info("Clean empty dir")

    @staticmethod
    def _FindFiles(szFullDir):
        import os
        import common.my_path as my_path

        dictFile = {}

        for szParentFPath, _, listFileName in os.walk(szFullDir):
            import os
            for szFileName in listFileName:
                szFullPath = os.path.join(szParentFPath, szFileName)
                szDirName = my_path.FileName(szParentFPath)
                szMd5 = szDirName + szFileName

                dictFile[szMd5] = szFullPath.replace("\\", "/")

        return dictFile

    def _GenFPath(self, szMd5):
        """根据md5生成完整的文件路径"""
        szDir = szMd5[:2]
        szFileName = szMd5[2:]
        return "%s/%s/%s" % (self.m_szFilesFDir, szDir, szFileName)


# g_szDownloadFDir = os.getcwd() + "/data/download_system"

g_DownloadSystem = DownloadSystem()
Init = g_DownloadSystem.Init
Download = g_DownloadSystem.Download
Write = g_DownloadSystem.Write
CheckOvertime = g_DownloadSystem.CheckOvertime
UseFile = g_DownloadSystem.UseFile
GetBlockSize = g_DownloadSystem.GetBlockSize

T_GetDownloadData = g_DownloadSystem.T_GetDownloadData
