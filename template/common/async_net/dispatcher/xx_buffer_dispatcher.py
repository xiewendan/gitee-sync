# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2021/3/11 20:21

# desc: 缓存Dispatcher，包含二进制的BytesIO，同时解决序列化，加密等功能


import common.async_net.dispatcher.xx_dispatcher as xx_dispatcher
import common.async_net.dispatcher.xx_dispatcher_base as xx_dispatcher_base
import common.async_net.pack.data_pack as data_pack


class XxBufferDispatcher(xx_dispatcher_base.XxDispatcherBase):
    """"""

    def __init__(self, dictData):
        super().__init__(dictData)

    @staticmethod
    def GetType():
        return xx_dispatcher.EDispatcherType.eBuffer

    def Send(self, dictData):
        self.m_LoggerObj.debug("data:%s", str(dictData))

        # TODO 1
        byteData = data_pack.Serialize(dictData)
        pass
