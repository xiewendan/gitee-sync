# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2020/12/5 18:55

# desc:

import os
import socket
import struct

import common.my_log as my_log
import common.stat_mgr as stat_mgr
import main_frame.cmd_base as cmd_base

TCP_MAX_BYTE = 1448 * 100


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

        # szLocalFPath = os.getcwd() + "/data/local/test1G.7z"
        # szUploadFPath = os.getcwd() + "/data/uploads/test1G.7z"
        # self.Copy(szLocalFPath, szUploadFPath)

        self.SendFile(nPort, szIP)

    def SendFile(self, nPort, szIP):
        nLen = 0
        szLocalFPath = os.getcwd() + "/data/local/test1G.7z"
        # szLocalFPath = os.getcwd() + "/data/local/1.txt"
        StatMgrObj = stat_mgr.StatMgr()
        StatMgrObj.LogTimeTag("begin")
        with socket.socket() as SocketObj:
            SocketObj.connect((szIP, nPort))
            self.m_LoggerObj.info("connect, ip %s, port %d", szIP, nPort)

            nTotalLen = os.path.getsize(szLocalFPath)
            bytesLen = struct.pack("!Q", nTotalLen)
            SocketObj.send(bytesLen)

            with open(szLocalFPath, "rb") as frp:
                while True:
                    if nLen + TCP_MAX_BYTE < nTotalLen:
                        szData = frp.read(TCP_MAX_BYTE)
                        nLen += len(szData)
                    elif nLen + TCP_MAX_BYTE >= nTotalLen:
                        szData = frp.read(nTotalLen - nLen)
                        nLen += len(szData)

                    SocketObj.send(szData)

                    if nLen == nTotalLen:
                        break

            self.m_LoggerObj.info("send size:%d/%d", nLen, nTotalLen)
            StatMgrObj.LogTimeTag("recv")

            szRecvData = SocketObj.recv(8)
            nByteLen = struct.unpack("!Q", szRecvData)[0]
            self.m_LoggerObj.info("receive size:%d", nByteLen)

        StatMgrObj.LogTimeTag("end")
        print(StatMgrObj.GetTimeTagStat())

    def Copy(self, szInFullPath, szOutFullPath):
        StatMgrObj = stat_mgr.StatMgr()
        StatMgrObj.LogTimeTag("begin")

        with open(szOutFullPath, "wb") as fwp:
            with open(szInFullPath, "rb") as frp:
                while True:
                    szData = frp.read(TCP_MAX_BYTE)
                    if szData == b'':
                        break

                    fwp.write(szData)

        StatMgrObj.LogTimeTag("end")
        print(StatMgrObj.GetTimeTagStat())
