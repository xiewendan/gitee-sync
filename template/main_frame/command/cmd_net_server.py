# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2020/12/5 18:55

# desc:

import os
import socket
import threading
import struct

import common.my_log as my_log
import common.stat_mgr as stat_mgr
import main_frame.cmd_base as cmd_base
import main_frame.command.cmd_net_client as cmd_net_client


class CmdNetServer(cmd_base.CmdBase):
    def __init__(self):
        super().__init__()
        self.m_LoggerObj = my_log.MyLog(__file__)

    @staticmethod
    def GetName():
        return "net_server"

    def SocketThread(self, ConnObj, szAddr):
        nLen = 0
        self.m_LoggerObj.info("socket thread running, ip: %s", szAddr)
        szUploadFPath = os.getcwd() + "/data/uploads/test1G.7z"

        StatMgrObj = stat_mgr.StatMgr()
        StatMgrObj.LogTimeTag("begin")

        with open(szUploadFPath, "wb") as fwp:
            nRecvLen = 0
            bytesLen = ConnObj.recv(8)
            nTotalLen = struct.unpack("!Q", bytesLen)[0]

            while True:
                if nRecvLen + cmd_net_client.TCP_MAX_BYTE < nTotalLen:
                    szRecvData = ConnObj.recv(cmd_net_client.TCP_MAX_BYTE)
                    nRecvLen += len(szRecvData)
                elif nRecvLen + cmd_net_client.TCP_MAX_BYTE >= nTotalLen:
                    szRecvData = ConnObj.recv(nTotalLen - nRecvLen)
                    nRecvLen += len(szRecvData)
                else:
                    pass

                fwp.write(szRecvData)

                if nRecvLen == nTotalLen:
                    break

            self.m_LoggerObj.info("total szie:%d", nRecvLen)
            bytesSendLen = struct.pack("!Q", nRecvLen)
            ConnObj.send(bytesSendLen)

        ConnObj.close()

        StatMgrObj.LogTimeTag("end")
        print(StatMgrObj.GetTimeTagStat())

    def Do(self):
        self.m_LoggerObj.info("Start do %s", self.GetName())

        szCWD = self.m_AppObj.ConfigLoader.CWD

        szIP = self.m_AppObj.CLM.GetArg(1)
        nPort = int(self.m_AppObj.CLM.GetArg(2))

        with socket.socket() as SocketObj:
            # SocketObj.setblocking(False)
            SocketObj.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 10240 * 1024)  # 250KB

            SocketObj.bind((szIP, nPort))
            SocketObj.listen(5)

            self.m_LoggerObj.info("socket listen, backlog %d, ip %s, port %d", 5, szIP, nPort)

            while True:
                ConnObj, szAddr = SocketObj.accept()
                self.m_LoggerObj.info("socket connect: %s", szAddr)
                SocketThreadObj = threading.Thread(target=self.SocketThread, args=(ConnObj, szAddr))
                SocketThreadObj.start()
                self.m_LoggerObj.info("socket thread start run: %s", szAddr)
