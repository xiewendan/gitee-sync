# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2021/3/18 21:05

# desc:

import importlib

import common.my_log as my_log


class EDataName:
    eModule = "module"
    eFunction = "function"
    eArg = "arg"


class MessageDispatcher:
    """"""

    def __init__(self):
        self.m_LoggerObj = my_log.MyLog(__file__)

    @my_log.SeperateWrap()
    def OnRecv(self, nID, dictData):
        self.m_LoggerObj.debug("id:%s, dictData:%s", nID, Str(dictData))

        szModule = dictData[EDataName.eModule]
        szFunction = dictData[EDataName.eFunction]
        listArg = dictData[EDataName.eArg]

        # noinspection PyBroadException
        try:
            ModuleObj = importlib.import_module(szModule)
            FunctionObj = getattr(ModuleObj, szFunction)
            return FunctionObj(nID, *tuple(listArg))

        except Exception as ExceptionObj:
            import common.my_trackback as my_traceback
            my_traceback.OnException()

    @staticmethod
    def F_CreateRpcData(szModule, szFunction, listArg):
        dictMsgData = {
            EDataName.eModule: szModule,
            EDataName.eFunction: szFunction,
            EDataName.eArg: listArg,
        }

        return dictMsgData

    @my_log.SeperateWrap()
    def CallRpc(self, nConnectionID, szModule, szFunction, listArg, Callback=None, tupleArg=None):
        self.m_LoggerObj.info("nID:%d, module:%s, function:%s, arg:%s", nConnectionID, szModule, szFunction,
                              Str(listArg))

        import common.async_net.xx_connection_mgr as xx_connection_mgr
        dictRpcData = self.F_CreateRpcData(szModule, szFunction, listArg)
        xx_connection_mgr.SendAsync(nConnectionID, dictRpcData, funCallback=Callback, tupleArg=tupleArg)


g_MessageDispatcher = MessageDispatcher()
OnRecv = g_MessageDispatcher.OnRecv
CallRpc = g_MessageDispatcher.CallRpc
F_CreateRpcData = g_MessageDispatcher.F_CreateRpcData
