import pymongo


class MongoMgr:
    def __init__(self, dictConfig=None):
        if dictConfig is None:
            self.m_szIp = "localhost"
            self.m_nPort = 27017
        
        else:
            self.m_szIp = dictConfig["ip"]
            self.m_nPort = dictConfig["port"]

        self.m_DbObj = None

    def Connect(self):
        szURI = "mongodb://{0}:{1}/".format(self.m_szIp, self.m_nPort)
        self.m_DbObj = pymongo.MongoClient(szURI)

    def InsertUpdate(self, szCol, dictKey, dictData):
        self.m_DbObj[szCol].update_one(dictKey, dictData, upsert=True)

    def Find(self, szCol):
        return self.m_DbObj[szCol].find()

g_MongoMgr = MongoMgr()

Connect = g_MongoMgr.Connect
InsertUpdate = g_MongoMgr.InsertUpdate
Find = g_MongoMgr.Find
