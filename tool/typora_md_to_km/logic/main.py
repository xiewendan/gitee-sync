# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2019/4/25 11:22

# desc: 主函数入口

import re
import shutil
import sys
import logging
import common.util as util
import common.command_line_arg_mgr as command_line_arg_mgr

READ_FILE_NUM = 100000  # 100k

RefPattern = re.compile("^\[([0-9]+)\]: ([0-9a-zA-Z=#:\?\-\./]*) \"(.*)\"$")


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
    MatchObj = RefPattern.match(szLine)
    if MatchObj is None:
        return szLine

    szRef = "* [{0}] [{1}]({2})\n".format(MatchObj.group(1), MatchObj.group(3), MatchObj.group(2))
    return szRef


def LineProcess(szLine):
    szLine = SharpReplace(szLine)
    szLine = WordReplace(szLine)
    szLine = RefProcess(szLine)
    return szLine


def Main(args):
    logging.getLogger("myLog").debug("main start")

    # command line
    commandLineArgMgr = command_line_arg_mgr.CommandLineArgMgr("hc:", ["help", "config="])
    commandLineArgMgr.Parse(args)
    szConf = commandLineArgMgr.GetOpt("-c", "-config")

    # 加载配置表
    import logic.my_config_loader as my_config_loader
    szConfFullPath = my_config_loader.MyConfigLoader.CheckConf(szConf)
    configLoader = my_config_loader.MyConfigLoader(szConfFullPath)
    configLoader.ParseConf()

    # todo
    szMDPath = commandLineArgMgr.GetArg(0)
    if szMDPath is None:
        szMDPath = input("请输入markdown文件路径:")
    szKMPath = szMDPath.replace(".md", "_km.md")

    with open(szMDPath, "r", encoding="utf-8") as fpMD:
        with open(szKMPath, "w", encoding="utf-8") as fpKM:
            listLine = fpMD.readlines(READ_FILE_NUM)
            while listLine:
                for nIndex, szLine in enumerate(listLine):
                    listLine[nIndex] = LineProcess(szLine)

                fpKM.writelines(listLine)
                listLine = fpMD.readlines(READ_FILE_NUM)

    logging.getLogger("myLog").info("输出markdown文件路径:" + szKMPath)

    logging.getLogger("myLog").debug("finished")
