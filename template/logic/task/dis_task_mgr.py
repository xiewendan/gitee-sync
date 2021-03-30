class DisTaskMgr:
    def __init__(self):
        import common.my_log as my_log
        self.m_LoggerObj = my_log.MyLog(__file__)

        self.m_szIp = ""
        self.m_nExePort = 0
        self.m_nFileExePort = 0
        self.m_nRegisterConnID = 0

        self.m_dictTask = {}

        self.m_listToDis = []

    def SetIpPort(self, szIp, nExePort, nFileExePort):
        self.m_szIp = szIp
        self.m_nExePort = nExePort
        self.m_nFileExePort = nFileExePort

    def GetIpPort(self):
        return self.m_szIp, self.m_nExePort, self.m_nFileExePort

    def SetRegisterConnID(self, nConnID):
        assert nConnID != 0
        self.m_nRegisterConnID = nConnID

    def GetRegisterConnID(self):
        return self.m_nRegisterConnID

    def AddTask(self, TaskObj):
        szTaskId = TaskObj.GetTaskId()
        self.m_LoggerObj.info("TaskId:%s", szTaskId)

        assert szTaskId not in self.m_dictTask
        self.m_dictTask[szTaskId] = TaskObj
        import common.xx_time as xx_time
        TaskObj.SetNextDisTime(xx_time.GetTime())

        self.m_listToDis.append(szTaskId)

    def RemoveTask(self, szTaskId):
        assert szTaskId in self.m_dictTask
        del self.m_dictTask[szTaskId]
        self.m_LoggerObj.info("TaskId:%s", szTaskId)

    def GetTask(self, szTaskId):
        assert szTaskId in self.m_dictTask
        return self.m_dictTask[szTaskId]

    def Update(self, nCurTime):
        import logic.connection.message_dispatcher as message_dispatcher
        import common.async_net.xx_connection_mgr as xx_connection_mgr
        import logic.task.task_enum as task_enum

        nRegisterConnID = self.GetRegisterConnID()
        if not xx_connection_mgr.IsConnected(nRegisterConnID):
            return

        for szTaskId in self.m_listToDis:
            TaskObj = self.m_dictTask[szTaskId]
            nNextDisTime = TaskObj.GetNextDisTime()
            if nNextDisTime < nCurTime:
                TaskObj.SetNextDisTime(nCurTime + task_enum.ETaskConst.eDisDeltaTime)
                message_dispatcher.CallRpc(nRegisterConnID, "logic.gm.gm_command", "OnRecvDisTask", [TaskObj.ToDict()])


g_DisTaskMgrObj = DisTaskMgr()
SetIpPort = g_DisTaskMgrObj.SetIpPort
GetIpPort = g_DisTaskMgrObj.GetIpPort
AddTask = g_DisTaskMgrObj.AddTask
GetTask = g_DisTaskMgrObj.GetTask
SetRegisterConnID = g_DisTaskMgrObj.SetRegisterConnID
GetRegisterConnID = g_DisTaskMgrObj.GetRegisterConnID
Update = g_DisTaskMgrObj.Update
