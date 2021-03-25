# desc: 1、缓存Dispatcher，包含二进制的BytesIO，同时解决序列化，加密等功能
#       2、将需要发送的文件块信息放到一个队列中，当发送WriteBuffer已经发送完成，从文件块信息中取出，再写到WriteBuffer中，直到缓存和文件块的信息都发送完毕，
#          才算发送完毕


import common.download_system.xx_file as xx_file
import common.async_net.dispatcher.xx_buffer_dispatcher as xx_buffer_dispatcher
import common.async_net.dispatcher.xx_dispatcher as xx_dispatcher

g_MaxSendBuffSize = 10000000  # 10 M


class XxFileDispatcher(xx_buffer_dispatcher.XxBufferDispatcher):
    def __init__(self, dictData):
        super().__init__(dictData)

        self.m_RecvCount = 1024 * 1024 * 10

        self.m_XxFileObj = None

        self.m_listToSendFileBlock = []

    def Destroy(self):
        super().Destroy()

        if self.m_XxFileObj is not None:
            self.m_XxFileObj.Close()
            self.m_XxFileObj = None

        """
        {
            "md5": szMd5,
            "file_name": szFileName,
            "size": nSize,
            "block_index": nBlockIndex,
            "offset": nBlockSize * nBlockIndex,
            "block_size": nBlockSize,
            "file_fpath": szFileFPath
        }
        """
        self.m_listToSendFileBlock = []

    @staticmethod
    def GetType():
        return xx_dispatcher.EDispatcherType.eFile

    def SendFile(self, dictData):
        self.m_LoggerObj.debug("data:%s", Str(dictData))

        self.m_listToSendFileBlock.append(dictData)

    def Writeable(self):
        return len(self.m_WriteBufferObj.getvalue()) > 0 or len(self.m_listToSendFileBlock) > 0

    # ********************************************************************************
    # private
    # ********************************************************************************
    def _HandleWrite(self):
        self._FileToSendBuff()

        super()._HandleWrite()

    def _OnDisconnect(self):
        super()._OnDisconnect()

        if self.m_XxFileObj is not None:
            self.m_XxFileObj.Close()
            self.m_XxFileObj = None

        self.m_listToSendFileBlock = []

    def _FileToSendBuff(self):
        self.m_LoggerObj.debug("")

        if len(self.m_listToSendFileBlock) == 0:
            return

        dictFileBlock = self.m_listToSendFileBlock.pop(0)
        self.m_LoggerObj.debug("dictFileBlock:%s", Str(dictFileBlock))

        nLenWriteBuffer = len(self.m_WriteBufferObj.getvalue())
        if nLenWriteBuffer + dictFileBlock["block_size"] > g_MaxSendBuffSize:
            assert nLenWriteBuffer > 0, "发送缓存已经空了，还没办法从文件中取出数据放到缓存中，这是什么鬼"
            return

        # TODO
        szMd5 = dictFileBlock["md5"]
        szFileName = dictFileBlock["file_name"]
        nSize = dictFileBlock["size"]
        nOffset = dictFileBlock["offset"]
        nBlockSize = dictFileBlock["block_size"]
        szFileFPath = dictFileBlock["file_fpath"]

        if self.m_XxFileObj is not None:
            if not self.m_XxFileObj.CheckSame(szMd5, szFileFPath, nSize):
                self.m_XxFileObj.Close()
                self.m_XxFileObj = None

        if self.m_XxFileObj is None:
            self.m_XxFileObj = xx_file.XxFile(szMd5, szFileFPath, nSize)

        byteData = self.m_XxFileObj.Read(nOffset, nBlockSize)
        assert len(byteData) == nBlockSize
        dictFileBlock["byte_data_block"] = byteData

        del dictFileBlock["file_fpath"]
        del dictFileBlock["offset"]

        # TODO common模块函数依赖外部函数，需要考虑怎么采用注册的方式，实现依赖翻转
        import logic.connection.message_dispatcher as message_dispatcher
        dictRpcData = message_dispatcher.F_CreateRpcData("logic.gm.gm_command", "OnDownloadFileReceive", [dictFileBlock])

        self.Send(dictRpcData)
