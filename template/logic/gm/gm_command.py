# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2021/3/18 21:06

# desc:

import os


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
    import logging
    logging.getLogger().info("")

    import common.my_path as my_path
    import common.callback_mgr as callback_mgr
    import common.download_system.download_system as download_system
    import logic.connection.message_dispatcher as message_dispatcher
    # TODO
    nConnID = 5

    nSize = 1026052571
    szMd5 = "ab67334b9bd3dc0349377738f0f0f97e"
    szFileFPath = os.getcwd().replace("\\", "/") + "/unit_test/test_data/file_cache_system/trunk__c74dcf98c_u74dcf98c.ipa"
    szFileName = my_path.FileNameWithExt(szFileFPath)

    def FunCB(name, nvalue, bOk=False):
        print("==============", name, nvalue, bOk)

    nCbID = callback_mgr.CreateCb(FunCB, "xjc", 1)
    listToDownloadBlockIndex = download_system.Download(szMd5, szFileName, nSize, nCbID)
    nBlockSize = download_system.GetBlockSize()

    for nBlockIndex in listToDownloadBlockIndex:
        dictData = {
            "md5": szMd5,
            "file_name": szFileName,
            "size": nSize,
            "block_index": nBlockIndex,
            "offset": nBlockSize * nBlockIndex,
            "block_size": nBlockSize,
            "file_fpath": szFileFPath
        }

        if dictData["offset"] + nBlockSize > nSize:
            dictData["block_size"] = nSize - dictData["offset"]

        message_dispatcher.CallRpc(nConnID, "logic.gm.gm_command", "OnDownloadFileRequest", [dictData])


def OnDownloadFileRequest(nConnID, dictData):
    assert "md5" in dictData
    assert "file_name" in dictData
    assert "size" in dictData
    assert "block_index" in dictData
    assert "offset" in dictData
    assert "block_size" in dictData
    assert "file_fpath" in dictData

    import logging
    logging.getLogger().info("ConnID:%d, dictData:%s", nConnID, Str(dictData))
    if not os.path.exists(dictData["file_fpath"]):
        logging.error("OnDownloadFileRequest error, file not exists:%s", dictData["file_fpath"])
        return

    # TODO
    nFileExeInExeConnID = 5
    import common.async_net.xx_connection_mgr as xx_connection_mgr
    xx_connection_mgr.SendFile(nFileExeInExeConnID, dictData)


def OnDownloadFileReceive(nConnID, dictData):
    import logging
    logging.getLogger().info("ConnID:%d, dictData:%s", nConnID, Str(dictData))

    import common.download_system.download_system as download_system
    szMd5 = dictData["md5"]
    szFileName = dictData["file_name"]
    nSize = dictData["size"]
    nBlockIndex = dictData["block_index"]
    byteDataBlock = dictData["byte_data_block"]

    download_system.Write(szMd5, szFileName, nSize, nBlockIndex, byteDataBlock)


def AddDisTask(nConnID, dictTaskData):
    import logging
    import logic.task.dis_task_mgr as dis_task_mgr
    logging.getLogger().info("ConnID:%d, dictTaskData:%s", nConnID, Str(dictTaskData))

    def TaskCB(nConnID, szTaskId):
        DisTaskObj = dis_task_mgr.GetTask(szTaskId)
        import logic.connection.message_dispatcher as message_dispatcher

        message_dispatcher.CallRpc(nConnID, "logic.gm.gm_command", "OnFinishTask", listArg)
        pass

    import logic.task.task_enum as task_enum
    import logic.task.task_factory as task_factory
    DisTaskObj = task_factory.TaskFactory.Create(task_enum.ETaskType.eDis, dictTaskData)
    DisTaskObj.AddCB(TaskCB, nConnID, DisTaskObj.GetTaskID())

    dis_task_mgr.AddTask(DisTaskObj)
    pass


def OnFinishTask(nConnID, dictTaskData):
    import main_frame.command.cmd_dis_task as cmd_dis_task
    cmd_dis_task.g_dictUUID2State[dictTaskData["uuid"]] = "True"


g_GmCommandMgr = GmCommandMgr()
Do = g_GmCommandMgr.Do
AddOutput = g_GmCommandMgr.AddOutput
