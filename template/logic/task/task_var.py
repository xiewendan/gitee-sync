import os
import logic.task.task_enum as task_enum


class TaskVar:
    """"""

    def __init__(self, szName: str, nType, nIotType, szFPath):
        import common.my_log as my_log
        self.m_LoggerObj = my_log.MyLog(__file__)

        self.m_LoggerObj.debug("name:%s, type:%d, iot_type:%d, fpath:%s", szName, nType, nIotType, szFPath)

        self.m_szName = szName
        self.m_nType = nType
        self.m_nIotType = nIotType
        self.m_szFPath = szFPath

        self.m_szMd5 = ""
        self.m_nSize = 0
        self.m_szFileName = ""

        self.m_szLocalFPath = ""

        self.m_bDownloaded = False
        self.m_bError = False

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
            "md5": self.m_szMd5,
            "size": self.m_nSize,
            "file_name": self.m_szFileName,
        }

    def Prepare(self, nExeConnID):
        assert self.IsInput()

        self.m_LoggerObj.info("name:%s", self.m_szName)

        if self.IsInput():
            import common.file_cache_system.file_cache_system as file_cache_system
            if file_cache_system.CheckExistSameFile(self.m_szMd5, self.m_nSize, self.m_szFileName):
                self.m_szLocalFPath = file_cache_system.UseFile(self.m_szMd5, self.m_nSize, self.m_szFileName)
                self.m_bDownloaded = True
                return

            self._Download(nExeConnID)

        elif self.IsTemp():
            self.m_szLocalFPath = "%s/data/temp/%s" % (os.getcwd(), self.m_szMd5)
            self.m_bDownloaded = True

        elif self.IsOutput():
            self.m_szLocalFPath = "%s/data/temp/%s" % (os.getcwd(), self.m_szMd5)
            self.m_bDownloaded = True

    def _Download(self, nExeConnID):
        import common.callback_mgr as callback_mgr
        import common.download_system.download_system as download_system
        import logic.connection.message_dispatcher as message_dispatcher

        nCbID = callback_mgr.CreateCb(self._DownloadFinish)
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
                "file_fpath": self.m_szFPath
            }

            if dictData["offset"] + nBlockSize > self.m_nSize:
                dictData["block_size"] = self.m_nSize - dictData["offset"]

            message_dispatcher.CallRpc(nExeConnID, "logic.gm.gm_command", "OnDownloadFileRequest", [dictData])

    def _DownloadFinish(self, bOk=False):
        self.m_LoggerObj.info("ok:%s", str(bOk))

        if bOk is True:
            import common.file_cache_system.file_cache_system as file_cache_system
            self.m_szLocalFPath = file_cache_system.UseFile(self.m_szMd5, self.m_nSize, self.m_szFileName)
            self.m_bDownloaded = True
        else:
            self.m_bError = True

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
