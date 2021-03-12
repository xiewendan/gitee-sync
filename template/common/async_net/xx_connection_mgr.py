# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2021/3/11 20:27

# desc: 连接管理器，id到连接对象的映射，其余地方都通过id引用（传递id而不传对象是比较安全的）

# 1、注册新的连接类
# 2、创建连接
# 3、监听
# 4、发送
# 5、更新

__all__ = ["XxConnectionMgr", "CreateConnectionData"]

import socket


class XxConnectionMgr:
    """"""

    def __init__(self):
        import common.my_log as my_log
        import common.async_net.xx_connection_factory as xx_connection_factory

        self.m_LoggerObj = my_log.MyLog(__file__)

        self.m_dictConnection = {}  # m_dictConnection[nId] = ConnectionObj

        self.m_ConnectionFactoryObj = xx_connection_factory.XxConnectionFactory()
        self.m_ConnectionFactoryObj.RegisterAll()

    def Destroy(self):
        self.m_LoggerObj.info("")
        self.m_ConnectionFactoryObj.UnregisterAll()

    def CreateConnection(self, nType, dictConnectionData=None):
        """@:return nID"""
        ConnectionObj = self.m_ConnectionFactoryObj.CreateConnection(nType, dictConnectionData)

        self._AddConnection(ConnectionObj)

        return ConnectionObj.ID

    def Listen(self, nID, szIp, nPort):
        self.m_LoggerObj.info("id:%d, ip:%s, port:%d", nID, szIp, nPort)

        ConnectionObj = self._GetConnection(nID)
        ConnectionObj.Listen(szIp, nPort)

    def Connect(self, nID, szIp, nPort):
        self.m_LoggerObj.info("id:%d, ip:%s, port:%d", nID, szIp, nPort)

        ConnectionObj = self._GetConnection(nID)
        ConnectionObj.Connect(szIp, nPort)

    def Send(self, nID, dictData):
        self.m_LoggerObj.info("id:%d, data:%s", nID, str(dictData))

        ConnectionObj = self._GetConnection(nID)
        ConnectionObj.Send(dictData)

    def Update(self):
        pass

    # ********************************************************************************
    # dictConnection
    # ********************************************************************************
    def _AddConnection(self, ConnectionObj):
        self.m_LoggerObj.debug("connection id:%d", ConnectionObj.ID)

        nID = ConnectionObj.ID
        assert nID not in self.m_dictConnection

        self.m_dictConnection[nID] = ConnectionObj

    def _RemoveConnection(self, nID):
        self.m_LoggerObj.debug("connection id:%d", nID)

        assert nID in self.m_dictConnection
        del self.m_dictConnection[nID]

    def _GetConnection(self, nID):
        assert nID in self.m_dictConnection

        return self.m_dictConnection[nID]

    def F_OnConnect(self, nID):
        ConnectionObj = self._GetConnection(nID)
        ConnectionObj.F_Connect()

    def F_OnDisconnect(self, nID):
        ConnectionObj = self._GetConnection(nID)
        ConnectionObj.F_OnDisconnect()

    def F_OnAccept(self, nID):
        ConnectionObj = self._GetConnection(nID)
        ConnectionObj.F_OnAccept()
        pass

    def F_OnRead(self, nID):
        ConnectionObj = self._GetConnection(nID)
        ConnectionObj.F_OnRead()
        pass

    def F_OnWrite(self, nID):
        ConnectionObj = self._GetConnection(nID)
        ConnectionObj.F_OnWrite()
        pass

    def F_OnClose(self, nID):
        ConnectionObj = self._GetConnection(nID)
        ConnectionObj.F_OnClose()
        pass


def CreateConnectionData(nSocketFamily=socket.AF_INET,
                         nSocketType=socket.SOCK_STREAM,
                         nSocketListen=1
                         ):
    assert nSocketListen > 0

    dictData = {
        "socket_family": nSocketFamily,
        "socket_type": nSocketType,
        "socket_listen": nSocketListen
    }

    return dictData


g_XxConnectionMgrObj = XxConnectionMgr()

CreateConnection = g_XxConnectionMgrObj.CreateConnection
Listen = g_XxConnectionMgrObj.Listen
Connect = g_XxConnectionMgrObj.Connect
Send = g_XxConnectionMgrObj.Send
Update = g_XxConnectionMgrObj.Update
Destroy = g_XxConnectionMgrObj.Destroy

F_OnConnect = g_XxConnectionMgrObj.F_OnConnect
F_OnDisconnect = g_XxConnectionMgrObj.F_OnDisconnect
F_OnAccept = g_XxConnectionMgrObj.F_OnAccept
F_OnRead = g_XxConnectionMgrObj.F_OnRead
F_OnWrite = g_XxConnectionMgrObj.F_OnWrite
F_OnClose = g_XxConnectionMgrObj.F_OnClose
