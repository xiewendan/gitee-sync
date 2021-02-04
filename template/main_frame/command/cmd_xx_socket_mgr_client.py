# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2021/2/4 12:08

# desc:xx socket mgr client客户端

import common.my_log as my_log
import main_frame.cmd_base as cmd_base


class CmdXxSocketMgrClient(cmd_base.CmdBase):
    def __init__(self):
        super().__init__()
        self.m_LoggerObj = my_log.MyLog(__file__)

    @staticmethod
    def GetName():
        return "xx_socket_mgr_client"

    def _OnInit(self):
        pass

    def Do(self):
        """执行命令"""
        self.m_LoggerObj.info("Start ")

        szCWD = self.m_AppObj.ConfigLoader.CWD

        szIp = self.m_AppObj.CLM.GetArg(1)
        nPort = self.m_AppObj.CLM.GetArg(2)

        import common.net.xx_socket_mgr as xx_socket_mgr
        XxSocketMgrObj = xx_socket_mgr.XxSocketMgr()

        dictData = {}
        XxSocketMgrObj.Send(szIp, nPort, dictData)



