# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2020/11/24 8:53

# desc:
import os
import json
import main_frame.cmd_base as cmd_base


class CmdMulLanSnippets(cmd_base.CmdBase):
    def __init__(self):
        self.m_AppObj = None

    @staticmethod
    def GetName():
        return "mul_lan_snippets"

    def Do(self):
        """执行命令"""
        self.m_AppObj.Info("Start MulLanSnippets")

        # 初始化目录
        szCWD = self.m_AppObj.ConfigLoader.CWD
        szOutputDir = self.m_AppObj.CLM.GetArg(1)

        szOutputFullDir = szCWD + "/" + szOutputDir
        if not os.path.exists(szOutputFullDir):
            os.makedirs(szOutputFullDir)

        # 解析语言列表
        # Key0 = 'ID'
        # Key1 = 'name'
        # Key2 = 'desc'
        # Key3 = 'prefix'
        import config.setting.mul_lan as mul_lan
        dictNotLanKey = {mul_lan.Key0: True, mul_lan.Key1: True, mul_lan.Key2: True, mul_lan.Key3: True}
        listLanName = self.ParseLanNameList(mul_lan.mul_lan, dictNotLanKey)

        # 遍历语言名字列表，生成对应的snippet
        for szLanName in listLanName:
            SnippetFileConverterObj = SnippetFileConverter(szLanName, mul_lan.mul_lan)
            SnippetFileConverterObj.ConvertSnippetDict()
            SnippetFileConverterObj.SaveSnippet(szOutputFullDir)

    @staticmethod
    def ParseLanNameList(dictMulLan, dictNotLanKey):
        if len(dictMulLan) == 0:
            return []

        for nID, dictValue in dictMulLan.items():
            listLan = []
            for szKey, _ in dictValue.items():
                if szKey not in dictNotLanKey:
                    listLan.append(szKey)

            return listLan


class SnippetFileConverter:
    def __init__(self, szLanName, dictMulLan):
        self.m_szLanName = szLanName
        self.m_dictMulLan = dictMulLan
        self.m_dictName2Snippet = {}

    def ConvertSnippetDict(self):
        for nID, dictValue in self.m_dictMulLan.items():
            szName = dictValue["name"]
            szDesc = dictValue["desc"]
            szPrefix = dictValue["prefix"]
            szBody = dictValue[self.m_szLanName]

            SnippetNodeObj = SnippetNode(szName, szDesc, szPrefix, szBody)
            szSnippetName, dictSnippet = SnippetNodeObj.Convert()

            self.m_dictName2Snippet[szSnippetName] = dictSnippet

    def SaveSnippet(self, szDir):
        szSnippetPath = "{}/{}.json".format(szDir, self.m_szLanName)
        # 编码问题请参考: https://www.cnblogs.com/mingjiatang/p/9527345.html
        with open(szSnippetPath, "w", encoding="utf-8") as fp:
            json.dump(self.m_dictName2Snippet, fp, indent=4, sort_keys=True, ensure_ascii=False)


class SnippetNode:
    def __init__(self, szName, szDesc, szPrefix, szBody):
        self.m_szName = szName
        self.m_szDesc = szDesc
        self.m_szPrefix = szPrefix
        self.m_szBody = szBody

        self.m_dictSnippet = None

    def Convert(self):
        self.m_dictSnippet = {
            "prefix": self.m_szPrefix,
            "description": self.m_szDesc
        }

        listBody = []
        listLine = self.m_szBody.split("\n")

        for szLine in listLine:
            szLine = self._HandleBodyLine(szLine)
            listBody.append(szLine)

        self.m_dictSnippet["body"] = listBody

        return self.m_szName, self.m_dictSnippet

    @staticmethod
    def _HandleBodyLine(szLine):
        szLine = szLine.replace("\r", "\n")
        return szLine

