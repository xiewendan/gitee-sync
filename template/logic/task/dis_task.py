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

    @staticmethod
    def GetType(self):
        return task_enum.ETaskType.eDis
