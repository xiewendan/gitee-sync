# -*- coding: utf-8 -*-
# __author__ = xiaobao
# __date__ = 2021/2/4 12:08

# desc:


import common.my_log as my_log
import main_frame.cmd_base as cmd_base


class CmdExecutor(cmd_base.CmdBase):
    def __init__(self):
        super().__init__()
        self.m_LoggerObj = my_log.MyLog(__file__)

        self.m_szIp = ""
        self.m_nExePort = 0
        self.m_nFileExePort = 0

    @staticmethod
    def GetName():
        return "executor"

    def GetIp(self):
        return self.m_szIp

    def GetExePort(self):
        return self.m_nExePort

    def GetFileExePort(self):
        return self.m_nFileExePort

    def _OnInit(self):
        pass

    def Do(self):
        """执行命令"""
        self.m_LoggerObj.info("Start")

        # szCWD = self.m_AppObj.ConfigLoader.CWD

        szRegisterIp = self.m_AppObj.CLM.GetArg(1)
        nRegisterPort = int(self.m_AppObj.CLM.GetArg(2))
        szListenIp = self.m_AppObj.CLM.GetArg(3)
        nListenPort = int(self.m_AppObj.CLM.GetArg(4))
        nFilePort = int(self.m_AppObj.CLM.GetArg(5))

        dictData = {
            "register_ip": szRegisterIp,
            "register_port": nRegisterPort,
            "listen_ip": szListenIp,
            "listen_port": nListenPort,
            "file_listen_ip": szListenIp,
            "file_listen_port": nFilePort,
        }

        self.m_szIp = szListenIp
        self.m_nExePort = nListenPort
        self.m_nFileExePort = nFilePort

        import logic.task.dis_task_mgr as dis_task_mgr
        dis_task_mgr.SetIpPort(szListenIp, nListenPort, nFilePort)

        import logic.executor.executor as executor
        ExecutorObj = executor.Executor(dictData)
        ExecutorObj.Run()
