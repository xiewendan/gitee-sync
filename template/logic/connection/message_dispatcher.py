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
        self.m_LoggerObj.debug("id:%s, dictData:%s", nID, str(dictData))

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
    def _CreateRpcData(szModule, szFunction, listArg):
        dictMsgData = {
            EDataName.eModule: szModule,
            EDataName.eFunction: szFunction,
            EDataName.eArg: listArg,
        }

        return dictMsgData

    @my_log.SeperateWrap()
    def CallRpc(self, nConnectionID, szModule, szFunction, listArg, Callback=None, tupleArg=None):
        self.m_LoggerObj.debug("nID:%d, module:%s, function:%s, arg:%s", nConnectionID, szModule, szFunction,
                               str(listArg))

        import common.async_net.xx_connection_mgr as xx_connection_mgr
        dictRpcData = self._CreateRpcData(szModule, szFunction, listArg)
        xx_connection_mgr.SendAsync(nConnectionID, dictRpcData, funCallback=Callback, tupleArg=tupleArg)


g_MessageDispatcher = MessageDispatcher()
OnRecv = g_MessageDispatcher.OnRecv
CallRpc = g_MessageDispatcher.CallRpc
