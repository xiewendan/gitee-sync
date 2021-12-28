# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2021/3/11 20:21

# desc: 缓存Dispatcher，包含二进制的BytesIO，同时解决序列化，加密等功能


import io

import common.async_net.dispatcher.xx_dispatcher as xx_dispatcher
import common.async_net.dispatcher.xx_dispatcher_base as xx_dispatcher_base
import common.async_net.pack.data_pack as data_pack


class XxBufferDispatcher(xx_dispatcher_base.XxDispatcherBase):
    """"""

    def __init__(self, dictData):
        super().__init__(dictData)

        self.m_WriteBufferObj = io.BytesIO()
        self.m_ReadBufferObj = io.BytesIO()
        self.m_RecvCount = 1024 * 1024

    def Destroy(self):
        super().Destroy()

        self.m_WriteBufferObj = io.BytesIO()
        self.m_ReadBufferObj = io.BytesIO()

    @staticmethod
    def GetType():
        return xx_dispatcher.EDispatcherType.eBuffer

    def Send(self, dictData):
        self.m_LoggerObj.debug("data:%s", Str(dictData))

        byteData = data_pack.Serialize(dictData)
        self.m_WriteBufferObj.write(byteData)

    def Writeable(self):
        return len(self.m_WriteBufferObj.getvalue()) > 0

    # ********************************************************************************
    # private
    # ********************************************************************************
    def _HandleRead(self):
        self.m_LoggerObj.debug("id:%d", self.m_nID)

        # 连接上事件
        if self.m_eDispatcherState == xx_dispatcher.EDispatcherState.eConnecting:
            import common.async_net.dispatcher.xx_dispatcher_mgr as xx_dispatcher_mgr
            xx_dispatcher_mgr.HandleConnectEvent(self.m_nID)

        # 接收数据
        try:
            byteData = self.m_SocketObj.recv(self.m_RecvCount)
        except BaseException as e:
            import common.async_net.dispatcher.xx_dispatcher_mgr as xx_dispatcher_mgr
            xx_dispatcher_mgr.HandleDisconnectEvent(self.m_nID)
            self.m_LoggerObj.error("socket recv data failed:%s", str(e))
            return

        if not byteData:
            self.m_LoggerObj.debug("closing, ip:%s, port:%d", self.m_szIp, self.m_nPort)
            import common.async_net.dispatcher.xx_dispatcher_mgr as xx_dispatcher_mgr
            xx_dispatcher_mgr.HandleDisconnectEvent(self.m_nID)
            return

        # 放到buff中
        self.m_ReadBufferObj.write(byteData)

        # 反序列化解析
        byteDataAll = self.m_ReadBufferObj.getvalue()
        while True:
            dictData, byteDataLeft = data_pack.UnserializeWithLeftByte(byteDataAll)

            if dictData is None:
                break

            byteDataAll = byteDataLeft

            import common.async_net.xx_connection_mgr as xx_connection_mgr
            xx_connection_mgr.F_OnRead(self.m_nID, dictData)

        self.m_ReadBufferObj = io.BytesIO(byteDataAll)
        self.m_ReadBufferObj.seek(0, 2)

    def _HandleWrite(self):
        self.m_LoggerObj.debug("id:%d", self.m_nID)

        # 连接上事件
        import common.async_net.dispatcher.xx_dispatcher_mgr as xx_dispatcher_mgr
        if self.m_eDispatcherState == xx_dispatcher.EDispatcherState.eConnecting:
            xx_dispatcher_mgr.HandleConnectEvent(self.m_nID)

        # 缓存中取出
        byteData = self.m_WriteBufferObj.getvalue()

        # 发送数据
        if len(byteData) <= 0:
            self.m_LoggerObj.debug("send data over, ip:%s, port:%d", self.m_szIp, self.m_nPort)
            return

        try:
            nSendedCount = self.m_SocketObj.send(byteData)
        except OSError:
            self.m_LoggerObj.error("send data failed, ip:%s, port:%d", self.m_szIp, self.m_nPort)
            xx_dispatcher_mgr.HandleDisconnectEvent(self.m_nID)
            return

        self.m_WriteBufferObj = io.BytesIO(byteData[nSendedCount:])
        self.m_WriteBufferObj.seek(0, 2)

    def _OnDisconnect(self):
        super()._OnDisconnect()

        self.m_WriteBufferObj = io.BytesIO()
        self.m_ReadBufferObj = io.BytesIO()
