# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2021/5/28 12:09

# desc:


class KeyNode:
    def __init__(self, KeyObj, PreObj=None, NextObj=None):
        assert KeyObj is not None
        self.m_KeyObj = KeyObj
        self.m_PreObj = PreObj
        self.m_NextObj = NextObj

    @property
    def KeyObj(self):
        return self.m_KeyObj


class LRULinkQueue:
    # 队头是pop，队尾是push
    def __init__(self):
        import common.my_log as my_log
        self.m_LoggerObj = my_log.MyLog(__file__)

        self.m_HeadNodeObj = None
        self.m_TailNodeObj = None

        self.m_dictKeyToNode = {}

    def Push(self, KeyObj):
        self.m_LoggerObj.debug("Md5:%s", KeyObj)

        assert KeyObj is not None

        if KeyObj in self.m_dictKeyToNode:
            NodeObj = self.m_dictKeyToNode[KeyObj]
            if NodeObj == self.m_TailNodeObj:
                pass
            else:
                # 将NodeObj从当前链表中移除
                NodeObj.m_NextObj.m_PreObj = NodeObj.m_PreObj

                if NodeObj == self.m_HeadNodeObj:
                    self.m_HeadNodeObj = NodeObj.m_NextObj
                else:
                    NodeObj.m_PreObj.m_NextObj = NodeObj.m_NextObj

                # 将Node节点插入到链表尾部
                self.m_TailNodeObj.m_NextObj = NodeObj

                NodeObj.m_PreObj = self.m_TailNodeObj
                NodeObj.m_NextObj = None

                self.m_TailNodeObj = NodeObj
        else:
            NewNodeObj = KeyNode(KeyObj, self.m_TailNodeObj, None)
            self.m_dictKeyToNode[KeyObj] = NewNodeObj

            if self.m_TailNodeObj is not None:
                self.m_TailNodeObj.m_NextObj = NewNodeObj

            self.m_TailNodeObj = NewNodeObj

            if self.m_HeadNodeObj is None:
                self.m_HeadNodeObj = NewNodeObj

    def Top(self):
        if self.m_HeadNodeObj is None:
            return None
        else:
            return self.m_HeadNodeObj.KeyObj

    def _Tail(self):
        if self.m_TailNodeObj is None:
            return None
        else:
            return self.m_TailNodeObj.KeyObj

    def Pop(self, KeyObj=None):
        if KeyObj is None:
            if self.m_HeadNodeObj is None:
                return None
            else:
                KeyObj = self.m_HeadNodeObj.KeyObj

        self.m_LoggerObj.debug("KeyObj:%s", KeyObj)

        assert KeyObj in self.m_dictKeyToNode
        CurNodeObj = self.m_dictKeyToNode[KeyObj]
        del self.m_dictKeyToNode[KeyObj]

        if CurNodeObj.m_PreObj is not None:
            CurNodeObj.m_PreObj.m_NextObj = CurNodeObj.m_NextObj

        if CurNodeObj.m_NextObj is not None:
            CurNodeObj.m_NextObj.m_PreObj = CurNodeObj.m_PreObj

        if self.m_TailNodeObj == CurNodeObj:
            self.m_TailNodeObj = CurNodeObj.m_PreObj

        if self.m_HeadNodeObj == CurNodeObj:
            self.m_HeadNodeObj = CurNodeObj.m_NextObj

        return KeyObj

    def GetMd5QueueList(self):
        listRet = []
        CurObj = self.m_HeadNodeObj
        while CurObj is not None:
            listRet.append(CurObj.KeyObj)
            CurObj = CurObj.m_NextObj

        return listRet
