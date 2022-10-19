# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2021/3/31 2:05

# desc:

import logic.task.base_task as tasK_base
import logic.task.task_enum as task_enum


class DisTask(tasK_base.BaseTask):

    def __init__(self, dictTaskData):
        super().__init__(dictTaskData)

        for szName, VarObj in self.m_dictVar.items():
            if VarObj.IsInput():
                VarObj.InitInput()

        import logic.task.dis_task_mgr as dis_task_mgr
        szIp, nExePort, nFileExePort = dis_task_mgr.GetIpPort()

        self.m_szIp = szIp
        self.m_nExePort = nExePort
        self.m_nFileExePort = nFileExePort

        self.m_eState = task_enum.ETaskState.eNone

        self.m_nFileExeConnID = 0

    @staticmethod
    def GetType():
        return task_enum.ETaskType.eDis

    def OnReturn(self, nConnID, dictVarReturn):
        """
        :param nConnID:
        :param dictVarReturn:
            task_var.TaskVar.ToReturnDict
        :return:
        """
        self.m_LoggerObj.debug("ConnID:%d, dictVarReturn:%s", nConnID, str(dictVarReturn))

        self.m_nFileExeConnID = nConnID

        for szName, dictValue in dictVarReturn.items():
            VarObj = self.m_dictVar[szName]
            VarObj.UpdateOutputValue(dictValue)

        for szName, _ in dictVarReturn.items():
            VarObj = self.m_dictVar[szName]
            VarObj.RequestReturn(nConnID, self.m_szTaskId, self.RequestReturnCb)

    def RequestReturnCb(self, szName):
        self.m_LoggerObj.debug("name:%s", szName)
        assert szName in self.m_dictVar

        CurVarObj = self.m_dictVar[szName]
        assert CurVarObj.IsOutput()

        bOver = True
        bAllOutputOK = True
        for _, VarObj in self.m_dictVar.items():
            if VarObj.IsOutput():
                if VarObj.IsError():
                    bAllOutputOK = False
                    break

                if not VarObj.IsDownloaded():
                    bAllOutputOK = False
                    bOver = False
                    break

        if bAllOutputOK:
            self.m_eState = task_enum.ETaskState.eSucceed

        if bOver:
            import logic.connection.message_dispatcher as message_dispatcher
            message_dispatcher.CallRpc(self.m_nFileExeConnID, "logic.gm.gm_command", "OnReturnOver", [self.m_szTaskId])

    def IsSucceed(self):
        return self.m_eState == task_enum.ETaskState.eSucceed
