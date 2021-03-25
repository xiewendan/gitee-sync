import copy
import json
import struct


# 序列化，需要支持bytes格式的数据
# 格式修改
#       第一个字节：高位为Head长度所占字节数
#       第一个字节：低位为Data长度所占字节数
#       Head长度
#       Data长度
#       读取Header部分的长度：格式为json
#       读取Data长度，json中，dict["byte"] = ["key1", 长度, "key2", 长度， ]  以此来解析并赋值到json中

class DataPack:
    """"""

    def __init__(self):
        self.m_nHeaderSize = 0
        self.m_nDataSize = 0

        self.m_byteJsonData = None

        self.m_byteByteData = None
        self.m_listCurByteKey = []
        self.m_listByteKeys = []

        self.m_nOffsetByteData = 0

    def Pack(self, dictData):
        dictData = copy.deepcopy(dictData)
        byteDataBlock = self._ConvertBytesInDict(dictData)

        self.m_byteJsonData = json.dumps(dictData).encode("utf-8")
        self.m_nDataSize = len(self.m_byteJsonData)
        self.m_nHeaderSize = self._GetByteCount(self.m_nDataSize)

        szHeaderSizeFormat = self._GetFormatByValue(self.m_nHeaderSize)
        assert szHeaderSizeFormat == "B"

        szDataSizeFormat = self._GetFormatByValue(self.m_nDataSize)
        szFormat = ">B%s" % (szDataSizeFormat,)

        byteHeaderObj = struct.pack(szFormat, self.m_nHeaderSize, self.m_nDataSize)

        return byteHeaderObj + self.m_byteJsonData + byteDataBlock

    def Unpack(self, byteData):
        nLen = len(byteData)

        if nLen < 1:
            return None, None

        self.m_nHeaderSize = struct.unpack(">B", byteData[0:1])[0]
        if nLen < 1 + self.m_nHeaderSize:
            return None, None

        szFormat = ">" + self._GetFormatByByteCount(self.m_nHeaderSize)
        self.m_nDataSize = struct.unpack(szFormat, byteData[1:1 + self.m_nHeaderSize])[0]

        if nLen < 1 + self.m_nHeaderSize + self.m_nDataSize:
            return None, None

        byteDataOne = byteData[1 + self.m_nHeaderSize:1 + self.m_nHeaderSize + self.m_nDataSize]

        dictData = json.loads(byteDataOne.decode("utf-8"))
        if "byte_count" not in dictData:
            return dictData, byteData[1 + self.m_nHeaderSize + self.m_nDataSize:]
        else:
            nLenByteByteData = dictData["byte_count"]
            if nLen < 1 + self.m_nHeaderSize + self.m_nDataSize + nLenByteByteData:
                return None, None

            byteByteData = byteData[
                           1 + self.m_nHeaderSize + self.m_nDataSize: 1 + self.m_nHeaderSize + self.m_nDataSize + nLenByteByteData]

            self._RevertBytesInDict(dictData, byteByteData)

            return dictData, byteData[1 + self.m_nHeaderSize + self.m_nDataSize + nLenByteByteData:]

    def _ConvertBytesInDict(self, dictData):
        assert "byte_key" not in dictData
        assert "byte_count" not in dictData

        self.m_byteByteData = b''
        self.m_listCurByteKey = []
        self.m_listByteKeys = []

        self._RecursiveConvertBytesInDict(dictData)

        if len(self.m_listByteKeys) > 0:
            dictData["byte_key"] = self.m_listByteKeys
            dictData["byte_count"] = len(self.m_byteByteData)

        byteByteData = self.m_byteByteData
        self.m_byteByteData = b''
        self.m_listCurByteKey = []
        self.m_listByteKeys = []

        return byteByteData

    def _RecursiveConvertBytesInDict(self, dictData):
        for szKey, ValueObj in dictData.items():
            assert not isinstance(szKey, bytes)

            self.m_listCurByteKey.append(szKey)

            if isinstance(ValueObj, dict):
                self._RecursiveConvertBytesInDict(ValueObj)
            elif isinstance(ValueObj, list):
                self._RecursiveConvertBytesInList(ValueObj)
            elif isinstance(ValueObj, bytes):
                self.m_listByteKeys.append(copy.deepcopy(self.m_listCurByteKey))
                self.m_byteByteData += ValueObj
                dictData[szKey] = len(ValueObj)
            else:
                pass

            self.m_listCurByteKey.pop()

    def _RecursiveConvertBytesInList(self, listData):
        for nIndex, ValueObj in enumerate(listData):
            self.m_listCurByteKey.append(nIndex)

            if isinstance(ValueObj, dict):
                self._RecursiveConvertBytesInDict(ValueObj)
            elif isinstance(ValueObj, list):
                self._RecursiveConvertBytesInList(ValueObj)
            elif isinstance(ValueObj, bytes):
                self.m_listByteKeys.append(copy.deepcopy(self.m_listCurByteKey))
                self.m_byteByteData += ValueObj
                listData[nIndex] = len(ValueObj)
            else:
                pass

            self.m_listCurByteKey.pop()

    def _RevertBytesInDict(self, dictData, byteDataAll):
        assert "byte_key" in dictData
        assert "byte_count" in dictData

        self.m_nOffsetByteData = 0
        self.m_byteByteData = byteDataAll

        listByteKey = dictData["byte_key"]
        for listCurKey in listByteKey:
            self._RecursiveRevertbytesInDict(dictData, listCurKey)

        del dictData["byte_key"]
        del dictData["byte_count"]

        self.m_nOffsetByteData = 0
        self.m_byteByteData = b''

    def _RecursiveRevertbytesInDict(self, dictData, listCurKey):
        nLenCurKey = len(listCurKey)
        if nLenCurKey == 0:
            assert False
        elif nLenCurKey == 1:
            szKey = listCurKey[0]
            nLenByteByteData = dictData[szKey]
            dictData[szKey] = self.m_byteByteData[self.m_nOffsetByteData: self.m_nOffsetByteData + nLenByteByteData]
            self.m_nOffsetByteData += nLenByteByteData
        else:
            szKey = listCurKey[0]
            listCurKey.pop(0)
            self._RecursiveRevertbytesInDict(dictData[szKey], listCurKey)

    @staticmethod
    def _GetFormatByValue(nSize):
        assert isinstance(nSize, int)
        assert nSize >= 0

        if nSize <= 0xff:
            return "B"
        elif nSize <= 0xffff:
            return "H"
        elif nSize <= 0xffffffff:
            return "I"
        else:
            assert nSize <= 0xffffffffffffffff
            return "Q"

    @staticmethod
    def _GetFormatByByteCount(nByteCount):
        assert isinstance(nByteCount, int)
        assert nByteCount >= 0

        dictFormat = {
            1: "B",
            2: "H",
            4: "I",
            8: "Q"
        }

        assert nByteCount in dictFormat

        return dictFormat[nByteCount]

    @staticmethod
    def _GetByteCount(nSize):
        assert isinstance(nSize, int)
        if nSize <= 0xff:
            return 1
        elif nSize <= 0xffff:
            return 2
        elif nSize <= 0xffffffff:
            return 3
        else:
            return 4


def Serialize(dictData):
    DataPackObj = DataPack()
    return DataPackObj.Pack(dictData)


def Unserialize(byteData):
    DataPackObj = DataPack()
    dictData, byteDataLeft = DataPackObj.Unpack(byteData)
    return dictData


def UnserializeWithLeftByte(byteData):
    DataPackObj = DataPack()
    dictData, byteDataLeft = DataPackObj.Unpack(byteData)
    return dictData, byteDataLeft
