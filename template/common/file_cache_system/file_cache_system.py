from .index_mgr import IndexMgr


class FileCacheSystem:
    """"""

    def __init__(self, szCacheFDir, nMaxTotalSize, bFullCheck=False, bDebug=False):
        import common.my_log as my_log
        self.m_LoggerObj = my_log.MyLog(__file__)

        import os
        assert nMaxTotalSize > 0
        assert os.path.exists(szCacheFDir)

        self.m_LoggerObj.info("szCacheFDir:%s, MaxTotalSize:%d", szCacheFDir, nMaxTotalSize)
        szCacheFDir = szCacheFDir.replace("\\", "/")

        self.m_szCacheFDir = szCacheFDir

        self.m_szFilesFDir = szCacheFDir + "/files"

        self.m_IndexMgrObj = IndexMgr(szCacheFDir + "/index.json", nMaxTotalSize)
        self.m_IndexMgrObj.LoadIndex()

        self._CheckCacheFile(bFullCheck)

        self.m_bDebug = bDebug

        self.m_nTotalSize = 0
        self.m_nMaxTotalSize = nMaxTotalSize

    def SaveFile(self, szMd5, szFileName, nSize, szSrcFPath):
        self.m_LoggerObj.info("md5:%s, filename:%s, size:%d, src_fpath:%s", szMd5, szFileName, nSize, szSrcFPath)

        import shutil
        import common.my_path as my_path

        # 调试状态检查索引和文件是否匹配
        if self.m_bDebug:
            assert self._CheckIndexMatchFile(szMd5, nSize, szSrcFPath, True)

        # 判断空间是否足够
        if not self.m_IndexMgrObj.CheckSpace(nSize):
            self._ClearSpace(nSize)

        # 创建文件
        szDestFPath = self._GenFPath(szMd5)
        my_path.CreateFileDir(szDestFPath)

        shutil.copy(szSrcFPath, szDestFPath)

        # 创建索引
        self.m_IndexMgrObj.AddFileIndex(szMd5, szFileName, nSize)

    def DelFile(self, szMd5):
        pass

    def LoadFile(self, szMd5, szFileName, nSize):
        pass

    def UseFile(self, szMd5, szFileName, nSize):
        pass

    def Destroy(self):
        self.m_LoggerObj.debug("")

        self.m_IndexMgrObj.SaveIndex()

    # ********************************************************************************
    # private
    # ********************************************************************************
    def _ClearSpace(self, nNeedSize):
        self.m_LoggerObj.info("NeedSize:%d", nNeedSize)

        import os

        listDelFile = self.m_IndexMgrObj.ClearSpace(nNeedSize)

        self.m_LoggerObj.info("to del file:%s", str(listDelFile))

        for szFPath in listDelFile:
            os.remove(szFPath)
            self.m_LoggerObj.info("del file:%s", szFPath)

    def _CheckCacheFile(self, bFullCheck):
        """
        确保索引和缓存文件两边一致
        所以索引，都有对应的缓存文件
        所有缓存文件，都可以在索引文件中找到记录
        """
        import os
        import common.util as util

        self.m_LoggerObj.debug("")

        dictFileIndex = self.m_IndexMgrObj.GetAllFileIndex()
        dictCacheFile = self._FindFiles(self.m_szFilesFDir)  # dictCacheFile[szMd5] = szFullPath

        # 清理没有索引的文件
        for szMd5, szFullPath in dictCacheFile.items():
            if szMd5 not in dictFileIndex:
                os.remove(szFullPath)
                self.m_LoggerObj.info("remove file without index:%s", szFullPath)

        # 检查索引和文件对比是否一致
        listErrorMd5 = []
        for szMd5, FileIndexObj in dictFileIndex.items():
            assert szMd5 in dictCacheFile, "有索引，没有文件:%s" % (szMd5,)

            nSize = FileIndexObj.Size
            szFPath = dictCacheFile[szMd5]

            if not self._CheckIndexMatchFile(szMd5, nSize, szFPath, bFullCheck):
                listErrorMd5.append(szMd5)

        # 删除有问题的索引信息和文件
        for szMd5 in listErrorMd5:
            self.m_IndexMgrObj.RemoveFileIndex(szMd5)

            szFPath = dictCacheFile[szMd5]
            util.RemoveFileDir(szFPath)

            self.m_LoggerObj.info("remove index and file not match:%s", szFPath)

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

    def _CheckIndexMatchFile(self, szIndexMd5, nIndexSize, szRealFPath, bFullCheck):
        """检查索引信息和文件信息是否匹配"""
        import os

        szIndexFPath = self._GenFPath(szIndexMd5)
        if szIndexFPath != szRealFPath:
            return False

        nRealSize = os.path.getsize(szRealFPath)
        if nIndexSize != nRealSize:
            return False

        if bFullCheck:
            import common.md5 as md5
            szRealMd5 = md5.GetFileMD5(szRealFPath)
            if szIndexMd5 != szRealMd5:
                return False

        return True
