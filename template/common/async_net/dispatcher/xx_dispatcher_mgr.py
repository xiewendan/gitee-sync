# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2021/3/11 20:28

# desc: dispatcher管理器，管理所有的dispatcher。其中，selectors等的event注册和响应，可以放到这里

__all__ = ["CreateDispatcher"]

import selectors
import socket

import common.my_log as my_log

g_Timeout = 0.01
g_RecvCount = 1024


class XxDispatcherMgr:
    """"""

    def __init__(self):
        import common.async_net.dispatcher.xx_dispatcher_factory as xx_dispatcher_factory

        self.m_LoggerObj = my_log.MyLog(__file__)

        self.m_dictDispathcer = {}

        self.m_DispatcherFactory = xx_dispatcher_factory.XxDispatcherFactory()
        self.m_DispatcherFactory.RegisterAll()

        self.m_nRegisterCount = 0
        self.m_SelectorObj = selectors.DefaultSelector()

        self.m_dictSocketFileNo2DispatcherID = {}

    def Destroy(self):
        self.m_LoggerObj.info("")

        listDispatcherID = list(self.m_dictDispathcer.keys())
        for nDispatcherID in listDispatcherID:
            self.DestroyDispatcher(nDispatcherID)

        assert len(self.m_dictDispathcer) == 0

        self.m_DispatcherFactory.UnregisterAll()

        self.m_SelectorObj = None
        assert self.m_nRegisterCount == 0

        assert len(self.m_dictSocketFileNo2DispatcherID) == 0

    def CloseDispatcher(self, nDispatcherID):
        self.m_LoggerObj.debug("dispatcherID:%d", nDispatcherID)

        DispatcherObj = self._GetDispatcher(nDispatcherID)
        DispatcherObj.Close()

    def CreateDispatcher(self, nType, dictData):
        self.m_LoggerObj.debug("type:%d, dictData:%s", nType, str(dictData))

        DispatcherObj = self.m_DispatcherFactory.CreateDispatcher(nType, dictData)
        self._AddDispatcher(DispatcherObj)

        self.m_LoggerObj.debug("dispatcherID:%d", DispatcherObj.ID)

        return DispatcherObj.ID

    def DestroyDispatcher(self, nDispatcherID):
        self.m_LoggerObj.debug("dispatcherID:%d", nDispatcherID)

        DispatcherObj = self._GetDispatcher(nDispatcherID)
        DispatcherObj.Destroy()

        del self.m_dictDispathcer[nDispatcherID]

    def Listen(self, nDispatcherID, szIp, nPort, nListenCount):
        self.m_LoggerObj.debug("nID:%d, szIp:%s, port:%d, listencoutn:%d", nDispatcherID, szIp, nPort, nListenCount)

        DispatcherObj = self._GetDispatcher(nDispatcherID)
        DispatcherObj.CreateSocket(socket.AF_INET, socket.SOCK_STREAM)
        # DispatcherObj.SetReuseAddress()
        DispatcherObj.Bind(szIp, nPort)
        DispatcherObj.Listen(nListenCount)

        self._AddSocketFileNo(DispatcherObj.SocketObj.fileno(), nDispatcherID)
        self._Register(DispatcherObj.SocketObj, selectors.EVENT_READ, self._AcceptCB)

    def Connect(self, nDispatcherID, szIp, nPort):
        self.m_LoggerObj.debug("dispatcherID:%d, ip:%s, port:%d", nDispatcherID, szIp, nPort)

        DispatcherObj = self._GetDispatcher(nDispatcherID)
        DispatcherObj.CreateSocket(socket.AF_INET, socket.SOCK_STREAM)
        DispatcherObj.Connect(szIp, nPort)

        self._AddSocketFileNo(DispatcherObj.SocketObj.fileno(), DispatcherObj.ID)
        self._Register(DispatcherObj.SocketObj, selectors.EVENT_READ | selectors.EVENT_WRITE, self._ReadWriteCB)

    def Send(self, nDispatcherID, dictData):
        self.m_LoggerObj.debug("dispatcherID:%d, dictdata:%s", nDispatcherID, str(dictData))

        DispatcherObj = self._GetDispatcher(nDispatcherID)
        DispatcherObj.Send(dictData)

        self._Modify(DispatcherObj.SocketObj, selectors.EVENT_READ | selectors.EVENT_WRITE, self._ReadWriteCB)

    def Update(self):
        # self.m_LoggerObj.debug("select update event")

        listEvent = self._Select(g_Timeout)

        for KeyObj, nMask in listEvent:
            CallbackObj = KeyObj.data

            SocketObj = KeyObj.fileobj
            nFileNo = SocketObj.fileno()
            nDispatcherID = self._GetDispatcherID(nFileNo)

            CallbackObj(nDispatcherID, nMask)

    def SetSocket(self, nDispatcherID, SocketObj):
        self.m_LoggerObj.debug("dispatcherID:%s, SocketObj:%s", nDispatcherID, SocketObj)

        DispatcherObj = self._GetDispatcher(nDispatcherID)
        DispatcherObj.SetSocket(SocketObj)

    def HandleConnectEvent(self, nDispatcherID):
        self.m_LoggerObj.debug("dispatcherID:%d", nDispatcherID)

        self._HandleConnectEvent(nDispatcherID)

    def HandleDisconnectEvent(self, nDispatcherID):
        self.m_LoggerObj.debug("dispatcherID:%d", nDispatcherID)

        self._HandleDisconnectEvent(nDispatcherID)

    def GetIp(self, nDispatcherID):
        DispatcherObj = self._GetDispatcher(nDispatcherID)
        return DispatcherObj.Ip

    def GetPort(self, nDispatcherID):
        DispatcherObj = self._GetDispatcher(nDispatcherID)
        return DispatcherObj.Port

    # ********************************************************************************
    # dictDispatcher
    # ********************************************************************************
    def _AddDispatcher(self, DispatcherObj):
        self.m_LoggerObj.debug("dispatcher id:%d", DispatcherObj.ID)

        nDispatcherID = DispatcherObj.ID
        assert nDispatcherID not in self.m_dictDispathcer

        self.m_dictDispathcer[nDispatcherID] = DispatcherObj

    def _RemoveDispatcher(self, nDispatcherID):
        self.m_LoggerObj.debug("dispatcher id:%d", nDispatcherID)

        assert nDispatcherID in self.m_dictDispathcer
        del self.m_dictDispathcer[nDispatcherID]

    def _GetDispatcher(self, nDispatcherID):
        assert nDispatcherID in self.m_dictDispathcer

        return self.m_dictDispathcer[nDispatcherID]

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
        self.m_LoggerObj.debug("fileno:%d", nFileNo)

        assert nFileNo in self.m_dictSocketFileNo2DispatcherID
        del self.m_dictSocketFileNo2DispatcherID[nFileNo]

    def _GetDispatcherID(self, nFileNo):
        assert nFileNo in self.m_dictSocketFileNo2DispatcherID
        return self.m_dictSocketFileNo2DispatcherID[nFileNo]

    # ********************************************************************************
    # selector event
    # ********************************************************************************
    @my_log.SeperateWrap()
    def _AcceptCB(self, nDispatcherID, nMask):
        self.m_LoggerObj.debug("dispatcherid:%d, mask:%d", nDispatcherID, nMask)
        self._HandleAcceptEvent(nDispatcherID)

    @my_log.SeperateWrap()
    def _ReadWriteCB(self, nDispatcherID, nMask):
        self.m_LoggerObj.debug("disptacherID:%d, mask:%d", nDispatcherID, nMask)

        if nMask & selectors.EVENT_READ:
            self._ReadCB(nDispatcherID)
        elif nMask & selectors.EVENT_WRITE:
            self._WriteCB(nDispatcherID)
        else:
            self.m_LoggerObj.error("can not handle event, dispatcherID:%d, mask:%d", nDispatcherID, nMask)

    def _ReadCB(self, nDispatcherID):
        self.m_LoggerObj.debug("dispatcherID:%d", nDispatcherID)
        self._HandleReadEvent(nDispatcherID)

    def _WriteCB(self, nDispatcherID):
        self.m_LoggerObj.debug("dispatcherID:%d", nDispatcherID)
        self._HandleWriteEvent(nDispatcherID)

    def _HandleAcceptEvent(self, nDispatcherID):
        DispatcherObj = self._GetDispatcher(nDispatcherID)
        DispatcherObj.HanleAcceptEvent()

    def _HandleReadEvent(self, nDispatcherID):
        DispatcherObj = self._GetDispatcher(nDispatcherID)
        DispatcherObj.HandleReadEvent()

    def _HandleWriteEvent(self, nDispatcherID):
        DispatcherObj = self._GetDispatcher(nDispatcherID)
        DispatcherObj.HandleWriteEvent()

        if not DispatcherObj.Writeable():
            self._Modify(DispatcherObj.SocketObj, selectors.EVENT_READ, self._ReadWriteCB)

    def _HandleConnectEvent(self, nDispatcherID):
        DispatcherObj = self._GetDispatcher(nDispatcherID)
        DispatcherObj.HandleConnectEvent()

        # 管理对象，并注册
        SocketObj = DispatcherObj.SocketObj
        nFileNo = SocketObj.fileno()
        if nFileNo not in self.m_dictSocketFileNo2DispatcherID:
            self._AddSocketFileNo(SocketObj.fileno(), nDispatcherID)
            self._Register(SocketObj, selectors.EVENT_READ, self._ReadWriteCB)

    def _HandleDisconnectEvent(self, nDispatcherID):
        DispatcherObj = self._GetDispatcher(nDispatcherID)
        SocketObj = DispatcherObj.SocketObj

        self._UnRegister(SocketObj)
        self._RemoveFileNo(SocketObj.fileno())

        DispatcherObj.HandleDisconnectEvent()


g_DispatcherMgr = XxDispatcherMgr()
CreateDispatcher = g_DispatcherMgr.CreateDispatcher
Listen = g_DispatcherMgr.Listen
Connect = g_DispatcherMgr.Connect
Send = g_DispatcherMgr.Send
Update = g_DispatcherMgr.Update
SetSocket = g_DispatcherMgr.SetSocket
Destroy = g_DispatcherMgr.Destroy
DestroyDispatcher = g_DispatcherMgr.DestroyDispatcher
HandleConnectEvent = g_DispatcherMgr.HandleConnectEvent
HandleDisconnectEvent = g_DispatcherMgr.HandleDisconnectEvent
GetIp = g_DispatcherMgr.GetIp
GetPort = g_DispatcherMgr.GetPort
CloseDispatcher = g_DispatcherMgr.CloseDispatcher
