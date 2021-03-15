# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2021/3/11 20:28

# desc: dispatcher管理器，管理所有的dispatcher。其中，selectors等的event注册和响应，可以放到这里

__all__ = ["CreateDispatcher"]

import selectors
import socket

g_Timeout = 0.01
g_RecvCount = 1024


class XxDispatcherMgr:
    """"""

    def __init__(self):
        import common.my_log as my_log
        import common.async_net.dispatcher.xx_dispatcher_factory as xx_dispatcher_factory

        self.m_LoggerObj = my_log.MyLog(__file__)

        self.m_dictDispathcer = {}

        self.m_DispatcherFactory = xx_dispatcher_factory.XxDispatcherFactory()
        self.m_DispatcherFactory.RegisterAll()

        self.m_nRegisterCount = 0
        self.m_SelectorObj = selectors.DefaultSelector()

        self.m_dictSocketFileNo2DispatcherID = {}

    def Destroy(self):
        listID = list(self.m_dictDispathcer.keys())
        for nID in listID:
            self.DestroyDispatcher(nID)

        assert len(self.m_dictDispathcer) == 0

        self.m_DispatcherFactory.UnregisterAll()

        self.m_SelectorObj = None
        assert self.m_nRegisterCount == 0

        assert len(self.m_dictSocketFileNo2DispatcherID) == 0

    def CreateDispatcher(self, nType, dictData):
        self.m_LoggerObj.debug("type:%d, dictData:%s", nType, str(dictData))

        DispatcherObj = self.m_DispatcherFactory.CreateDispatcher(nType, dictData)

        self._AddDispatcher(DispatcherObj)

        return DispatcherObj.ID

    def Listen(self, nID, szIp, nPort, nListenCount):
        self.m_LoggerObj.debug("nID:%d, szIp:%s, port:%d, listencoutn:%d", nID, szIp, nPort, nListenCount)

        DispatcherObj = self.GetDispatcher(nID)
        DispatcherObj.CreateSocket(socket.AF_INET, socket.SOCK_STREAM)
        DispatcherObj.SetReuseAddress()
        DispatcherObj.Bind(szIp, nPort)
        DispatcherObj.Listen(nListenCount)

        self._AddSocketFileNo(DispatcherObj.SocketObj.fileno(), DispatcherObj.ID)
        self._Register(DispatcherObj.SocketObj, selectors.EVENT_READ, self._AcceptCB)

    def GetDispatcher(self, nID):
        assert nID in self.m_dictDispathcer

        return self.m_dictDispathcer[nID]

    def Connect(self, nID, szIp, nPort):
        DispatcherObj = self.GetDispatcher(nID)
        DispatcherObj.CreateSocket(socket.AF_INET, socket.SOCK_STREAM)
        DispatcherObj.Connect(szIp, nPort)

        nFileNo = DispatcherObj.SocketObj.fileno()
        if nFileNo not in self.m_dictSocketFileNo2DispatcherID:
            self._AddSocketFileNo(DispatcherObj.SocketObj.fileno(), DispatcherObj.ID)
            self._Register(DispatcherObj.SocketObj, selectors.EVENT_READ | selectors.EVENT_WRITE, self._ReadWriteCB)

    def HandleConnectEvent(self, nDispatcherID):
        self._HandleConnectEvent(nDispatcherID)

    def HandleDisconnectEvent(self, nDispatcherID):
        self._HandleDisconnectEvent(nDispatcherID)

    def Send(self, nID, dictData):
        DispatcherObj = self.GetDispatcher(nID)
        DispatcherObj.Send(dictData)

        self._Modify(DispatcherObj.SocketObj, selectors.EVENT_READ | selectors.EVENT_WRITE, self._ReadWriteCB)

    def Update(self):
        self.m_LoggerObj.debug("select update event")

        listEvent = self._Select(g_Timeout)
        for KeyObj, nMask in listEvent:
            CallbackObj = KeyObj.data
            CallbackObj(KeyObj.fileobj, nMask)

    def SetSocket(self, nID, SocketObj):
        DispatcherObj = self.GetDispatcher(nID)
        DispatcherObj.SetSocket(SocketObj)

    def DestroyDispatcher(self, nDispatcherID):
        DispatcherObj = self.GetDispatcher(nDispatcherID)
        SocketObj = DispatcherObj.SocketObj
        nFileNo = SocketObj.fileno()

        self._RemoveFileNo(nFileNo)
        self._UnRegister(SocketObj)

        DispatcherObj.Destroy()
        del self.m_dictDispathcer[nDispatcherID]

    # ********************************************************************************
    # dictDispatcher
    # ********************************************************************************
    def _AddDispatcher(self, DispatcherObj):
        self.m_LoggerObj.debug("dispatcher id:%d", DispatcherObj.ID)

        nID = DispatcherObj.ID
        assert nID not in self.m_dictDispathcer

        self.m_dictDispathcer[nID] = DispatcherObj

    def _RemoveDispatcher(self, nID):
        self.m_LoggerObj.debug("dispatcher id:%d", nID)

        assert nID in self.m_dictDispathcer
        del self.m_dictDispathcer[nID]

    # ********************************************************************************
    # selector
    # ********************************************************************************
    def _Select(self, nTimeout):
        if self.m_nRegisterCount == 0:
            return []
        else:
            return self.m_SelectorObj.select(nTimeout)

    def _Register(self, SocketObj, nMask, Callback):
        self.m_LoggerObj.debug("socketobj:%s, mask:%d", SocketObj, nMask)
        assert isinstance(SocketObj, socket.socket)
        self.m_SelectorObj.register(SocketObj, nMask, Callback)
        self._AddRegisterCount(1)

    def _UnRegister(self, SocketObj):
        self.m_LoggerObj.debug("socketobj:%s", SocketObj)
        self.m_SelectorObj.unregister(SocketObj)
        self._AddRegisterCount(-1)

    def _AddRegisterCount(self, nCount):
        self.m_LoggerObj.debug("reigstercount:%d, count:%d", self.m_nRegisterCount, nCount)
        self.m_nRegisterCount += nCount
        assert self.m_nRegisterCount >= 0

    def _Modify(self, SocketObj, nMask, Callback):
        self.m_LoggerObj.debug("socketobj:%s, mask:%d, callback:%s", SocketObj, nMask, Callback)

        self.m_SelectorObj.modify(SocketObj, nMask, Callback)

    # ********************************************************************************
    # fileno to dispatcher id
    # ********************************************************************************
    def _AddSocketFileNo(self, nFileNo, nDispatcherID):
        self.m_LoggerObj.debug("fileno:%d, dispatcherid:%d", nFileNo, nDispatcherID)
        assert nFileNo not in self.m_dictSocketFileNo2DispatcherID
        self.m_dictSocketFileNo2DispatcherID[nFileNo] = nDispatcherID

    def _RemoveFileNo(self, nFileNo):
        assert nFileNo in self.m_dictSocketFileNo2DispatcherID
        del self.m_dictSocketFileNo2DispatcherID[nFileNo]

    def _GetDispatcherID(self, nFileNo):
        assert nFileNo in self.m_dictSocketFileNo2DispatcherID
        return self.m_dictSocketFileNo2DispatcherID[nFileNo]

    # ********************************************************************************
    # selector event
    # ********************************************************************************
    def _AcceptCB(self, ListenSocketObj, nMask):
        self.m_LoggerObj.debug("listensocket:%s, mask:%d", str(ListenSocketObj), nMask)

        SocketObj, AddrObj = ListenSocketObj.accept()
        szIp, nPort = AddrObj
        self.m_LoggerObj.info("new client come, ip:%s, port:%d", szIp, nPort)

        self._HandleAcceptEvent(ListenSocketObj, SocketObj, szIp, nPort)

    def _ReadWriteCB(self, SocketObj, nMask):
        self.m_LoggerObj.debug("socketobj:%s, mask:%d", str(SocketObj), nMask)

        if nMask & selectors.EVENT_READ:
            self._ReadCB(SocketObj)
        elif nMask & selectors.EVENT_WRITE:
            self._WriteCB(SocketObj)
        else:
            self.m_LoggerObj.error("can not handle event:%s", nMask)

    def _ReadCB(self, SocketObj):
        self.m_LoggerObj.debug("socketobj:%s", SocketObj)

        nDispatcherID = self._GetDispatcherID(SocketObj.fileno())
        self._HandleReadEvent(nDispatcherID)

    def _WriteCB(self, SocketObj):
        self.m_LoggerObj.debug("socketobj:%s", SocketObj)

        nDispatcherID = self._GetDispatcherID(SocketObj.fileno())
        self._HandleWriteEvent(nDispatcherID)

    def _HandleAcceptEvent(self, ListenSocketObj, SocketObj, szIp, nPort):
        nServerFileNo = ListenSocketObj.fileno()
        nServerDispatcherID = self._GetDispatcherID(nServerFileNo)
        ServerDispatcherObj = self.GetDispatcher(nServerDispatcherID)

        nClientID = ServerDispatcherObj.HanleAcceptEvent(szIp, nPort)
        self.SetSocket(nClientID, SocketObj)
        self.HandleConnectEvent(nClientID)

    def _HandleConnectEvent(self, nDispatcherID):
        DispatcherObj = self.GetDispatcher(nDispatcherID)
        DispatcherObj.HandleConnectEvent()

        # 管理对象，并注册
        SocketObj = DispatcherObj.SocketObj
        nFileNo = SocketObj.fileno()
        if nFileNo not in self.m_dictSocketFileNo2DispatcherID:
            self._AddSocketFileNo(SocketObj.fileno(), nDispatcherID)
            self._Register(SocketObj, selectors.EVENT_READ, self._ReadWriteCB)

    def _HandleDisconnectEvent(self, nDispatcherID):
        DispatcherObj = self.GetDispatcher(nDispatcherID)
        SocketObj = DispatcherObj.SocketObj

        self._UnRegister(SocketObj)
        self._RemoveFileNo(SocketObj.fileno())

        DispatcherObj.HandleDisconnectEvent()

    def _HandleReadEvent(self, nDispatcherID):
        DispatcherObj = self.GetDispatcher(nDispatcherID)
        DispatcherObj.HandleReadEvent()

    def _HandleWriteEvent(self, nDispatcherID):
        DispatcherObj = self.GetDispatcher(nDispatcherID)
        DispatcherObj.HandleWriteEvent()

        if not DispatcherObj.Writeable():
            self._Modify(DispatcherObj.SocketObj, selectors.EVENT_READ, self._ReadWriteCB)


g_DispatcherMgr = XxDispatcherMgr()
CreateDispatcher = g_DispatcherMgr.CreateDispatcher
GetDispatcher = g_DispatcherMgr.GetDispatcher
Listen = g_DispatcherMgr.Listen
Connect = g_DispatcherMgr.Connect
Send = g_DispatcherMgr.Send
Update = g_DispatcherMgr.Update
SetSocket = g_DispatcherMgr.SetSocket
Destroy = g_DispatcherMgr.Destroy
DestroyDispatcher = g_DispatcherMgr.DestroyDispatcher
HandleConnectEvent = g_DispatcherMgr.HandleConnectEvent
HandleDisconnectEvent = g_DispatcherMgr.HandleDisconnectEvent
