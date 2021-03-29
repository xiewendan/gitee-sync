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
        self.m_szIp = ""
        self.m_nExePort = 0
        self.m_nFileExePort = 0
        self.m_szTaskID = dictTaskData["uuid"]
        self.m_eState = task_enum.ETaskState.eTodo
        self.m_nNextDisTime = 0

        self.m_listCB = []

        import logic.task.task_command as task_command
        for szCommand in dictTaskData["command"]:
            CommandObj = task_command.TaskCommand(szCommand)
            self.m_listCommand.append(CommandObj)

        import logic.task.task_var as task_var
        for szVarName, dictValue in dictTaskData["var"].items():
            nType = task_enum.EVarType.ToType(dictValue["type"])
            nIotType = task_enum.EIotType.ToType(dictValue["iot"])
            szFPath = dictValue["fpath"]

            TaskVarObj = task_var.TaskVar(szVarName, nType, nIotType, szFPath)
            self.m_dictVar[szVarName] = TaskVarObj

    def GetTaskId(self):
        return self.m_szTaskID

    def GenDict(self):
        pass

    @staticmethod
    def GetType(self):
        NotImplementedError

    def AddCB(self, FunCB, *args):
        import common.callback_mgr as callback_mgr
        nCallBackID = callback_mgr.CreateCb(FunCB, *args)

        assert nCallBackID not in self.m_listCB
        self.m_listCB.append(nCallBackID)

        return nCallBackID

    def OnCB(self):
        import common.callback_mgr as callback_mgr
        for nCallbackID in self.m_listCB:
            callback_mgr.Call(nCallbackID)

        self.m_listCB = []
