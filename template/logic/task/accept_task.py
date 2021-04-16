# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2021/3/31 2:04

# desc:

import logic.task.base_task as tasK_base
import logic.task.task_enum as task_enum


class AcceptTask(tasK_base.BaseTask):
    """"""

    def __init__(self, dictTaskData):
        super().__init__(dictTaskData)

        self.m_nTotalInput = 0

        self.m_nExeConnID = 0
        self.m_nFileExeConnID = 0

        self.m_eState = task_enum.ETaskState.eCreate

    @staticmethod
    def GetType():
        return task_enum.ETaskType.eAccept

    def Update(self):
        # 创建状态
        if self.m_eState == task_enum.ETaskState.eCreate:
            self._CreateConnection()  # 发起连接
            self.m_eState = task_enum.ETaskState.eConnecting

        elif self.m_eState == task_enum.ETaskState.eConnecting:
            import common.async_net.xx_connection_mgr as xx_connection_mgr
            if xx_connection_mgr.IsConnected(self.m_nExeConnID) and xx_connection_mgr.IsConnected(self.m_nFileExeConnID):
                # 请求文件
                for szName, VarObj in self.m_dictVar.items():
                    VarObj.Prepare(self.m_nFileExeConnID, self.m_szTaskId)

                self.m_eState = task_enum.ETaskState.ePreparing

        elif self.m_eState == task_enum.ETaskState.ePreparing:
            bVarAllPrepare = True
            for szName, VarObj in self.m_dictVar.items():
                if VarObj.IsError():
                    self.m_eState = task_enum.ETaskState.eFailed
                    import logic.task.accept_task_mgr as accept_task_mgr
                    accept_task_mgr.ClearCurTask(self.m_szTaskId)
                    bVarAllPrepare = False
                    break

                if not VarObj.IsDownloaded():
                    bVarAllPrepare = False
                    break

            if bVarAllPrepare:
                self.m_eState = task_enum.ETaskState.ePrepared

        elif self.m_eState == task_enum.ETaskState.ePrepared:
            bOK = self._Exec()
            if bOK:
                for szName, VarObj in self.m_dictVar.items():
                    if VarObj.IsOutput():
                        VarObj.InitOutput()

                import logic.connection.message_dispatcher as message_dispatcher

                dictVarReturn = {}
                for szName, VarObj in self.m_dictVar.items():
                    if VarObj.IsOutput():
                        dictVarReturn[szName] = VarObj.ToReturnDict()

                message_dispatcher.CallRpc(self.m_nFileExeConnID, "logic.gm.gm_command", "OnReturn", [self.m_szTaskId, dictVarReturn])

                self.m_eState = task_enum.ETaskState.eReturning

            else:
                self.m_eState = task_enum.ETaskState.eFailed
                import logic.task.accept_task_mgr as accept_task_mgr
                accept_task_mgr.ClearCurTask(self.m_szTaskId)

        elif self.m_eState == task_enum.ETaskState.eReturning:
            pass

    def _CreateConnection(self):
        self.m_LoggerObj.info("create connection, ip:%s, exe_port:%d, file_exe_port:%d", self.m_szIp, self.m_nExePort, self.m_nFileExePort)

        import common.async_net.xx_connection_mgr as xx_connection_mgr
        import common.async_net.connection.xx_connection as xx_connection

        dictConnectionData = xx_connection_mgr.CreateConnectionData()
        self.m_nExeConnID = xx_connection_mgr.CreateConnection(xx_connection.EConnectionType.eExe2Exe, dictConnectionData)
        xx_connection_mgr.Connect(self.m_nExeConnID, self.m_szIp, self.m_nExePort)

        dictConnectionData1 = xx_connection_mgr.CreateConnectionData()
        self.m_nFileExeConnID = xx_connection_mgr.CreateConnection(xx_connection.EConnectionType.eFileExe2Exe, dictConnectionData1)
        xx_connection_mgr.Connect(self.m_nFileExeConnID, self.m_szIp, self.m_nFileExePort)

    def _Exec(self):
        import os
        import common.util as util

        # TODO 在执行前，需要先将文件放到temp目录下，如果不存在rpath的时候，就放到data/temp/任务id/filename文件

        szWorkDir = "%s/data/temp/%s" % (os.getcwd(), self.m_szTaskId)

        dictVarConfig = {}
        for szVarName, VarObj in self.m_dictVar.items():
            dictVarConfig[szVarName] = VarObj.GetValue()

        import platform
        szPlatform = platform.system().lower()

        for CommandObj in self.m_listCommand:
            szCommandFormat = CommandObj.ToStr()

            szCommandFormat = szCommandFormat.replace("{{platform}}", szPlatform)

            szCommand = util.RenderString(szCommandFormat, dictVarConfig)

            nRet = util.RunCmd(szCommand, szWorkDir=szWorkDir)
            if nRet != 0:
                self.m_LoggerObj.error("Command:%s", szCommand)
                return False

        return True
