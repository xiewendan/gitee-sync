# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2021/3/31 2:05

# desc:

class AcceptTaskMgr:
    def __init__(self):
        import common.my_log as my_log
        self.m_LoggerObj = my_log.MyLog(__file__)

        self.m_dictTask = {}
        self.m_listTask = []
        self.m_szCurTaskID = 0

    def AddTask(self, TaskObj):
        self.m_LoggerObj.debug("TaskID:%s", TaskObj.GetTaskId())

        szTaskId = TaskObj.GetTaskId()

        assert szTaskId not in self.m_dictTask
        self.m_dictTask[szTaskId] = TaskObj

        self.m_listTask.append(szTaskId)

    def Update(self, nCurTime):
        while self.m_szCurTaskID == 0 and len(self.m_listTask) > 0:
            szCurTaskID = self.m_listTask.pop(0)
            TaskObj = self.m_dictTask[szCurTaskID]

            if TaskObj.IsOverdue(nCurTime):
                del self.m_dictTask[szCurTaskID]
            else:
                self.m_szCurTaskID = szCurTaskID

        if self.m_szCurTaskID != 0:
            TaskObj = self.m_dictTask[self.m_szCurTaskID]
            TaskObj.Update()

    def ClearCurTask(self, szTaskId):
        self.m_LoggerObj.info("CurTaskID:%s", self.m_szCurTaskID)

        assert szTaskId == self.m_szCurTaskID
        assert self.m_szCurTaskID != 0

        del self.m_dictTask[self.m_szCurTaskID]

        self.m_szCurTaskID = 0


g_AcceptTaskMgr = AcceptTaskMgr()
AddTask = g_AcceptTaskMgr.AddTask
Update = g_AcceptTaskMgr.Update
ClearCurTask = g_AcceptTaskMgr.ClearCurTask
