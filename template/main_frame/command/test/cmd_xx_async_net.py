# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2021/2/4 12:08

# desc: 测试xx_net网络代码

import common.my_log as my_log
import main_frame.cmd_base as cmd_base


class CmdXxNet(cmd_base.CmdBase):
    def __init__(self):
        super().__init__()
        self.m_LoggerObj = my_log.MyLog(__file__)

    @staticmethod
    def GetName():
        return "xx_async_net"

    def _OnInit(self):
        pass

    def Do(self):
        """执行命令"""
        self.m_LoggerObj.info("Start")

        szCWD = self.m_AppObj.ConfigLoader.CWD

        szIp = self.m_AppObj.CLM.GetArg(1)
        nPort = int(self.m_AppObj.CLM.GetArg(2))
        szTargetIp = self.m_AppObj.CLM.GetArg(3)
        nTargetPort = int(self.m_AppObj.CLM.GetArg(4))

        import common.net.xx_async_net as xx_async_net
        XxNetObj = xx_async_net.XxAsyncNet()
        # XxNetObj.Listen(szIp, nPort)

        import time
        # connect
        dictData = {"type": "YtSocket", "function": "PyConnect"}
        XxNetObj.SendAsync(szTargetIp, nTargetPort, dictData, self.OnConnect, (XxNetObj, szTargetIp, nTargetPort))

        while True:
            XxNetObj.HandleRecv()

    def OnConnect(self, XxNetObj, szTargetIp, nTargetPort):
        self.m_LoggerObj.debug("XxNetObj:%s, targetip:%s, targetport:%d", XxNetObj, szTargetIp, nTargetPort)

        # SnapshotWindow
        dictData = {"type": "YtSocket", "function": "SnapshotWindow"}
        XxNetObj.SendAsync(szTargetIp, nTargetPort, dictData, self.OnSnapshotWindow, (XxNetObj,))

    def OnSnapshotWindow(self, XxNetObj):
        self.m_LoggerObj.debug("OnSnapshotwindow")

        XxNetObj.Destroy()

        exit(0)
