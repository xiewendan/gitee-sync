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

import common.my_log as my_log

class XxConnectionMgr:
    """"""

    def __init__(self):
        import common.async_net.xx_connection_factory as xx_connection_factory

        self.m_LoggerObj = my_log.MyLog(__file__)

        self.m_dictConnection = {}  # m_dictConnection[nId] = ConnectionObj

        self.m_ConnectionFactoryObj = xx_connection_factory.XxConnectionFactory()
        self.m_ConnectionFactoryObj.RegisterAll()

    @my_log.SeperateWrap()
    def Destroy(self):
        self.m_LoggerObj.info("")

        self.m_ConnectionFactoryObj.UnregisterAll()

        listID = list(self.m_dictConnection.keys())
        for nID in listID:
            self.DestroyConnection(nID)

        import common.async_net.dispatcher.xx_dispatcher_mgr as xx_dispatcher_mgr
        xx_dispatcher_mgr.Destroy()

    @my_log.SeperateWrap()
    def CreateConnection(self, nType, dictConnectionData) -> int:
        """@:return nID"""
        self.m_LoggerObj.info("type:%d, dictData:%s", nType, dictConnectionData)

        ConnectionObj = self.m_ConnectionFactoryObj.CreateConnection(nType, dictConnectionData)

        self._AddConnection(ConnectionObj)

        return ConnectionObj.ID

    @my_log.SeperateWrap()
    def DestroyConnection(self, nID):
        self.m_LoggerObj.info("id:%s", nID)

        ConnectionObj = self._GetConnection(nID)
        ConnectionObj.Destroy()
        del self.m_dictConnection[nID]

    @my_log.SeperateWrap()
    def Listen(self, nID, szIp, nPort):
        self.m_LoggerObj.info("id:%d, ip:%s, port:%d", nID, szIp, nPort)

        ConnectionObj = self._GetConnection(nID)
        ConnectionObj.Listen(szIp, nPort)

    @my_log.SeperateWrap()
    def Connect(self, nID, szIp, nPort):
        self.m_LoggerObj.info("id:%d, ip:%s, port:%d", nID, szIp, nPort)

        ConnectionObj = self._GetConnection(nID)
        ConnectionObj.Connect(szIp, nPort)

    @my_log.SeperateWrap()
    def Send(self, nID, dictData):
        self.m_LoggerObj.info("id:%d, data:%s", nID, str(dictData))

        ConnectionObj = self._GetConnection(nID)
        ConnectionObj.Send(dictData)

    # noinspection PyMethodMayBeStatic
    def Update(self):
        # 每帧需要调用一次，处理select中的事件消息
        import common.async_net.dispatcher.xx_dispatcher_mgr as xx_dispatcher_mgr
        xx_dispatcher_mgr.Update()

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

    # ********************************************************************************
    # callback
    # ********************************************************************************
    def F_OnConnect(self, nID):
        ConnectionObj = self._GetConnection(nID)
        ConnectionObj.F_OnConnect()

    def F_OnDisconnect(self, nID):
        ConnectionObj = self._GetConnection(nID)
        ConnectionObj.F_OnDisconnect()

    def F_Accept(self, nID, szIp, nPort):
        ConnectionObj = self._GetConnection(nID)
        return ConnectionObj.F_Accept(szIp, nPort)

    def F_OnRead(self, nID, dictData):
        ConnectionObj = self._GetConnection(nID)
        ConnectionObj.F_OnRead(dictData)

    def F_OnClose(self, nID):
        ConnectionObj = self._GetConnection(nID)
        ConnectionObj.F_OnClose()


def CreateConnectionData(nSocketListen=1):
    assert nSocketListen > 0

    dictData = {"socket_listen": nSocketListen}

    return dictData


g_XxConnectionMgrObj = XxConnectionMgr()

CreateConnection = g_XxConnectionMgrObj.CreateConnection
Listen = g_XxConnectionMgrObj.Listen
Connect = g_XxConnectionMgrObj.Connect
Send = g_XxConnectionMgrObj.Send
Update = g_XxConnectionMgrObj.Update
Destroy = g_XxConnectionMgrObj.Destroy
DestroyConnection = g_XxConnectionMgrObj.DestroyConnection

F_OnConnect = g_XxConnectionMgrObj.F_OnConnect
F_OnDisconnect = g_XxConnectionMgrObj.F_OnDisconnect
F_Accept = g_XxConnectionMgrObj.F_Accept
F_OnRead = g_XxConnectionMgrObj.F_OnRead
F_OnClose = g_XxConnectionMgrObj.F_OnClose
