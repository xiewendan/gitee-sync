# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 3/22/2020 3:26 PM

# desc:

import re
import logging
import main_frame.base_app as base_app

READ_FILE_NUM = 100000  # 100k

def SharpReplace(szLine):
    if szLine.startswith("#"):
        szLine = "#" + szLine

    return szLine


def WordReplace(szLine):
    if szLine.startswith("["):
        return szLine

    dictOld2New = {
        "ios": "iOS",
        "android": "Android",
        "unity": "Unity",
        "windows": "Windows",
        "topython": "ToPython",
        "c#": "C#",
        "python": "Python",
        "github": "GitHub",
        "c++": "C++",
        "tolua": "ToLua",
        "android studio": "Android Studio",
        "Android studio": "Android Studio",
        "[[": "[",
        "][]]": "]",
    }
    for szOld, szNew in dictOld2New.items():
        szLine = szLine.replace(szOld, szNew)

    dictErrorReplace = {
        r"ToPython::GetUserObjectSubtype": r"topython::GetUserObjectSubtype",
        r"ToPython::PyUserObject": r"topython::PyUserObject",
        r"build\Android\cmake_build_Android.bat": r"build\android\cmake_build_android.bat",
        r"build\Android": r"build\android",
        r"ToPython.dll": r"topython.dll",
        r"ToPython.xcodeproj": r"topython.xcodeproj",
        r"ToPython.cpp": r"topython.cpp",

    }

    for szOld, szNew in dictErrorReplace.items():
        szLine = szLine.replace(szOld, szNew)

    return szLine


def RefProcess(szLine):
    MatchObj = re.match("^\[([0-9]+)\]: ([0-9a-zA-Z=#:\?\-\./]*) \"(.*)\"$", szLine)
    if MatchObj is None:
        return szLine

    szRef = "* [{0}] [{1}]({2})\n".format(MatchObj.group(1), MatchObj.group(3), MatchObj.group(2))
    return szRef


def LineProcess(szLine):
    szLine = SharpReplace(szLine)
    szLine = WordReplace(szLine)
    szLine = RefProcess(szLine)
    return szLine


def GetAppCls():
    return MainApp


class MainApp(base_app.BaseApp):
    @staticmethod
    def GetConfigLoaderCls():
        import logic.my_config_loader as my_config_loader
        return my_config_loader.MyConfigLoader

    def OnLogic(self):
        # todo
        szMDPath = self.m_CLMObj.GetArg(0)
        if szMDPath is None:
            szMDPath = input("\n请输入markdown文件路径:")
        szKMPath = szMDPath.replace(".md", "_km.md")

        with open(szMDPath, "r", encoding="utf-8") as fpMD:
            with open(szKMPath, "w", encoding="utf-8") as fpKM:
                listLine = fpMD.readlines(READ_FILE_NUM)
                while listLine:
                    for nIndex, szLine in enumerate(listLine):
                        listLine[nIndex] = LineProcess(szLine)

                    fpKM.writelines(listLine)
                    listLine = fpMD.readlines(READ_FILE_NUM)

        print("\n输出markdown文件路径:" + szKMPath + "\n")
        logging.getLogger("myLog").debug("输出markdown文件路径:" + szKMPath)
