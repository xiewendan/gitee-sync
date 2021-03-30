import logic.task.base_task as tasK_base
import logic.task.task_enum as task_enum


class DisTask(tasK_base.BaseTask):

    def __init__(self, dictTaskData):
        super().__init__(dictTaskData)

        for szName, VarObj in self.m_dictVar.items():
            if VarObj.IsInput():
                VarObj.Init()

        import logic.task.dis_task_mgr as dis_task_mgr
        szIp, nExePort, nFileExePort = dis_task_mgr.GetIpPort()

        self.m_szIp = szIp
        self.m_nExePort = nExePort
        self.m_nFileExePort = nFileExePort

        self.m_eState = task_enum.ETaskState.eNone

    @staticmethod
    def GetType(self):
        return task_enum.ETaskType.eDis

    def OnReturn(self, nConnID, dictVarReturn):
        """
        :param nConnID:
        :param dictVarReturn:
            task_var.TaskVar.ToReturnDict
        :return:
        """
        self.m_LoggerObj.debug("ConnID:%d, dictVarReturn:%s", nConnID, str(dictVarReturn))

        for szName, dictValue in dictVarReturn.items():
            VarObj = self.m_dictVar[szName]
            VarObj.UpdateOutputValue(dictValue)

        for szName, _ in dictVarReturn.items():
            VarObj = self.m_dictVar[szName]
            VarObj.RequestReturn(nConnID, self.RequestReturnCb)

    def RequestReturnCb(self, szName):
        self.m_LoggerObj.debug("name:%s", szName)
        assert szName in self.m_dictVar

        CurVarObj = self.m_dictVar[szName]
        assert CurVarObj.IsOutput()

        bAllOutputOK = True
        for _, VarObj in self.m_dictVar.items():
            if VarObj.IsOutput():
                if VarObj.IsError():
                    bAllOutputOK = False
                    break

                if not VarObj.IsDownloaded():
                    bAllOutputOK = False
                    break

        if bAllOutputOK:
            self.m_eState = task_enum.ETaskState.eSucceed

    def IsSucceed(self):
        return self.m_eState == task_enum.ETaskState.eSucceed
