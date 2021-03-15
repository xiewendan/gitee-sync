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

    def Destroy(self):
        super().Destroy()
        self.m_WriteBufferObj = io.BytesIO()
        self.m_ReadBufferObj = io.BytesIO()

    @staticmethod
    def GetType():
        return xx_dispatcher.EDispatcherType.eBuffer

    def Send(self, dictData):
        self.m_LoggerObj.debug("data:%s", str(dictData))

        byteData = data_pack.Serialize(dictData)
        self.m_WriteBufferObj.write(byteData)


    def _HandleRead(self, byteData):
        self.m_ReadBufferObj.write(byteData)

        byteDataLeft = self.m_ReadBufferObj.getvalue()
        while True:
            dictData, byteDataLeft = data_pack.UnserializeWithLeftByte(byteDataLeft)

            if dictData is None:
                break

            import common.async_net.xx_connection_mgr as xx_connection_mgr
            xx_connection_mgr.F_OnRead(dictData)

        self.m_ReadBufferObj = io.BytesIO(byteDataLeft)

    def _HandleWrite(self):
        byteData = self.m_WriteBufferObj.getvalue()

        if len(byteData) <= 0:
            self.m_LoggerObj.debug("send data over, ip:%s, port:%d", self.m_szIp, self.m_nPort)
            return

        # TODO 发送异常，先不考虑
        nSendedCount = self.m_SocketObj.send(byteData)
        self.m_WriteBufferObj = io.BytesIO(byteData[nSendedCount:])

        import common.async_net.xx_connection_mgr as xx_connection_mgr
        xx_connection_mgr.F_OnWrite()

    def Writeable(self):
        return len(self.m_WriteBufferObj.getvalue()) > 0

    # ********************************************************************************
    # selector
    # ********************************************************************************
    def _Modify(self, SocketObj, nMask, Callback):
        pass
