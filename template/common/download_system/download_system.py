import os

from .index_mgr import IndexMgr


class DownloadSystem:
    """"""

    def __init__(self, szDownloadFDir, nMaxTotalSize, nOverMilliSecond=300000, bFullCheck=False, nBlockSize=2000000):
        import common.my_log as my_log
        self.m_LoggerObj = my_log.MyLog(__file__)

        import os
        assert nMaxTotalSize > 0
        assert nBlockSize > 0
        assert os.path.exists(szDownloadFDir)

        self.m_LoggerObj.info("szDownloadFDir:%s, MaxTotalSize:%d", szDownloadFDir, nMaxTotalSize)
        szDownloadFDir = szDownloadFDir.replace("\\", "/")

        self.m_szDownloadFDir = szDownloadFDir

        self.m_szFilesFDir = szDownloadFDir + "/files"

        self.m_IndexMgrObj = IndexMgr(szDownloadFDir + "/index.json", nMaxTotalSize)

        self.m_nBlockSize = nBlockSize

        self._CheckCacheFile(bFullCheck)

        self.m_bFullCheck = bFullCheck

        self.m_nOverMilliSecond = nOverMilliSecond

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
            self.m_IndexMgrObj.AddCb(szMd5, nCbID)
            return self.m_IndexMgrObj.GetToDownloadBlockIndex(szMd5)

        # 删除相同Md5的旧文件
        szDestFPath = self._GenFPath(szMd5)
        if szMd5 in self.m_IndexMgrObj:
            self.m_IndexMgrObj.RemoveFileIndex(szMd5)
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
        with open(szDestFPath, "wb"):
            pass

        # 创建索引
        import math
        listToDownloadBlockIndex = [nIndex for nIndex in range(0, math.ceil(nSize / self.m_nBlockSize))]

        self.m_IndexMgrObj.AddFileIndex(szMd5, szFileName, nSize, 0, self.m_nBlockSize, listToDownloadBlockIndex)

        return listToDownloadBlockIndex

    def Write(self, szMd5, szFileName, nSize, nBlockIndex, byteDataBlock):
        self.m_LoggerObj.debug("szMd5:%s, szFileName:%s, nSize:%d, nBlockIndex:%d", szMd5, szFileName, nSize, nBlockIndex)

        assert self.m_IndexMgrObj.CheckExistDownloading(szMd5, szFileName, nSize), "发送到远端请求文件，结果本地下载缓存不够，把文件清除了就尴尬了"

        szDestFPath = self._GenFPath(szMd5)
        nBlockSize = self.m_IndexMgrObj.GetBlockSize(szMd5)

        nOffset = nBlockSize * nBlockIndex
        nDataSize = len(byteDataBlock)
        assert nDataSize == nBlockSize or nOffset + nDataSize == nSize

        # 更新文件
        with open(szDestFPath, "wb") as FileObj:
            FileObj.seek(nOffset)
            FileObj.write(byteDataBlock)

        # 更新索引
        self.m_IndexMgrObj.UpdateFileIndex(szMd5, nBlockIndex, nDataSize)

        # 检查是否完成
        if not self.m_IndexMgrObj.CheckExistDownloaded(szMd5, szFileName, nSize):
            return

        # 下载完成检查
        self.m_LoggerObj.info("file downloaded, md5:%s, filename:%s", szMd5, szFileName)

        bMd5Ok = True
        if self.m_bFullCheck:
            import common.md5 as md5
            szRealMd5 = md5.GetFileMD5(szDestFPath)
            bMd5Ok = szMd5 != szRealMd5
            if not bMd5Ok:
                self.m_LoggerObj.error("md5 not match, md5:%s, realmd5:%s", szMd5, szRealMd5)

        # 调用回调
        listCb = self.m_IndexMgrObj.GetCbList(szMd5)
        import common.callback_mgr as callback_mgr
        for nCbID in listCb:
            callback_mgr.Call(nCbID, bOk=bMd5Ok)

        self.m_IndexMgrObj.RemoveCbList(szMd5)

    def CheckOvertime(self):
        import time
        import math
        import common.callback_mgr as callback_mgr

        nCurTime = math.floor(time.time() * 1000)

        dictFileIndex = self.m_IndexMgrObj.GetAllFileIndex()
        for szMd5, FileIndexObj in dictFileIndex.items():
            if nCurTime - FileIndexObj.LastUseTime() >= self.m_nOverMilliSecond:
                self.m_LoggerObj.error("over time file, szMd5:%s, filename:%s", szMd5, FileIndexObj.FileName)

                listCb = self.m_IndexMgrObj.GetCbList(szMd5)
                for nCbID in listCb:
                    callback_mgr.Call(nCbID, bOk=False)

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
    def _ClearSpace(self, nNeedSize):
        self.m_LoggerObj.info("NeedSize:%d", nNeedSize)

        listDelFile = self.m_IndexMgrObj.ClearSpace(nNeedSize)

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

    def _CheckCacheFile(self, bFullCheck):
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
        self.m_LoggerObj.info("clean empty dir")

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


szDownloadFDir = os.getcwd() + "/data/download_system"
nMaxTotalSize = 10000000000
g_DownloadSystem = DownloadSystem(szDownloadFDir, nMaxTotalSize)
Download = g_DownloadSystem.Download
Write = g_DownloadSystem.Write
CheckOvertime = g_DownloadSystem.CheckOvertime
T_GetDownloadData = g_DownloadSystem.T_GetDownloadData
GetBlockSize = g_DownloadSystem.GetBlockSize
