# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2021/1/25 19:15

# desc:  独立文件，用于发送文件和数据

import os
import socket
import struct

TCP_MAX_BYTE = 1448 * 100


class NetClient:
    """"""

    def __init__(self):
        import logging
        self.m_LoggerObj = logging.getLogger(self.__class__.__name__)

    def SendFile(self, szIP, nPort, szLocalFPath, szTargetRPath):
        nLen = 0
        with socket.socket() as SocketObj:
            SocketObj.connect((szIP, nPort))
            self.m_LoggerObj.info("connect, ip %s, port %d", szIP, nPort)

            # header
            nTotalLen = os.path.getsize(szLocalFPath)
            bytesTargetRPath = szTargetRPath.encode("utf-8")
            nTargetRPathLen = len(bytesTargetRPath)
            byteHeader = struct.pack("!QI%ds" % nTargetRPathLen, nTotalLen, nTargetRPathLen, bytesTargetRPath)
            SocketObj.send(byteHeader)

            # data
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

            # recv
            szRecvData = SocketObj.recv(8)
            nByteLen = struct.unpack("!Q", szRecvData)[0]
            self.m_LoggerObj.info("receive size:%d", nByteLen)

    def SendData(self, szIP, nPort, szData, szTargetRPath):
        with socket.socket() as SocketObj:
            SocketObj.connect((szIP, nPort))
            self.m_LoggerObj.info("connect, ip %s, port %d", szIP, nPort)

            # header
            bytesData = szData.encode("utf-8")
            nTotalLen = len(bytesData)

            bytesTargetRPath = szTargetRPath.encode("utf-8")
            nTargetRPathLen = len(bytesTargetRPath)

            byteHeader = struct.pack("!QI%ds" % nTargetRPathLen, nTotalLen, nTargetRPathLen, bytesTargetRPath)
            SocketObj.send(byteHeader)

            # data
            SocketObj.send(bytesData)

            self.m_LoggerObj.info("send size:%d", nTotalLen)

            # redv
            szRecvData = SocketObj.recv(8)
            nByteLen = struct.unpack("!Q", szRecvData)[0]
            self.m_LoggerObj.info("receive size:%d", nByteLen)


if __name__ == '__main__':
    NetClientObj = NetClient()
    NetClientObj.SendData("10.249.80.162", 5000, "xjc", "test1.txt")
    NetClientObj.SendFile("10.249.80.162", 5000, "G:/project/xiewendan/tools/template/data/uploads/1.txt", "2.txt")
