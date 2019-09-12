# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2019/4/25 11:22

# desc: 主函数入口

import sys
import os
import json
import logging
import common.my_path as my_path

import os
from os.path import join, getsize


def getdirsize(dir):
    size = 0
    for root, dirs, files in os.walk(dir):
        size += sum([getsize(join(root, name)) for name in files])
    return size


def Main(args):
    dir = "E:\\project\\dm109\\dm109_py3_2019\\trunk"
    dictExt2Count = {}
    for root, dirs, files in os.walk(dir):
        for name in files:
            szPath = join(root, name)
            if not szPath.startswith("E:\\project\\dm109\\dm109_py3_2019\\trunk\\Client\\Unity\\WwiseProject\\.svn") and not szPath.startswith("E:\\project\\YY25\\YY25\\.git") and not szPath.startswith("E:\\project\\YY25\\YY25\\Client\\Unity\\Library"):
                nSize = getsize(szPath)
                if nSize > 1000000:
                    # print(szPath, nSize)
                    szExt = my_path.FileExt(szPath)
                    if len(szExt) > 0:
                        if szExt not in dictExt2Count:
                            dictExt2Count[szExt] = 0
                        dictExt2Count[szExt] += 1
                pass
        pass
    listSortedExt2Count = sorted(dictExt2Count.items(), key=lambda d: d[1], reverse=True)
    logging.getLogger("myLog").debug("Ext2Count:" + str(listSortedExt2Count))
    pass
    logging.getLogger("myLog").debug("main start")

    # 加载配置表
    import logic.my_config_loader as my_config_loader
    szConfFullPath = my_config_loader.MyConfigLoader.CheckConf(args)
    configLoader = my_config_loader.MyConfigLoader(szConfFullPath)
    configLoader.ParseConf()

    # 获得所有Ext的名字
    dictExt2Count = {}
    szWorkspaceDir = my_path.ParseDir(configLoader.VSCodeWorkspacePath)
    logging.getLogger("myLog").debug("workspace dir:" + str(szWorkspaceDir))
    for szDir, listSubDir, listFile in os.walk(szWorkspaceDir):
        for szFile in listFile:
            szExt = my_path.FileExt(szFile)
            if len(szExt) > 0:
                if szExt not in dictExt2Count:
                    dictExt2Count[szExt] = 0
                dictExt2Count[szExt] += 1

    listSortedExt2Count = sorted(dictExt2Count.items(), key=lambda d: d[1], reverse=True)
    logging.getLogger("myLog").debug("Ext2Count:" + str(listSortedExt2Count))

    # 过滤Ext
    szExtList = configLoader.ExtList
    listExt = szExtList.split(",")
    logging.getLogger("myLog").debug("ExtList:" + str(listExt))

    for szExt in listExt:
        if szExt in dictExt2Count:
            del dictExt2Count[szExt]

    # 计算Excludefile
    dictFileExclude = {}
    for szExt in dictExt2Count.keys():
        dictFileExclude["**/*" + szExt] = True
    logging.getLogger("myLog").debug("dictFileExclude by suffix:" + str(dictFileExclude))

    szExcludeList = configLoader.ExcludeList
    listExclude = szExcludeList.split(",")
    logging.getLogger("myLog").debug("listExclude from conf:" + str(listExclude))

    for szExclude in listExclude:
        dictFileExclude[szExclude] = True
    logging.getLogger("myLog").debug("dictFileExclude:" + str(dictFileExclude))

    # 加载workspace，并修改
    dictWorkspaceConf = None
    with open(configLoader.VSCodeWorkspacePath, "r") as fp:
        try:
            dictWorkspaceConf = json.load(fp)
        except Exception as e:
            raise e

    szStrSetting = "settings"
    szStrFileExclude = "files.exclude"
    if szStrSetting not in dictWorkspaceConf:
        dictWorkspaceConf[szStrSetting] = {}

    dictWorkspaceConf[szStrSetting][szStrFileExclude] = dictFileExclude

    with open(configLoader.VSCodeWorkspacePath, "w") as fp:
        json.dump(dictWorkspaceConf, fp, indent=4)

    # 结束记录log
    logging.getLogger("myLog").debug("finished")

