import importlib


class EDataName:
    eModule = "module"
    eFunction = "function"
    eArg = "arg"


def OnRecv(nID, dictData):
    szModule = dictData[EDataName.eModule]
    szFunction = dictData[EDataName.eFunction]
    listArg = dictData[EDataName.eArg]

    ModuleObj = importlib.import_module(szModule)
    FunctionObj = getattr(ModuleObj, szFunction)

    # noinspection PyBroadException
    try:
        return FunctionObj(nID, *tuple(listArg))
    except Exception as ExceptionObj:
        import common.my_trackback as my_traceback
        my_traceback.OnException()


def CreateRpcData(szModule, szFunction, listArg):
    dictMsgData = {
        EDataName.eModule: szModule,
        EDataName.eFunction: szFunction,
        EDataName.eArg: listArg,
    }

    return dictMsgData


def CallRpc(szModule, szFunction, listArg, )
    import common.async_net.xx_connection_mgr as xx_connection_mgr
    xx_connection_mgr.SendAsync(nConnectionID, dictGMCommand, )
    nConnectionID, "logic.gm.gm_command", "Do", [szCommand], GMCallback, ("xjc", 1, True)
