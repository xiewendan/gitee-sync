# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2021/3/31 2:05

# desc:

import common.my_log as my_log
import logic.task.task_enum as task_enum


class BaseTask:
    """"""

    def __init__(self, dictTaskData):
        """
        :param dictTaskData:
        {
            "uuid": szTaskUuid,
            "command": [
                "{{exe_fpath}} {{tga_file}} {{temp_dir}}  -s fast -c etc2 -f RGBA -ktx"
            ],
            "var": {
                "exe_fpath": {
                    "type": "file",
                    "iot": "input",
                    "fpath": "E:/project/xx/tools/template/data/test/etcpack.exe",
                },
                "tga_file": {
                    "type": "file",
                    "iot": "input",
                    "fpath": "E:/project/xx/tools/template/data/test/cqs_ground_06.tga",
                },
                "temp_dir": {
                    "type": "dir",
                    "iot": "temp",
                    "fpath": "E:/project/xx/tools/template/data/test/cqs_ground_06.ktx",
                },
                "ktx_file": {
                    "type": "file",
                    "iot": "output",
                    "fpath": "E:/project/xx/tools/template/data/test/cqs_ground_06.ktx/cqs_ground_06.ktx",
                }
            },
        }
        """
        self.m_LoggerObj = my_log.MyLog(__file__)
        self.m_LoggerObj.debug("dictTaskData:%s", Str(dictTaskData))

        self.m_listCommand = []
        self.m_dictVar = {}
        self.m_szIp = dictTaskData.get("ip", "")
        self.m_nExePort = dictTaskData.get("exe_port", 0)
        self.m_nFileExePort = dictTaskData.get("file_exe_port", 0)
        self.m_szTaskId = dictTaskData["uuid"]
        self.m_eState = task_enum.ETaskState.eNone
        self.m_nNextDisTime = dictTaskData.get("next_dis_time", 0)

        self.m_listCB = []

        import logic.task.task_command as task_command
        for szCommand in dictTaskData["command"]:
            CommandObj = task_command.TaskCommand(szCommand)
            self.m_listCommand.append(CommandObj)

        import logic.task.task_var as task_var
        for szVarName, dictValue in dictTaskData["var"].items():
            TaskVarObj = task_var.TaskVar(szVarName, dictValue)
            self.m_dictVar[szVarName] = TaskVarObj

    def GetTaskId(self):
        return self.m_szTaskId

    def ToDict(self):
        """
        :return:
        {
            "uuid": szTaskUuid,
            "command": [
                "{{exe_fpath}} {{tga_file}} {{temp_dir}}  -s fast -c etc2 -f RGBA -ktx"
            ],
            "var": {
                "exe_fpath": {
                    "type": "file",
                    "iot": "input",
                    "fpath": "E:/project/xx/tools/template/data/test/etcpack.exe",
                },
                "tga_file": {
                    "type": "file",
                    "iot": "input",
                    "fpath": "E:/project/xx/tools/template/data/test/cqs_ground_06.tga",
                },
                "temp_dir": {
                    "type": "dir",
                    "iot": "temp",
                    "fpath": "E:/project/xx/tools/template/data/test/cqs_ground_06.ktx",
                },
                "ktx_file": {
                    "type": "file",
                    "iot": "output",
                    "fpath": "E:/project/xx/tools/template/data/test/cqs_ground_06.ktx/cqs_ground_06.ktx",
                }
            },
        }
        """
        dictData = {
            "uuid": self.m_szTaskId,
            "command": self._GetCommandList(),
            "var": self._GetVarDict(),
            "ip": self.m_szIp,
            "exe_port": self.m_nExePort,
            "file_exe_port": self.m_nFileExePort,
            "next_dis_time": self.m_nNextDisTime,
        }

        return dictData

    @staticmethod
    def GetType():
        NotImplementedError

    def AddCB(self, FunCB, *args):
        self.m_LoggerObj.debug("TaskId:%s", self.m_szTaskId)

        import common.callback_mgr as callback_mgr
        nCallBackID = callback_mgr.CreateCb(FunCB, *args)

        assert nCallBackID not in self.m_listCB
        self.m_listCB.append(nCallBackID)

        return nCallBackID

    def OnCB(self):
        self.m_LoggerObj.debug("TaskId:%s", self.m_szTaskId)

        import common.callback_mgr as callback_mgr
        for nCallbackID in self.m_listCB:
            callback_mgr.Call(nCallbackID)

        self.m_listCB = []

    def SetNextDisTime(self, nNextDisTime):
        self.m_LoggerObj.debug("taskid:%s, curdistime:%d, nextdistime:%d", self.m_szTaskId, self.m_nNextDisTime, nNextDisTime)
        self.m_nNextDisTime = max(nNextDisTime, self.m_nNextDisTime)

    def GetNextDisTime(self):
        return self.m_nNextDisTime

    def IsOverdue(self, nCurTime=None):
        if nCurTime is None:
            import common.xx_time as xx_time
            nCurTime = xx_time.GetTime()

        return nCurTime > self.m_nNextDisTime

    # ********************************************************************************
    # private
    # ********************************************************************************
    def _GetCommandList(self):
        listCommand = []
        for CommandObj in self.m_listCommand:
            listCommand.append(CommandObj.ToStr())

        return listCommand

    def _GetVarDict(self):
        dictRet = {}
        for szName, VarObj in self.m_dictVar.items():
            dictRet[szName] = VarObj.ToDict()

        return dictRet
