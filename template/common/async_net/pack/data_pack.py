import json
import struct


class DataPack:
    """"""

    def __init__(self):
        self.m_nHeaderSize = 0
        self.m_nDataSize = 0

        self.m_ByteData = None

    def Pack(self, dictData):
        self.m_ByteData = json.dumps(dictData).encode("utf-8")
        self.m_nDataSize = len(self.m_ByteData)
        self.m_nHeaderSize = self._GetByteCount(self.m_nDataSize)

        szHeaderSizeFormat = self._GetFormatByValue(self.m_nHeaderSize)
        assert szHeaderSizeFormat == "B"

        szDataSizeFormat = self._GetFormatByValue(self.m_nDataSize)
        szFormat = ">B%s" % (szDataSizeFormat,)

        byteHeaderObj = struct.pack(szFormat, self.m_nHeaderSize, self.m_nDataSize)
        return byteHeaderObj + self.m_ByteData

    def Unpack(self, byteData):
        nLen = len(byteData)

        if nLen < 1:
            return None, None

        self.m_nHeaderSize = struct.unpack(">B", byteData[0])[0]
        if nLen < 1 + self.m_nHeaderSize:
            return None, None

        szFormat = ">" + self._GetFormatByByteCount(self.m_nHeaderSize)
        self.m_nDataSize = struct.unpack(szFormat, byteData[1:1 + self.m_nHeaderSize])[0]

        if nLen < 1 + self.m_nHeaderSize + self.m_nDataSize:
            return None, None

        byteDataOne = byteData[1 + self.m_nHeaderSize:1 + self.m_nHeaderSize + self.m_nDataSize]

        return json.loads(byteDataOne.decode("utf-8")), byteData[1 + self.m_nHeaderSize + self.m_nDataSize:]

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
