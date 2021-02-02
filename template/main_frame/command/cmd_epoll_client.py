# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2021/2/2 19:02

# desc: epoll示例，client

import socket

import common.my_log as my_log
import main_frame.cmd_base as cmd_base


class CmdEPollClient(cmd_base.CmdBase):
    def __init__(self):
        super().__init__()
        self.m_LoggerObj = my_log.MyLog(__file__)

    @staticmethod
    def GetName():
        return "epoll_client"

    def Do(self):
        self.m_LoggerObj.info("Start do %s", self.GetName())

        szIP = self.m_AppObj.CLM.GetArg(1)
        nPort = int(self.m_AppObj.CLM.GetArg(2))
        self.m_LoggerObj.info("IP:%s, port:%d", szIP, nPort)

        with socket.socket() as SocketObj:
            SocketObj.connect((szIP, nPort))
            self.m_LoggerObj.info("connect, ip %s, port %d", szIP, nPort)

            SocketObj.send("xjc".encode("utf-8"))
