class BaseFactory:
    """"""

    def __init__(self):
        import common.my_log as my_log

        self.m_LoggerObj = my_log.MyLog(__file__)

        self.m_dictCls = {}

    def GetClassData(self):
        """

        :return:
            [
                [
                    "common/async_net/connection", # 相对当前目录
                    r"^xx_[_a-zA-Z0-9]*.py$", # 文件正则表达式
                    xx_connection_base.XxConnectionBase # 基类，要求基类实现GetType()静态函数方法，返回一个nType，表明子类的类型，Create传入nType
                ]
            ]
        """
        NotImplementedError
        return []

    def RegisterAll(self):
        self.m_LoggerObj.info("register all class")

        import os
        import common.util as util

        szCwd = os.getcwd()
        listClassObj = []
        listClassData = self.GetClassData()

        for listData in listClassData:
            szRPath = listData[0]
            szReg = listData[1]
            BaseClassObj = listData[2]

            listClassObj.extend(
                util.FilterClassObj(
                    os.path.join(szCwd, szRPath),
                    szReg,
                    BaseClassObj))

        for ConnectionClassObj in listClassObj:
            self._RegisterClass(ConnectionClassObj)

    def UnregisterAll(self):
        self.m_LoggerObj.info("unregister all connection class")
        self.m_dictCls = {}

    def Create(self, nType, dictData):
        self.m_LoggerObj.debug("type:%d, dictData:%s", nType, Str(dictData))
        assert nType in self.m_dictCls
        assert dictData is not None

        ClsObj = self.m_dictCls[nType]

        return ClsObj(dictData)

    def _RegisterClass(self, ClsObj):
        nType = ClsObj.GetType()
        assert nType not in self.m_dictCls

        self.m_dictCls[nType] = ClsObj
        self.m_LoggerObj.debug("register class type: %s", nType)

    def _UnregisterClass(self, ClsObj):
        nType = ClsObj.GetType()
        assert nType in self.m_dictCls
        del self.m_dictCls[nType]
        self.m_LoggerObj.debug("unregister class type: %s", nType)
