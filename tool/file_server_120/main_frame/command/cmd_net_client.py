# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2020/12/5 18:55

# desc:

import socket

import main_frame.cmd_base as cmd_base
import common.my_log as my_log

TCP_MAX_BYTE = 1448


class CmdNetClient(cmd_base.CmdBase):
    def __init__(self):
        super().__init__()

        self.m_LoggerObj = my_log.MyLog(__file__)

    @staticmethod
    def GetName():
        return "net_client"

    def Do(self):
        self.m_LoggerObj.info("Start do %s", self.GetName())

        szCWD = self.m_AppObj.ConfigLoader.CWD
        szIP = self.m_AppObj.CLM.GetArg(1)
        nPort = int(self.m_AppObj.CLM.GetArg(2))

        # szInFullPath = "{}/{}".format(szCWD, szInPath)
        # szOutFullPath = "{}/{}".format(szCWD, szOutPath)

        with socket.socket() as SocketObj:
            SocketObj.connect((szIP, nPort))
            self.m_LoggerObj.info("connect, ip %s, port %d", szIP, nPort)
            szMsg = "你好，我是小宝"
            SocketObj.send(szMsg.encode("utf-8"))
            self.m_LoggerObj.debug("send msg: %s", szMsg.encode("gbk"))

    def Copy(self, szInFullPath, szOutFullPath):
        with open(szOutFullPath, "wb") as fwp:
            with open(szInFullPath, "rb") as frp:
                while True:
                    szData = frp.read(1448)
                    if szData == b'':
                        break

                    fwp.write(szData)

        print("aaa")

        # nTcpEndIndex = nStartIndex + TCP_MAX_BYTE
        # while nTcpEndIndex < nEndIndex:
        #     nStartIndex += TCP_MAX_BYTE

        # import hashlib
        # Md5Obj = hashlib.md5()
        # Md5Obj
