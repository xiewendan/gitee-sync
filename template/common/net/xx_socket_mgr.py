# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2021/2/4 12:00

# desc: 管理所有的XxSocket对象

import threading


class SelectorThread(threading.Thread):
    """Selector监控所有创建的socket，读和写都会从这里触发回调给上层"""

    def __init__(self, XxSocketMgrObj, nTimeout):
        import selectors
        import common.my_log as my_log

        super().__init__()

        self.m_LoggerObj = my_log.MyLog(__file__)

        self.m_bRunning = True
        self.m_nTimeout = nTimeout
        self.m_XxSocketMgrObj = XxSocketMgrObj
        self.m_SelectorObj = selectors.DefaultSelector()

    def stop(self):
        self.m_bRunning = False

    def run(self):
        self.m_LoggerObj.info("run")

        while self.m_bRunning:
            # 监听处理回调
            listEvent = self.m_SelectorObj.select(self.m_nTimeout)
            for KeyObj, nMask in listEvent:
                CallbackObj = KeyObj.data
                CallbackObj(KeyObj.fileobj, nMask)

            # 新增注册socket


class XxSocketMgr:
    def __init__(self, nTimeout):
        import common.my_log as my_log
        self.m_LoggerObj = my_log.MyLog(__file__)

        self.m_SelectThreadObj = None

        assert nTimeout >= 0, "超时不能小于0"
        self.m_nTimeout = nTimeout

        # ip-port -> socket
        self.m_listListenList = []

        # send msg -> pack data
        self.m_listSendData = []

        # send data -> create socket

        # socket sending data

        # socket

        # socket管理列表
        self.m_dictIp2Port2Socket = {}  # self.m_dictIp2Port2Socket[IP][nPort]=SocketObj



    def Init(self):
        self.m_LoggerObj.debug("Init")

        self.m_SelectThreadObj = SelectorThread(self, self.m_nTimeout)
        self.m_SelectThreadObj.start()

    def Destroy(self):
        self.m_LoggerObj.debug("Destroy")

        self.m_SelectThreadObj.stop()
        self.m_SelectThreadObj.join()

    def Listen(self, szIP, nPort, nBacklog=1):
        self.m_LoggerObj.info("ip:%s, port:%d", szIP, nPort)
        assert nBacklog >= 0, "back log %s" % nBacklog

        import socket
        import selectors

        SocketObj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        SocketObj.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        SocketObj.bind((szIP, nPort))
        SocketObj.listen(nBacklog)



        def Accept(AcceptSocketObj, nMask):
            ConnObj, AddrObj = AcceptSocketObj.accept()

            self.m_LoggerObj.info("new client com:%s", str(AddrObj))

            SelectorObj.register(ConnObj, selectors.EVENT_READ, Read)

        def Read(ConnObj, nMask):
            self.m_LoggerObj.info("socket can read: %s", str(ConnObj))
            byteData = ConnObj.recv(2)
            if byteData:
                self.m_LoggerObj.info("echoing:%s to %s", repr(byteData), str(ConnObj))
                SelectorObj.modify(ConnObj, selectors.EVENT_WRITE, Write)
            else:
                self.m_LoggerObj.info("closing:%s", str(ConnObj))
                SelectorObj.unregister(ConnObj)

        def Write(ConnObj, nMask):
            self.m_LoggerObj.info("socket can write: %s", str(ConnObj))
            SelectorObj.modify(ConnObj, selectors.EVENT_READ, Read)

        SelectorObj.register(SocketObj, selectors.EVENT_READ, Accept)


    def Send(self, szIP, nPort, dictData):
        pass
