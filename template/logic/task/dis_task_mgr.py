class DisTaskMgr:
    def __init__(self):
        import common.my_log as my_log
        self.m_LoggerObj = my_log.MyLog(__file__)

        self.m_szIp = ""
        self.m_nExePort = 0
        self.m_nFileExePort = 0

        self.m_dictTask = {}

        self.m_listToDis = []

    def SetIpPort(self, szIp, nExePort, nFileExePort):
        self.m_szIp = szIp
        self.m_nExePort = nExePort
        self.m_nFileExePort = nFileExePort

    def GetIpPort(self):
        return self.m_szIp, self.m_nExePort, self.m_nFileExePort

    def AddTask(self, TaskObj):
        szTaskId = TaskObj.GetTaskId()
        self.m_LoggerObj.info("TaskId:%s", szTaskId)

        assert szTaskId not in self.m_dictTask
        self.m_dictTask[szTaskId] = TaskObj

        self.m_listToDis.append(TaskObj)

    def RemoveTask(self, szTaskId):
        assert szTaskId in self.m_dictTask
        del self.m_dictTask[szTaskId]
        self.m_LoggerObj.info("TaskId:%s", szTaskId)

    def GetTask(self, szTaskId):
        assert szTaskId in self.m_dictTask
        return self.m_dictTask[szTaskId]


g_DisTaskMgrObj = DisTaskMgr()
SetIpPort = g_DisTaskMgrObj.SetIpPort
GetIpPort = g_DisTaskMgrObj.GetIpPort
AddTask = g_DisTaskMgrObj.AddTask
GetTask = g_DisTaskMgrObj.GetTask
