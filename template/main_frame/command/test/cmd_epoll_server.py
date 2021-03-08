# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2021/2/2 19:02

# desc: epoll示例，server


import select

import main_frame.cmd_base as cmd_base


class CmdEPollServer(cmd_base.CmdBase):
    def __init__(self):
        super().__init__()

        import common.my_log as my_log
        self.m_LoggerObj = my_log.MyLog(__file__)
        self.m_dictFileNo2SocketObj = {}
        self.m_dictFileNo2Callback = {}

    @staticmethod
    def GetName():
        return "epoll_server"

    def Do(self):
        import socket

        self.m_LoggerObj.info("Start do %s", self.GetName())

        szIP = self.m_AppObj.CLM.GetArg(1)
        nPort = int(self.m_AppObj.CLM.GetArg(2))
        self.m_LoggerObj.info("IP:%s, port:%d", szIP, nPort)

        SocketObj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        SocketObj.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        SocketObj.bind((szIP, nPort))
        SocketObj.listen(10)

        EpollObj = select.epoll()

        def Accept(NewSocketObj, nMask):
            ConnObj, AddrObj = NewSocketObj.accept()

            self.m_LoggerObj.info("new client com:%s", str(AddrObj))

            self.Register(EpollObj, ConnObj, select.EPOLLIN | select.EPOLLRDHUP, ReadWrite)

        def Read(ConnObj, nMask):
            self.m_LoggerObj.info("socket can read: %s", str(ConnObj))
            try:
                byteData = ConnObj.recv(4)
            except BaseException as e:
                self.m_LoggerObj.info("socket except, disconnect:%s", str(e))
                self.Unregister(EpollObj, ConnObj.fileno())
                return

            if byteData:
                self.m_LoggerObj.info("echoing:%s to %s", repr(byteData), str(ConnObj))
                # EpollObj.modify(ConnObj, selectors.EVENT_WRITE, Write)
            else:
                self.m_LoggerObj.info("closing:%s", str(ConnObj))
                self.Unregister(EpollObj, ConnObj.fileno())

        def Write(ConnObj, nMask):
            self.m_LoggerObj.info("socket can write: %s", str(ConnObj))
            # EpollObj.modify(ConnObj, selectors.EVENT_READ, Read)

        def ReadWrite(ConnObj, nMask):
            self.m_LoggerObj.debug("socket can read or can write:%s", str(nMask))

            if nMask & select.EPOLLOUT:
                self.m_LoggerObj.debug("socket can write")
                Write(ConnObj, nMask)
            elif nMask & select.EPOLLIN:
                self.m_LoggerObj.debug("socket can read")
                Read(ConnObj, nMask)
            elif nMask & select.EPOLLRDHUP:
                self.m_LoggerObj.debug("socket disonnect")
                self.Unregister(EpollObj, ConnObj.fileno())

        self.Register(EpollObj, SocketObj, select.EPOLLIN, Accept)

        while True:
            listEvent = EpollObj.poll(1)
            for nFileno, nEvent in listEvent:
                self.HandleMsg(nFileno, nEvent)

    def HandleMsg(self, nFileno, nEvent):
        funCallback = self.GetCallback(nFileno)
        SocketObj = self.GetSocketObj(nFileno)

        funCallback(SocketObj, nEvent)

    def Register(self, EpollObj, SocketObj, nEvent, funCallback):
        self.m_LoggerObj.debug("fileno:%s, nEvent:%s", SocketObj.fileno(), nEvent)

        nFileNo = SocketObj.fileno()
        self.AddSocketObj(SocketObj)
        self.AddCallback(nFileNo, funCallback)

        EpollObj.register(nFileNo, nEvent)

    def Unregister(self, EpollObj, nFileNo):
        self.m_LoggerObj.debug("nFileNo:%s", nFileNo)
        EpollObj.unregister(nFileNo)

        self.RemoveSocketObj(nFileNo)
        self.RemoveCallback(nFileNo)

    def AddSocketObj(self, SocketObj):
        nFileNo = SocketObj.fileno()

        assert nFileNo not in self.m_dictFileNo2SocketObj

        self.m_dictFileNo2SocketObj[nFileNo] = SocketObj

    def GetSocketObj(self, nFileNo):
        assert nFileNo in self.m_dictFileNo2SocketObj
        return self.m_dictFileNo2SocketObj[nFileNo]

    def RemoveSocketObj(self, nFileNo):
        assert nFileNo in self.m_dictFileNo2SocketObj
        del self.m_dictFileNo2SocketObj[nFileNo]

    def AddCallback(self, nFileNo, funCallback):
        assert nFileNo not in self.m_dictFileNo2Callback
        self.m_dictFileNo2Callback[nFileNo] = funCallback

    def GetCallback(self, nFileNo):
        assert nFileNo in self.m_dictFileNo2Callback
        return self.m_dictFileNo2Callback[nFileNo]

    def RemoveCallback(self, nFileNo):
        assert nFileNo in self.m_dictFileNo2Callback
        del self.m_dictFileNo2Callback[nFileNo]
