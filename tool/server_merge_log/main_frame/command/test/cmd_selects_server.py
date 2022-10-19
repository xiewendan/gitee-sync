# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2021/2/2 19:02

# desc: epoll示例，server


import main_frame.cmd_base as cmd_base


class CmdSelectsServer(cmd_base.CmdBase):
    def __init__(self):
        super().__init__()

        import common.my_log as my_log
        self.m_LoggerObj = my_log.MyLog(__file__)

    @staticmethod
    def GetName():
        return "selects_server"

    def Do(self):
        import socket
        import selectors

        self.m_LoggerObj.info("Start do %s", self.GetName())

        szIP = self.m_AppObj.CLM.GetArg(1)
        nPort = int(self.m_AppObj.CLM.GetArg(2))
        self.m_LoggerObj.info("IP:%s, port:%d", szIP, nPort)

        SocketObj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        SocketObj.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        SocketObj.bind((szIP, nPort))
        SocketObj.listen(10)

        SelectorObj = selectors.DefaultSelector()

        def Accept(NewSocketObj, nMask):
            ConnObj, AddrObj = NewSocketObj.accept()

            self.m_LoggerObj.info("new client com:%s", str(AddrObj))

            SelectorObj.register(ConnObj, selectors.EVENT_READ, ReadWrite)

        def Read(ConnObj, nMask):
            self.m_LoggerObj.info("socket can read: %s", str(ConnObj))
            try:
                byteData = ConnObj.recv(4)
            except BaseException as e:
                SelectorObj.unregister(ConnObj)
                return

            if byteData:
                self.m_LoggerObj.info("echoing:%s to %s", repr(byteData), str(ConnObj))
                # SelectorObj.modify(ConnObj, selectors.EVENT_WRITE, Write)
            else:
                self.m_LoggerObj.info("closing:%s", str(ConnObj))
                SelectorObj.unregister(ConnObj)

        def Write(ConnObj, nMask):
            self.m_LoggerObj.info("socket can write: %s", str(ConnObj))
            # SelectorObj.modify(ConnObj, selectors.EVENT_READ, Read)

        def ReadWrite(ConnObj, nMask):
            self.m_LoggerObj.debug("socket can read or can write:%s", str(ConnObj))

            if nMask & selectors.EVENT_WRITE:
                self.m_LoggerObj.debug("socket can write")
                Write(ConnObj, nMask)
            elif nMask & selectors.EVENT_READ:
                self.m_LoggerObj.debug("socket can read")
                Read(ConnObj, nMask)
            else:
                self.m_LoggerObj.debug("socket not read and write")

        SelectorObj.register(SocketObj, selectors.EVENT_READ, Accept)

        while True:
            listEvent = SelectorObj.select(1)
            for key, mask in listEvent:
                CallbackObj = key.data
                CallbackObj(key.fileobj, mask)
