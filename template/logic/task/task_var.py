# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2021/3/31 2:05

# desc:

import os
import logic.task.task_enum as task_enum


class TaskVar:
    """"""

    def __init__(self, szName: str, nType, nIotType, szFPath, szRPath):
        import common.my_log as my_log
        self.m_LoggerObj = my_log.MyLog(__file__)

        self.m_LoggerObj.debug("name:%s, type:%d, iot_type:%d, fpath:%s", szName, nType, nIotType, szFPath)

        self.m_szName = szName
        self.m_nType = nType
        self.m_nIotType = nIotType
        self.m_szFPath = szFPath
        self.m_szRPath = szRPath

        self.m_szMd5 = ""
        self.m_nSize = 0
        self.m_szFileName = ""

        self.m_szLocalFPath = ""
        self.m_szRemoteFPath = ""

        self.m_bDownloaded = False
        self.m_bError = False

        self.m_RequestReturnCb = None

    def Init(self):
        import os
        import common.md5 as md5
        import common.my_path as my_path

        self.m_szMd5 = md5.GetFileMD5(self.m_szFPath)
        self.m_nSize = os.path.getsize(self.m_szFPath)
        self.m_szFileName = my_path.FileNameWithExt(self.m_szFPath)

        self.m_LoggerObj.info("md5:%s, size:%d, filename:%s", self.m_szMd5, self.m_nSize, self.m_szFileName)

    def IsInput(self):
        return self.m_nIotType == task_enum.EIotType.eInput

    def IsOutput(self):
        return self.m_nIotType == task_enum.EIotType.eOutput

    def IsTemp(self):
        return self.m_nIotType == task_enum.EIotType.eTemp

    def IsError(self):
        return self.m_bError

    def IsDownloaded(self):
        return self.m_bDownloaded

    def GetLocalFPath(self):
        return self.m_szLocalFPath

    def GetName(self):
        return self.m_szName

    def GetValue(self):
        return self.m_szLocalFPath

    def ToDict(self):
        """
        :return:
        {
            "type": task_enum.EVarType.eFile/eDir,
            "iot": task_enum.EIotType.eInput/eOutput/eTemp,
            "fpath": "E:/project/xx/tools/template/data/test/etcpack.exe",
        }
        """
        return {
            "name": self.m_szName,
            "type": self.m_nType,
            "iot": self.m_nIotType,
            "fpath": self.m_szFPath,
            "rpath": self.m_szRPath,
            "md5": self.m_szMd5,
            "size": self.m_nSize,
            "file_name": self.m_szFileName,
        }

    def ToReturnDict(self):
        """
        :return:
        """
        return {
            "name": self.m_szName,
            "remote_fpath": self.m_szLocalFPath,
            "md5": self.m_szMd5,
            "size": self.m_nSize,
            "file_name": self.m_szFileName,
        }

    def Prepare(self, nFileExeConnID, szTaskID):
        assert self.IsInput()

        self.m_LoggerObj.info("name:%s", self.m_szName)

        import common.my_path as my_path
        self.m_szLocalFPath = "%s/data/temp/%s/%s" % (os.getcwd(), szTaskID, self.m_szRPath)
        my_path.CreateFileDir(self.m_szLocalFPath)

        if self.IsTemp():
            self.m_bDownloaded = True

        elif self.IsOutput():
            self.m_bDownloaded = True

        if self.IsInput():
            import common.file_cache_system.file_cache_system as file_cache_system
            if file_cache_system.CheckExistSameFile(self.m_szMd5, self.m_nSize, self.m_szFileName):
                szFPathInCacheSystem = file_cache_system.UseFile(self.m_szMd5, self.m_nSize, self.m_szFileName)

                my_path.Copy(szFPathInCacheSystem, self.m_szLocalFPath)

                self.m_bDownloaded = True
            else:
                import common.callback_mgr as callback_mgr
                nPrepareCbID = callback_mgr.CreateCb(self._PrepareDownloadFinish)
                self._Download(nFileExeConnID, szTaskID, self.m_szFPath, nPrepareCbID)

        else:
            assert False, "not support"

    def UpdateOutputValue(self, dictReturn):
        assert self.IsOutput()
        self.m_szMd5 = dictReturn["md5"]
        self.m_nSize = dictReturn["size"]
        self.m_szFileName = dictReturn["file_name"]
        self.m_szRemoteFPath = dictReturn["remote_fpath"]

    def RequestReturn(self, nConnID, szTaskId, RequestReturnCb):
        assert self.IsOutput()

        import common.callback_mgr as callback_mgr
        nReturnCbID = callback_mgr.CreateCb(self._ReturnDownloadFinish)
        self._Download(nConnID, szTaskId, self.m_szRemoteFPath, nReturnCbID)

        self.m_RequestReturnCb = RequestReturnCb

    # ********************************************************************************
    # private
    # ********************************************************************************
    def _Download(self, nFileExeConnID, szTaskID, szFPath, nCbID):
        import common.download_system.download_system as download_system
        import logic.connection.message_dispatcher as message_dispatcher

        listToDownloadBlockIndex = download_system.Download(self.m_szMd5, self.m_szFileName, self.m_nSize, nCbID)
        nBlockSize = download_system.GetBlockSize()

        for nBlockIndex in listToDownloadBlockIndex:
            dictData = {
                "md5": self.m_szMd5,
                "file_name": self.m_szFileName,
                "size": self.m_nSize,
                "block_index": nBlockIndex,
                "offset": nBlockSize * nBlockIndex,
                "block_size": nBlockSize,
                "file_fpath": szFPath
            }

            if dictData["offset"] + nBlockSize > self.m_nSize:
                dictData["block_size"] = self.m_nSize - dictData["offset"]

            message_dispatcher.CallRpc(nFileExeConnID, "logic.gm.gm_command", "OnDownloadFileRequest", [szTaskID, dictData])

    def _PrepareDownloadFinish(self, bOk=False):
        self.m_LoggerObj.info("varname:%s, ok:%s", self.m_szName, str(bOk))

        if bOk is True:
            import common.download_system.download_system as download_system
            szDownloadFPath = download_system.UseFile(self.m_szMd5, self.m_nSize, self.m_szFileName)
            assert szDownloadFPath != ""

            import common.file_cache_system.file_cache_system as file_cache_system
            file_cache_system.SaveFile(self.m_szMd5, self.m_nSize, self.m_szFileName, szDownloadFPath)
            szFPathInCacheSystem = file_cache_system.UseFile(self.m_szMd5, self.m_nSize, self.m_szFileName)

            import common.my_path as my_path
            my_path.Copy(szFPathInCacheSystem, self.m_szLocalFPath)

            self.m_bDownloaded = True
        else:
            self.m_bError = True

    def _ReturnDownloadFinish(self, bOk=False):
        self.m_LoggerObj.info("varname:%s, ok:%s", self.m_szName, str(bOk))

        if bOk is True:
            import common.download_system.download_system as download_system
            szDownloadFPath = download_system.UseFile(self.m_szMd5, self.m_nSize, self.m_szFileName)
            assert szDownloadFPath != ""

            import common.my_path as my_path
            my_path.Copy(szDownloadFPath, self.m_szFPath)

            self.m_bDownloaded = True
        else:
            self.m_bError = True

        self.m_RequestReturnCb(self.m_szName)
