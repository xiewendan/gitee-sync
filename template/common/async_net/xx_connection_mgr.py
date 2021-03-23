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

        # async callback
        self.m_nAsyncID = 0
        self.m_dictAsyncID2Callback = {}

        # 销毁
        self.m_dictToDestroyConnection = {}

    @my_log.SeperateWrap()
    def Destroy(self):
        self.m_LoggerObj.info("")

        self.m_ConnectionFactoryObj.UnregisterAll()

        listID = list(self.m_dictConnection.keys())
        for nID in listID:
            self.DestroyConnection(nID)

        import common.async_net.dispatcher.xx_dispatcher_mgr as xx_dispatcher_mgr
        xx_dispatcher_mgr.Destroy()

        assert len(self.m_dictToDestroyConnection) == 0

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
        ConnectionObj.Close()
        ConnectionObj.Destroy()
        del self.m_dictConnection[nID]

        if nID in self.m_dictToDestroyConnection:
            del self.m_dictToDestroyConnection[nID]

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

    @my_log.SeperateWrap()
    def SendAsync(self, nID, dictData, funCallback=None, tupleArg=None):
        self.m_LoggerObj.debug("id:%d, dictData:%s", nID, str(dictData))

        if funCallback is not None:
            nAsyncID = self._GenAsyncID()
            self._AddAsyncCallback(nAsyncID, funCallback, tupleArg)

            import common.async_net.connection.xx_connection as xx_connection
            assert xx_connection.EAsyncName.eRetAsyncID not in dictData
            dictData[xx_connection.EAsyncName.eRetAsyncID] = nAsyncID

        self.Send(nID, dictData)

    # noinspection PyMethodMayBeStatic
    def Update(self):
        # 每帧需要调用一次，处理select中的事件消息
        import common.async_net.dispatcher.xx_dispatcher_mgr as xx_dispatcher_mgr
        xx_dispatcher_mgr.Update()

        self._ClearToDestroyConnection()

    def GetAllDataStr(self):
        listConnectionData = []
        for nID, ConnectionObj in self.m_dictConnection.items():
            szColName = ConnectionObj.F_GetDataColName()
            szData = ConnectionObj.F_GetDataStr()
            listConnectionData.append(szColName)
            listConnectionData.append(szData)
            listConnectionData.append("")

        import common.async_net.dispatcher.xx_dispatcher_mgr as xx_dispatcher_mgr
        xx_dispatcher_mgr.GetAllDataStr()

        return "\n".join(listConnectionData) + "\n" + xx_dispatcher_mgr.GetAllDataStr()

    # ********************************************************************************
    # to destroy
    # ********************************************************************************
    def F_SetConnectionToDestroy(self, nID):
        self.m_LoggerObj.debug("nID:%d", nID)
        if nID not in self.m_dictToDestroyConnection:
            self.m_dictToDestroyConnection[nID] = True

    def _ClearToDestroyConnection(self):
        listToDestroy = list(self.m_dictToDestroyConnection.keys())
        for nID in listToDestroy:
            self.DestroyConnection(nID)

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
        assert szIp is not None
        assert nPort is not None

        ConnectionObj = self._GetConnection(nID)
        return ConnectionObj.F_Accept(szIp, nPort)

    def F_OnRead(self, nID, dictData):
        self._HandleAsync(nID, dictData)

    def F_OnClose(self, nID):
        ConnectionObj = self._GetConnection(nID)
        ConnectionObj.F_OnClose()

    # ********************************************************************************
    # async callback
    # ********************************************************************************
    def _GenAsyncID(self):
        self.m_nAsyncID += 1
        return self.m_nAsyncID

    def _AddAsyncCallback(self, nAsyncID, funCallback, tupleArg):
        self.m_LoggerObj.debug("asyncid:%d, arg:%s", nAsyncID, str(tupleArg))

        assert nAsyncID not in self.m_dictAsyncID2Callback
        self.m_dictAsyncID2Callback[nAsyncID] = (funCallback, tupleArg)

    def _RemoveAsyncCallback(self, nAsyncID):
        self.m_LoggerObj.debug("asyncid:%d", nAsyncID)
        assert nAsyncID in self.m_dictAsyncID2Callback
        del self.m_dictAsyncID2Callback[nAsyncID]

    def _GetAsyncCallback(self, nAsyncID):
        self.m_LoggerObj.debug("asyncid:%d", nAsyncID)

        assert nAsyncID in self.m_dictAsyncID2Callback
        return self.m_dictAsyncID2Callback[nAsyncID]

    def _HandleAsync(self, nID, dictData):
        self.m_LoggerObj.debug("id:%d, dictData:%s", nID, str(dictData))

        import common.async_net.connection.xx_connection as xx_connection
        if xx_connection.EAsyncName.eAsyncID in dictData:
            nAsyncID = dictData[xx_connection.EAsyncName.eAsyncID]
            self.m_LoggerObj.debug("call asyncid:%d", nAsyncID)

            funCallback, tupleArg = self._GetAsyncCallback(nAsyncID)
            self._RemoveAsyncCallback(nAsyncID)

            dictRetData = funCallback(dictData, *tupleArg)

        else:
            ConnectionObj = self._GetConnection(nID)
            dictRetData = ConnectionObj.F_OnRead(dictData)

        if xx_connection.EAsyncName.eRetAsyncID in dictData:
            if dictRetData is None or not isinstance(dictRetData, dict):
                self.m_LoggerObj.error("ret data error, id:%d, dictData:%s, dictRetData:%s",
                                       nID,
                                       str(dictData),
                                       str(dictRetData))
                dictRetData = {}

            nRetAsyncID = dictData[xx_connection.EAsyncName.eRetAsyncID]

            assert xx_connection.EAsyncName.eAsyncID not in dictRetData
            dictRetData[xx_connection.EAsyncName.eAsyncID] = nRetAsyncID

            self.Send(nID, dictRetData)

            self.m_LoggerObj.debug("send ret async id:%d, dictRetData:%s", nRetAsyncID, str(dictRetData))


