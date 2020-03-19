# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 3/19/2020 3:07 PM

# desc:
import getopt


class CommandLineArgMgr:
    # https://www.jianshu.com/p/0361cd8b8fec
    def __init__(self, szShortOpts, listLongOpts):
        self.m_szShortOpts = szShortOpts
        self.m_listLongOpts = listLongOpts
        self.m_dictOptions = {}
        self.m_listArgs = []
        self.m_nLenListArgs = 0

    def Parse(self, tupleArgs):
        listOptions, listArgs = getopt.getopt(tupleArgs[1:], self.m_szShortOpts, self.m_listLongOpts)
        for szKey, szValue in listOptions:
            self.m_dictOptions[szKey] = szValue
        self.m_listArgs = listArgs
        self.m_nLenListArgs = len(self.m_listArgs)

    def HasOpt(self, szOptName):
        return szOptName in self.m_dictOptions

    def GetOpt(self, *tupleArg):
        for szArg in tupleArg:
            if szArg in self.m_dictOptions:
                return self.m_dictOptions[szArg]

        return None

    def GetArgs(self, nIndex):
        if nIndex >= self.m_nLenListArgs:
            return None

        return self.m_listArgs[nIndex]
