# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2021/2/4 12:02

# desc: 自己的XxSocket对象


# TODO 实现不重复，不可修改基类，并继承
class ESocketState:
    eCreate = 1
    eConnect = 2
    eRegister = 3
    eUnregister = 4
    eDestroy = 5

    dictChange = {
        eCreate: (eRegister,eConnect),
        eConnect: (eRegister,),
        eRegister: (eUnregister,),
        eUnregister: (eDestroy,)
    }

    @staticmethod
    def CanChange(eOld, eNew):
        tupleNew = ESocketState.dictChange[eOld]
        return eNew in tupleNew


class XxSocket:
    def __init__(self, SocketObj):
        self.m_SocketObj = SocketObj
        self.m_eState = ESocketState.eCreate

        import common.my_log as my_log
        self.m_LoggerObj = my_log.MyLog(__file__)

    def GetSocketObj(self):
        return self.m_SocketObj

    def GetState(self):
        return self.m_eState

    def SetState(self, eState):
        self.m_LoggerObj.debug("old state:%s, new state:%s", self.m_eState, eState)

        if not ESocketState.CanChange(self.m_eState, eState):
            import common.my_exception as my_exception
            raise my_exception.MyException("change socket state error: %s, %s" % (str(self.m_eState), str(eState)))

        self.m_eState = eState