def CreateConnectionData(nSocketListen=1,
                         ExecutorObj=None,
                         szIp=None, nPort=None,
                         nAutoReconnectMaxCount=None,
                         nAutoReconnectInterval=None,
                         bConnectionAccepted=False,
                         ):
    assert nSocketListen > 0

    dictData = {"socket_listen": nSocketListen}

    if ExecutorObj is not None:
        dictData["executor"] = ExecutorObj

    if szIp is not None:
        assert isinstance(szIp, str)
        dictData["ip"] = szIp

    if nPort is not None:
        assert isinstance(nPort, int)
        dictData["port"] = nPort

    if nAutoReconnectMaxCount is not None:
        assert isinstance(nAutoReconnectMaxCount, int)
        dictData["auto_reconnect_max_count"] = nAutoReconnectMaxCount

    if nAutoReconnectInterval is not None:
        dictData["auto_reconnect_interval"] = nAutoReconnectInterval

    dictData["connection_accepted"] = bConnectionAccepted

    return dictData


g_XxConnectionMgrObj = XxConnectionMgr()

CreateConnection = g_XxConnectionMgrObj.CreateConnection
Listen = g_XxConnectionMgrObj.Listen
Connect = g_XxConnectionMgrObj.Connect
Send = g_XxConnectionMgrObj.Send
SendAsync = g_XxConnectionMgrObj.SendAsync
Update = g_XxConnectionMgrObj.Update
Destroy = g_XxConnectionMgrObj.Destroy
DestroyConnection = g_XxConnectionMgrObj.DestroyConnection
GetAllDataStr = g_XxConnectionMgrObj.GetAllDataStr

F_OnConnect = g_XxConnectionMgrObj.F_OnConnect
F_OnDisconnect = g_XxConnectionMgrObj.F_OnDisconnect
F_Accept = g_XxConnectionMgrObj.F_Accept
F_OnRead = g_XxConnectionMgrObj.F_OnRead
F_OnClose = g_XxConnectionMgrObj.F_OnClose

F_SetConnectionToDestroy = g_XxConnectionMgrObj.F_SetConnectionToDestroy
