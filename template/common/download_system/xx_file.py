class XxFile:
    def __init__(self, szMd5, szFileFPath, nSize, szMode="rb"):
        self.m_szMd5 = szMd5
        self.m_szFileFPath = szFileFPath
        self.m_nSize = nSize

        self.m_FileObj = open(szFileFPath, szMode)

    def CheckSame(self, szMd5, szFileFPath, nSize):
        return self.m_szMd5 == szMd5 and self.m_szFileFPath == szFileFPath and self.m_nSize == nSize

    def Read(self, nOffset, nBlockSize):
        assert self.m_FileObj.seekable()

        self.m_FileObj.seek(nOffset)
        return self.m_FileObj.read(nBlockSize)

    def Write(self, nOffset, byteData):
        assert self.m_FileObj.seekable()

        self.m_FileObj.seek(nOffset)
        self.m_FileObj.write(byteData)

    def Close(self):
        self.m_FileObj.close()
        self.m_FileObj = None
