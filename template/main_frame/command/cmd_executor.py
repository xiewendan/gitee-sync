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

    @staticmethod
    def GetName():
        return "executor"

    def _OnInit(self):
        pass

    def Do(self):
        """执行命令"""
        self.m_LoggerObj.info("Start")

        # szCWD = self.m_AppObj.ConfigLoader.CWD

        szIp = self.m_AppObj.CLM.GetArg(1)
        nPort = int(self.m_AppObj.CLM.GetArg(2))
        szTargetIp = self.m_AppObj.CLM.GetArg(3)
        nTargetPort = int(self.m_AppObj.CLM.GetArg(4))

        dictData = {
            "listen_ip": szIp,
            "listen_port": nPort,
            "register_ip": szTargetIp,
            "register_port": nTargetPort
        }

        import logic.client.executor as executor
        ExecutorObj = executor.Executor(dictData)
        ExecutorObj.Run()
