# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2021/3/31 2:05

# desc:

import logging


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
        self.m_LoggerObj.debug("ip:%s, ExePort:%d, FileExePort:%d", szIp, nExePort, nFileExePort)

        self.m_szIp = szIp
        self.m_nExePort = nExePort
        self.m_nFileExePort = nFileExePort

    def GetIpPort(self):
        return self.m_szIp, self.m_nExePort, self.m_nFileExePort

    def SetRegisterConnID(self, nConnID):
        self.m_LoggerObj.debug("nConnID:%d", nConnID)

        assert nConnID != 0
        self.m_nRegisterConnID = nConnID

    def _GetRegisterConnID(self):
        return self.m_nRegisterConnID

    def AddTask(self, TaskObj):
        import logic.task.task_enum as task_enum

        szTaskId = TaskObj.GetTaskId()
        self.m_LoggerObj.info("Add task, Id:%s", szTaskId)

        assert szTaskId not in self.m_dictTask
        self.m_dictTask[szTaskId] = TaskObj

        import common.xx_time as xx_time
        TaskObj.SetNextDisTime(xx_time.GetTime(), "Add Task")

        self.m_listToDis.append(szTaskId)

    def RemoveTask(self, szTaskId):
        assert szTaskId in self.m_dictTask
        del self.m_dictTask[szTaskId]
        self.m_listToDis.remove(szTaskId)
        self.m_LoggerObj.info("TaskId:%s", szTaskId)

    def GetTask(self, szTaskId):
        assert szTaskId in self.m_dictTask
        return self.m_dictTask[szTaskId]

    def Update(self, nCurTime):
        import logic.task.task_enum as task_enum
        import common.async_net.xx_connection_mgr as xx_connection_mgr
        import logic.connection.message_dispatcher as message_dispatcher

        nRegisterConnID = self._GetRegisterConnID()
        if not xx_connection_mgr.IsConnected(nRegisterConnID):
            return

        # 遍历发布任务
        listSucceedTaskId = []
        for szTaskId in self.m_listToDis:
            TaskObj = self.m_dictTask[szTaskId]
            if TaskObj.IsSucceed():
                listSucceedTaskId.append(szTaskId)
                continue

            if TaskObj.IsOverdue(nCurTime):
                self.m_LoggerObj.warn("task overdue:%s", szTaskId)

                TaskObj.SetNextDisTime(nCurTime + task_enum.ETaskConst.eDisDeltaTime, "task overdue")
                message_dispatcher.CallRpc(nRegisterConnID, "logic.gm.gm_command", "OnRecvDisTask", [TaskObj.ToDict()])

        # 遍历处理成功的任务
        for szTaskId in listSucceedTaskId:
            TaskObj = self.m_dictTask[szTaskId]
            assert TaskObj.IsSucceed()

            self.RemoveTask(szTaskId)
            TaskObj.OnCB()
            TaskObj.Destroy()

            self.m_LoggerObj.info("task succeed:%s", szTaskId)

        assert len(self.m_dictTask) == len(self.m_listToDis)


g_DisTaskMgrObj = DisTaskMgr()
SetIpPort = g_DisTaskMgrObj.SetIpPort
GetIpPort = g_DisTaskMgrObj.GetIpPort
AddTask = g_DisTaskMgrObj.AddTask
GetTask = g_DisTaskMgrObj.GetTask
SetRegisterConnID = g_DisTaskMgrObj.SetRegisterConnID
Update = g_DisTaskMgrObj.Update
