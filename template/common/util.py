# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2018/11/25 16:40:28

# desc: 常用函数

import logging
import os
import shutil
import subprocess
import sys

import yaml
from jinja2 import Template

import common.my_path as my_path
from common.my_exception import MyException


def RunCmd(szCmd, szOutputFile=None, bStdout=False):
    logging.getLogger("myLog").debug("%s,%s,%s", szCmd, szOutputFile, bStdout)

    if szOutputFile is None:
        szOutputFile = open(os.devnull, 'w')
    if bStdout:
        szOutputFile = sys.stdout
    p = subprocess.Popen(
        szCmd, shell=True, stdout=szOutputFile, stderr=szOutputFile)

    return p.wait()


def AssertRunCmd(szCmd, szOutputFile=None):
    logging.getLogger("myLog").debug("%s,%s", szCmd, szOutputFile)

    nRet = RunCmd(szCmd, szOutputFile)
    if nRet != 0:
        raise MyException("Run cmd error=%s" % szCmd)

    return True


def RemoveFileDir(szPath):
    if not os.path.exists(szPath):
        return
    if os.path.isfile(szPath):
        os.remove(szPath)
    else:
        shutil.rmtree(szPath)


def RenderConfig(szConfigPath, dictTemplatePath2TargetPath):
    assert os.path.exists(szConfigPath) and os.path.isfile(szConfigPath), "render_template文件不存在" + szConfigPath

    # 转换所有的配置文件，多层key合并为一个key，并用'_'连接
    # 比如 a["BOY"]["NAME"]="xjc" ==> a["BOY_NAME"]="xjc"
    def LoadConfig(szFilePath):
        logging.getLogger("myLog").debug("yaml file path:" + szFilePath)

        with open(szFilePath, 'r') as fp:
            dictConfigYaml = yaml.full_load(fp)
            if dictConfigYaml is None:
                return {}

            def RecursiveSetDict(dictConfigTemp, szPrefix, dictOutputConfigTemp):
                for szKey, szValue in dictConfigTemp.items():
                    if isinstance(szValue, dict):
                        RecursiveSetDict(szValue, szPrefix + szKey + "_", dictOutputConfigTemp)
                    else:
                        dictOutputConfigTemp[szPrefix + szKey] = szValue

            dictOutputConfig = {}

            RecursiveSetDict(dictConfigYaml, "", dictOutputConfig)

            dictOutputConfig["CWD"] = os.path.abspath(dictOutputConfig["CWD"]).replace("\\", "/")

            return dictOutputConfig

    def RenderSingleConfig(szTemplatePath1, szTargetPath1, dictConfig1):
        assert os.path.exists(szTemplatePath1) and os.path.isfile(szTemplatePath1), "template文件不存在" + szTemplatePath1

        my_path.CreateFileDir(szTargetPath1)

        with open(szTemplatePath1, "r") as fpTemplate:
            templateObj = Template(fpTemplate.read())
            szContent = templateObj.render(dictConfig1)

            with open(szTargetPath1, "w") as fpTarget:
                fpTarget.write(szContent)

    dictConfig = LoadConfig(szConfigPath)
    for szTemplatePath, szTargetPath in dictTemplatePath2TargetPath.items():
        RenderSingleConfig(szTemplatePath, szTargetPath, dictConfig)


def FilterClassObj(szClassFullDir, szRegPattern, BaseClass):
    assert os.path.exists(szClassFullDir), "目录不存在:" + szClassFullDir

    import re
    import importlib

    listClassObj = []

    szCwd = os.getcwd()
    for szParentPath, listDirName, listFileName in os.walk(szClassFullDir):
        for szFileName in listFileName:
            szFullPath = os.path.join(szParentPath, szFileName)

            if not re.match(szRegPattern, szFileName):
                continue

            szRelPath = os.path.relpath(szFullPath, szCwd)
            szRelPathNoExt = os.path.splitext(szRelPath)[0]
            szModuleName = szRelPathNoExt.replace("\\", "/").replace("/", ".")

            ModuleObj = importlib.import_module(szModuleName)

            for szAttr in dir(ModuleObj):
                ClassObj = getattr(ModuleObj, szAttr)
                if isinstance(ClassObj, type) and issubclass(ClassObj, BaseClass):
                    listClassObj.append(ClassObj)

    return listClassObj
