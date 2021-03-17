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
