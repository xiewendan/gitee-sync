# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2021/3/20 13:02

# desc:


__all__ = ["FileCacheSystem"]

import os
import shutil

from .index_mgr import IndexMgr


class FileCacheSystem:
    def __init__(self, szCacheFDir=None, nMaxTotalSize=10000000000, bFullCheck=False, bDebug=False):
        import common.my_log as my_log
        self.m_LoggerObj = my_log.MyLog(__file__)

        assert nMaxTotalSize > 0

        self.m_szCacheFDir = None
        self.m_szFilesFDir = None
        self.m_IndexMgrObj = None

        self.m_nMaxTotalSize = nMaxTotalSize
        self.m_bFullCheck = bFullCheck
        self.m_bDebug = bDebug

        if szCacheFDir is not None:
            self.Init(szCacheFDir)

    def Init(self, szCacheFDir):
        self.m_LoggerObj.info("szCacheFDir:%s", szCacheFDir)
        szCacheFDir = szCacheFDir.replace("\\", "/")

        self.m_szCacheFDir = szCacheFDir
        self.m_szFilesFDir = szCacheFDir + "/files"
        self.m_IndexMgrObj = IndexMgr(szCacheFDir + "/index.json", self.m_nMaxTotalSize)

        self._CheckCacheFile(self.m_bFullCheck)

    def CheckExistSameFile(self, szMd5, szFileName, nSize):
        """是否存在相同文件"""
        return self.m_IndexMgrObj.CheckExist(szMd5, szFileName, nSize)

    def SaveFile(self, szMd5, szFileName, nSize, szSrcFPath):
        """调用之前，请先检查CheckExistSameFile"""
        self.m_LoggerObj.info("md5:%s, filename:%s, size:%d, src_fpath:%s", szMd5, szFileName, nSize, szSrcFPath)

        assert not self.CheckExistSameFile(szMd5, szFileName, nSize), "调用之前，需要先确保没有相同的文件"

        import common.my_path as my_path

        # 调试状态检查索引和文件是否匹配
        if self.m_bDebug:
            assert self._CheckIndexMatchFile(szMd5, nSize, szSrcFPath, True)

        # 删除相同Md5的旧文件
        szDestFPath = self._GenFPath(szMd5)
        assert szSrcFPath != szDestFPath
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

        # 创建文件
        my_path.CreateFileDir(szDestFPath)
        shutil.copy(szSrcFPath, szDestFPath)
        self.m_LoggerObj.debug("copy file from %s to %s", szSrcFPath, szDestFPath)

        if self.m_bFullCheck:
            import common.md5 as md5
            szRealMd5 = md5.GetFileMD5(szDestFPath)
            assert szRealMd5 == szMd5

        # 创建索引
        self.m_IndexMgrObj.AddFileIndex(szMd5, szFileName, nSize)

    def UseFile(self, szMd5, szFileName, nSize):
        self.m_LoggerObj.debug("Md5:%s, FileName:%s, Size:%d", szMd5, szFileName, nSize)
        szDestFPath = self._GenFPath(szMd5)
        if not self.CheckExistSameFile(szMd5, szFileName, nSize):
            return ""

        if not os.path.exists(szDestFPath):
            return ""

        self.m_IndexMgrObj.RemoveFileIndex(szMd5)
        self.m_IndexMgrObj.AddFileIndex(szMd5, szFileName, nSize)

        return szDestFPath

    def Destroy(self):
        self.m_LoggerObj.debug("")

        self.m_IndexMgrObj.SaveIndex()

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


# g_szCacheFDir = os.getcwd() + "/data/cache_system"
g_FileCacheSystem = FileCacheSystem()
Init = g_FileCacheSystem.Init
CheckExistSameFile = g_FileCacheSystem.CheckExistSameFile
UseFile = g_FileCacheSystem.UseFile
SaveFile = g_FileCacheSystem.SaveFile
