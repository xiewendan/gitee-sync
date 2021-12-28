# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2021/2/2 19:10

# desc: 服务类基类，所有服务的封装，避免base_app.py不断的膨胀


import common.my_log as my_log
import common.my_exception as my_exception


class EServiceState:
    eCreate = 1
    eIniting = 2
    eInit = 3
    eDestroying = 4
    eDestroy = 5


class ServiceBase:
    def __init__(self):
        self.m_eState = EServiceState.eCreate
        self.m_AppObj = None
        self.m_LoggerObj = my_log.MyLog(__file__)

    @staticmethod
    def GetOptList():
        return []

    @staticmethod
    def GetName():
        return "service_base"

    def _GetDepServiceList(self):
        return []

    def GetApp(self):
        return self.m_AppObj

    def Init(self, AppObj, listInitingServiceName: list):
        """初始化AppObj"""
        self.m_LoggerObj.debug("Init: %s", Str(listInitingServiceName))
        self.m_AppObj = AppObj

        if self.m_eState == EServiceState.eInit:
            return

        elif self.m_eState == EServiceState.eIniting:
            szError = self._FormatInitingServiceName(listInitingServiceName)
            raise my_exception.MyException("service依赖关系死循环了:\n%s" % szError)

        assert self.m_eState == EServiceState.eCreate, "未初始化状态"
        self.m_eState = EServiceState.eIniting
        listInitingServiceName.append(self.GetName())
        self.m_LoggerObj.debug("%s Initing", self.GetName())

        listDepServiceName = self._GetDepServiceList()
        for szDepServiceName in listDepServiceName:
            self.m_AppObj.GetService(szDepServiceName).Init(self.m_AppObj, listInitingServiceName)

        self._OnInit()

        listInitingServiceName.pop()
        self.m_eState = EServiceState.eInit
        self.m_LoggerObj.debug("%s Init", self.GetName())

    def _OnInit(self):
        pass

    def Destroy(self):
        self.m_LoggerObj.debug("Destroy")

        self.m_eState = EServiceState.eDestroying

        self._OnDestroy()

        self.m_eState = EServiceState.eDestroy

    def _OnDestroy(self):
        pass

    def _FormatInitingServiceName(self, listInitingServiceName):
        self.m_LoggerObj.debug("%s", str(listInitingServiceName))

        szCurName = self.GetName()
        listInitingServiceName.append(szCurName)

        listPrintServiceName = []
        for szName in listInitingServiceName:
            if szName == szCurName:
                listPrintServiceName.append("->" + szName)
            else:
                listPrintServiceName.append("  " + szName)

        return "\n".join(listPrintServiceName)
