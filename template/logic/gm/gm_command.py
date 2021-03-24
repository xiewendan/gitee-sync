# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2021/3/18 21:06

# desc:

class GmCommandMgr:
    def __init__(self):
        import common.my_log as my_log
        self.m_LoggerObj = my_log.MyLog(__file__)

        self.m_listOutput = []

    def _ClearOutput(self):
        self.m_listOutput = []

    def AddOutput(self, szMsg):
        self.m_listOutput.append(szMsg)

    def Do(self, nID, szCommand):
        self.m_LoggerObj.debug("id:%d, command:%s", nID, szCommand)

        self._ClearOutput()

        exec(szCommand)

        szOutput = "\n".join(self.m_listOutput)
        self._ClearOutput()

        return {"ret": szOutput}


def TestDo():
    nIndex = 10
    nIndex += 20

    AddOutput("xjc")
    AddOutput(str(nIndex))


def GetAllExecutorData():
    import logic.register.executor_mgr as executor_mgr
    szExecutorData = executor_mgr.ExecutorDataToStr()

    AddOutput(szExecutorData)


def GetAllConnectionData():
    import common.async_net.xx_connection_mgr as xx_connection_mgr
    szData = xx_connection_mgr.GetAllDataStr()

    AddOutput(szData)


def GetDownloadData():
    import common.download_system.download_system as download_system
    szData = download_system.T_GetDownloadData()

    AddOutput(szData)


def DownloadFile():
    import common.download_system.download_system as download_system
    import logic.connection.message_dispatcher as message_dispatcher
    nConnID = 100
    nSize = 28160
    szMd5 = "9767f3103c55c66cc2c9eb39d56db594"
    szFileName = "E:/project/xiewendan/tools/template/unit_test/test_data/file_cache_system/1.data"
    listFileBlock = download_system.Download(szMd5, szFileName, nSize)

    for FileBlockObj in listFileBlock:
        dictData = {
            # TODO
            "md5": FileBlockObj[0],
            "file_name": FileBlockObj[1],
            "size": FileBlockObj[2],
            "block_index": FileBlockObj[3],
            "offset": FileBlockObj[4],
            "block_size": FileBlockObj[5],
        }

        message_dispatcher.CallRpc(nConnID, "logic.gm.gm_command", "OnDownloadFileRequest", [dictData])


def OnDownloadFileRequest(nConnID, dictData):
    import common.async_net.xx_connection_mgr as xx_connection_mgr
    xx_connection_mgr.SendFile(nConnID, dictData)


def OnDownloadFileReceive(nConnID, dictData):
    import common.download_system.download_system as download_system
    szMd5 = dictData["md5"]
    szFileName = dictData["file_name"]
    nSize = dictData["size"]
    nBlockIndex = dictData["block_index"]
    byteDataBlock = dictData["data_block"]

    download_system.Write(szMd5, szFileName, nSize, nBlockIndex, byteDataBlock)


g_GmCommandMgr = GmCommandMgr()
Do = g_GmCommandMgr.Do
AddOutput = g_GmCommandMgr.AddOutput
