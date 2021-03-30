class AcceptTaskMgr:
    def __init__(self):
        import common.my_log as my_log
        self.m_LoggerObj = my_log.MyLog(__file__)

        self.m_dictTask = {}
        self.m_listTask = []
        self.m_szCurTaskID = 0

    def AddTask(self, TaskObj):
        self.m_LoggerObj.debug("TaskID:%s", TaskObj.GetTaskID())

        szTaskID = TaskObj.GetTaskID()
        assert szTaskID not in self.m_dictTask
        self.m_dictTask[szTaskID] = TaskObj

        self.m_listTask.append(szTaskID)

    def Update(self, nCurTime):
        while self.m_szCurTaskID == 0 and len(self.m_listTask) > 0:
            szCurTaskID = self.m_listTask.pop(0)
            TaskObj = self.m_dictTask[szCurTaskID]
            nNextDisTime = TaskObj.GetNextDisTime()

            if nCurTime < nNextDisTime:
                self.m_szCurTaskID = szCurTaskID
            else:
                del self.m_dictTask[szCurTaskID]

        if self.m_szCurTaskID != 0:
            TaskObj = self.m_dictTask[self.m_szCurTaskID]
            TaskObj.Update()

    def ClearCurTask(self):
        assert self.m_szCurTaskID != 0
        del self.m_dictTask[self.m_szCurTaskID]
        self.m_szCurTaskID = 0


g_AcceptTaskMgr = AcceptTaskMgr()
AddTask = g_AcceptTaskMgr.AddTask
Update = g_AcceptTaskMgr.Update
