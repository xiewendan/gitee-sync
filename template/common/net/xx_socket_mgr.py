# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2021/2/4 12:00

# desc: 管理所有的XxSocket对象
# 名词注释：
#   1 Listen：表示监听，用于监听连接
#   2 Data: 表示发送数据的socket
#

import json
import selectors
import socket
import struct
import threading

import common.my_log as my_log
import common.net.ip_port_data as ip_port_data
import common.net.xx_socket as xx_socket


class ESocketType:
    eListen = 1
    eData = 2


g_SendCount = 1024
g_RecvCount = 1024
g_ListenCount = 100
g_Timeout = 0.01


def SerializeData(dictData):
    byteData = json.dumps(dictData).encode("utf-8")
    nByteLen = len(byteData) + 8
    byteLen = struct.pack("!Q", nByteLen)

    return byteLen + byteData


def UnserializeData(byteData):
    nByteLen = struct.unpack("!Q", byteData[:8])[0]
    assert len(byteData) == nByteLen

    return json.loads(byteData[8:].decode("utf-8"))


class XxSocketMgr(threading.Thread):
    """socket管理器，用于管理底层信息发送和接收"""

    def __init__(self, XxNetObj):
        """
        @:param nTimeout 如果为None，则表示不超时，会一直等待。nTimeout为大于等于0的数，表示会超时，0表示不等待，1表示等待1秒
        """
        super().__init__()
        self.m_LoggerObj = my_log.MyLog(__file__)

        self.m_bRunning = True
        self.m_SelectorObj = None
        self.m_nRegisterCount = 0

        # socket
        self.m_nSocketID = 0
        self.m_dictID2XxSocket = {}  # [id] = XxSocket

        self.m_dictSocket2ID = {}  # [socket]=id
        self.m_dictIp2Port2Type2ID = {}  # [ip][port][type] = id

        # buffer
        self.m_dictIp2Port2RecvBuffer = {}  # [ip][port] = szData
        self.m_dictIp2Port2SendBuffer = {}  # [ip][port] = szData

        self.m_XxNetObj = XxNetObj

    def Start(self):
        self.m_LoggerObj.info("start")

        self.m_SelectorObj = selectors.DefaultSelector()

        self.start()

    def Destroy(self):
        self.m_LoggerObj.info("destroy")
        self._Stop()
        self.join()

    def _Stop(self):
        self.m_LoggerObj.info("stop")
        self.m_bRunning = False

    def run(self):
        self.m_LoggerObj.info("run")

        while self.m_bRunning:
            self.m_LoggerObj.info("===================xxsocket loop begin")

            self._HandleSocketEvent()

            self._UpdateSendBuffer()

            self._UpdateWriteEvent()

            self._HandleRecvBuffer()

            self._HandleListen()

    def _HandleSocketEvent(self):
        self.m_LoggerObj.debug("handle socket event")

        listEvent = self._Select(g_Timeout)
        for KeyObj, nMask in listEvent:
            CallbackObj = KeyObj.data
            CallbackObj(KeyObj.fileobj, nMask)

    def _Accept(self, ListenSocketObj, nMask):
        self.m_LoggerObj.debug("listensocket:%s, mask:%d", str(ListenSocketObj), nMask)

        SocketObj, AddrObj = ListenSocketObj.accept()
        self.m_LoggerObj.info("new client come:%s", str(AddrObj))

        szIp, nPort = AddrObj
        if self._HasSocketObj(szIp, nPort, ESocketType.eData):
            SocketObj.close()
            self.m_LoggerObj.info("has exist socket, close it. ip:%s, port:%d", szIp, nPort)

        else:
            self._Register(SocketObj, selectors.EVENT_READ, self._ReadWrite)

            self._AddSocketObj(szIp, nPort, ESocketType.eData, SocketObj)

    def _ReadWrite(self, SocketObj, nMask):
        self.m_LoggerObj.debug("socketobj:%s, mask:%d", str(SocketObj), nMask)

        if nMask & selectors.EVENT_READ:
            self._Read(SocketObj)
        elif nMask & selectors.EVENT_WRITE:
            self._Write(SocketObj)

    def _Read(self, SocketObj):
        self.m_LoggerObj.debug("socketobj:%s", SocketObj)

        try:
            byteData = SocketObj.recv(g_RecvCount)
        except BaseException as e:
            self._UnRegister(SocketObj)
            self._RemoveSocketObj(SocketObj)
            self.m_LoggerObj.error("socket recv data failed:", e)
            return

        if byteData:
            self._AddRecvBuffer(SocketObj, byteData)
        else:
            self.m_LoggerObj.info("closing:%s", str(SocketObj))
            self._UnRegister(SocketObj)
            self._RemoveSocketObj(SocketObj)

    def _Write(self, SocketObj):
        self.m_LoggerObj.debug("socketobj:%s", SocketObj)

        byteSendData = self._GetDataFromSendBuffer(SocketObj, g_SendCount)
        if byteSendData is None:
            szIp, nPort = self._GetIpPort(SocketObj)
            self.m_LoggerObj.info("send data over, ip:%s, port:%d", szIp, nPort)

            self._Modify(SocketObj, selectors.EVENT_READ, self._ReadWrite)
            return

        # TODO 写异常，是否需要考虑移除
        nSendedCount = SocketObj.send(byteSendData)
        self._UpdateSendedCount(SocketObj, nSendedCount)

    def _UpdateSendBuffer(self):
        self.m_LoggerObj.debug("update send data buffer")

        # [IpPortDataObj,...]
        listSendData = self.m_XxNetObj.GetSendData()
        for IpPortDataObj in listSendData:
            szIp = IpPortDataObj.Ip
            nPort = IpPortDataObj.Port
            dictData = IpPortDataObj.Data

            byteData = SerializeData(dictData)
            self._AddSendBuffer(szIp, nPort, byteData)

    def _UpdateWriteEvent(self):
        self.m_LoggerObj.debug("update write event")

        listIpPort = self._GetSendIpPort()
        for listData in listIpPort:
            szIp = listData[0]
            nPort = listData[1]

            SocketObj = self._GetSocketObj(szIp, nPort, ESocketType.eData)
            if SocketObj is not None:
                self._Modify(SocketObj, selectors.EVENT_READ | selectors.EVENT_WRITE, self._ReadWrite)
            else:
                self.m_LoggerObj.info("try connect, ip:%s, port:%d", szIp, nPort)

                try:
                    SocketObj = socket.socket()
                    SocketObj.connect((szIp, nPort))
                except ConnectionRefusedError as ExceptionObj:
                    import common.my_trackback as my_traceback
                    my_traceback.OnException()
                else:
                    self.m_LoggerObj.info("connected, ip:%s, port:%d", szIp, nPort)
                    self._AddSocketObj(szIp, nPort, ESocketType.eData, SocketObj)
                    self._Register(SocketObj, selectors.EVENT_READ | selectors.EVENT_WRITE, self._ReadWrite)

    def _HandleListen(self):
        self.m_LoggerObj.debug("handle listen")

        listListenData = self.m_XxNetObj.GetListenData()
        for IpPortDataObj in listListenData:
            szIp = IpPortDataObj.Ip
            nPort = IpPortDataObj.Port

            SocketObj = self._GetSocketObj(szIp, nPort, ESocketType.eListen)

            if SocketObj is not None:
                self.m_LoggerObj.error("socket listen failed, port has been taken. ip:%s, port:%d", szIp, nPort)
                continue

            # TODO 可能端口还是被其它应用占用
            SocketObj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            SocketObj.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            SocketObj.bind((szIp, nPort))
            SocketObj.listen(g_ListenCount)
            self.m_LoggerObj.info("listen socket, ip:%s, port:%d, count:%d", szIp, nPort, g_ListenCount)

            self._AddSocketObj(szIp, nPort, ESocketType.eListen, SocketObj)

            self._Register(SocketObj, selectors.EVENT_READ, self._Accept)

    # ********************************************************************************
    # socket管理
    # ********************************************************************************
    def _GenSocketID(self):
        self.m_nSocketID += 1
        return self.m_nSocketID

    def _HasSocketObj(self, szIp, nPort, eType):
        self.m_LoggerObj.debug("ip:%s, port:%d, type:%d", szIp, nPort, eType)

        if szIp not in self.m_dictIp2Port2Type2ID:
            return False

        if nPort not in self.m_dictIp2Port2Type2ID[szIp]:
            return False

        if eType not in self.m_dictIp2Port2Type2ID[szIp][nPort]:
            return False

        return True

    def _GetSocketObj(self, szIp, nPort, eType):
        self.m_LoggerObj.debug("ip:%s, port:%d, type:%d", szIp, nPort, eType)

        if not self._HasSocketObj(szIp, nPort, eType):
            return None

        nID = self.m_dictIp2Port2Type2ID[szIp][nPort][eType]
        XxSocketObj = self.m_dictID2XxSocket[nID]
        return XxSocketObj.SocketObj

    def _AddSocketObj(self, szIp, nPort, eType, SocketObj):
        self.m_LoggerObj.debug("ip:%s, port:%d, type:%s, socketobj:%s", szIp, nPort, eType, SocketObj)

        assert not self._HasSocketObj(szIp, nPort, eType)

        nID = self._GenSocketID()

        XxSocketObj = xx_socket.XxSocket(SocketObj, szIp, nPort, nID, eType)

        if szIp not in self.m_dictIp2Port2Type2ID:
            self.m_dictIp2Port2Type2ID[szIp] = {}
        if nPort not in self.m_dictIp2Port2Type2ID[szIp]:
            self.m_dictIp2Port2Type2ID[szIp][nPort] = {}

        self.m_dictIp2Port2Type2ID[szIp][nPort][eType] = nID

        self.m_dictID2XxSocket[nID] = XxSocketObj

        self.m_dictSocket2ID[SocketObj] = nID

    def _RemoveSocketObj(self, SocketObj):
        self.m_LoggerObj.debug("socketobj:%s", str(SocketObj))

        nID = self.m_dictSocket2ID[SocketObj]
        XxSocketObj = self.m_dictID2XxSocket[nID]

        szIp = XxSocketObj.Ip
        nPort = XxSocketObj.Port
        eType = XxSocketObj.Type

        del self.m_dictID2XxSocket[nID]
        del self.m_dictSocket2ID[SocketObj]

        del self.m_dictIp2Port2Type2ID[szIp][nPort][eType]
        if len(self.m_dictIp2Port2Type2ID[szIp][nPort]) == 0:
            del self.m_dictIp2Port2Type2ID[szIp][nPort]
            if len(self.m_dictIp2Port2Type2ID[szIp]) == 0:
                del self.m_dictIp2Port2Type2ID[szIp]

    def _GetIpPort(self, SocketObj):
        self.m_LoggerObj.debug("socketobj:%s", str(SocketObj))

        assert SocketObj in self.m_dictSocket2ID
        nID = self.m_dictSocket2ID[SocketObj]

        assert nID in self.m_dictID2XxSocket
        XxSocketObj = self.m_dictID2XxSocket[nID]

        return XxSocketObj.Ip, XxSocketObj.Port

    # ********************************************************************************
    # data
    # ********************************************************************************
    def _AddRecvBuffer(self, SocketObj, byteData):
        self.m_LoggerObj.debug("socketobj:%s, data:%s", str(SocketObj), repr(byteData))

        szIp, nPort = self._GetIpPort(SocketObj)
        if szIp not in self.m_dictIp2Port2RecvBuffer:
            self.m_dictIp2Port2RecvBuffer[szIp] = {}

        if nPort not in self.m_dictIp2Port2RecvBuffer[szIp]:
            self.m_dictIp2Port2RecvBuffer[szIp][nPort] = byteData
        else:
            self.m_dictIp2Port2RecvBuffer[szIp][nPort] += byteData

    def _GetDataFromSendBuffer(self, SocketObj, nSize):
        self.m_LoggerObj.debug("socketobj:%s", str(SocketObj))

        szIp, nPort = self._GetIpPort(SocketObj)
        if szIp not in self.m_dictIp2Port2SendBuffer:
            return None

        if nPort not in self.m_dictIp2Port2SendBuffer[szIp]:
            return None

        return self.m_dictIp2Port2SendBuffer[szIp][nPort][:nSize]

    def _GetSendIpPort(self):
        self.m_LoggerObj.debug("")
        listIpPort = []

        for szIp, dictPort2SendBuffer in self.m_dictIp2Port2SendBuffer.items():
            for nPort, _ in dictPort2SendBuffer.items():
                listIpPort.append([szIp, nPort])

        return listIpPort

    def _AddSendBuffer(self, szIp, nPort, byteData):
        self.m_LoggerObj.debug("ip:%s, port:%d, data:%s", szIp, nPort, byteData)

        if szIp not in self.m_dictIp2Port2SendBuffer:
            self.m_dictIp2Port2SendBuffer[szIp] = {}

        if nPort not in self.m_dictIp2Port2SendBuffer[szIp]:
            self.m_dictIp2Port2SendBuffer[szIp][nPort] = byteData
        else:
            self.m_dictIp2Port2SendBuffer[szIp][nPort] += byteData

    def _UpdateSendedCount(self, SocketObj, nSendedCount):
        """返回值，是否发送结束"""
        self.m_LoggerObj.debug("socketobj:%s, sended count:%d", SocketObj, nSendedCount)

        szIp, nPort = self._GetIpPort(SocketObj)
        assert szIp in self.m_dictIp2Port2SendBuffer
        assert nPort in self.m_dictIp2Port2SendBuffer[szIp]

        byteSendData = self.m_dictIp2Port2SendBuffer[szIp][nPort]
        if len(byteSendData) <= nSendedCount:
            del self.m_dictIp2Port2SendBuffer[szIp][nPort]
            if len(self.m_dictIp2Port2SendBuffer[szIp]) == 0:
                del self.m_dictIp2Port2SendBuffer[szIp]
            return True

        else:
            self.m_dictIp2Port2SendBuffer[szIp][nPort] = self.m_dictIp2Port2SendBuffer[szIp][nPort][nSendedCount:]
            return False

    def _HandleRecvBuffer(self):
        self.m_LoggerObj.debug("handle recv buffer")

        listRecvData = []
        for szIp, dictPort2RecvBuffer in self.m_dictIp2Port2RecvBuffer.items():
            for nPort, byteData in dictPort2RecvBuffer.items():
                while True:
                    nByteLen = self._ParseByteLen(byteData)
                    if nByteLen is None:
                        break
                    elif len(byteData) < nByteLen:
                        break
                    else:
                        dictData = UnserializeData(byteData[:nByteLen])
                        IpPortData = ip_port_data.IpPortData(szIp, nPort, dictData)
                        listRecvData.append(IpPortData)

                        byteData = byteData[nByteLen:]
                        dictPort2RecvBuffer[nPort] = byteData

        self.m_XxNetObj.AddRecvData(listRecvData)

    def _ParseByteLen(self, byteData):
        if len(byteData) < 8:
            return None

        nByteLen = struct.unpack("!Q", byteData[:8])[0]

        return nByteLen

    # ********************************************************************************
    # selector
    # ********************************************************************************
    def _Select(self, nTimeout):
        if self.m_nRegisterCount == 0:
            return []
        else:
            return self.m_SelectorObj.select(nTimeout)

    def _Register(self, SocketObj, nMask, Callback):
        self.m_SelectorObj.register(SocketObj, nMask, Callback)
        self._AddRegisterCount(1)

    def _UnRegister(self, SocketObj):
        self.m_SelectorObj.unregister(SocketObj)
        self._AddRegisterCount(-1)

    def _AddRegisterCount(self, nCount):
        self.m_LoggerObj.debug("reigstercount:%d, count:%d", self.m_nRegisterCount, nCount)
        self.m_nRegisterCount += nCount
        assert self.m_nRegisterCount >= 0

    def _Modify(self, SocketObj, nMask, Callback):
        self.m_LoggerObj.debug("socketobj:%s, mask:%d, callback:%s", SocketObj, nMask, Callback)

        self.m_SelectorObj.modify(SocketObj, nMask, Callback)
