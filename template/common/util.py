# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2018/11/25 16:40:28

# desc: 常用函数

import os
import sys
import subprocess
import logging
import shutil
from jinja2 import Template
import yaml

from common.my_exception import MyException
import common.my_path as my_path


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
        assert (os.path.exists(szTemplatePath1) and os.path.isfile(szTemplatePath1), "template文件不存在" + szTemplatePath1)

        my_path.CreateFileDir(szTargetPath1)

        with open(szTemplatePath1, "r") as fpTemplate:
            templateObj = Template(fpTemplate.read())
            szContent = templateObj.render(dictConfig1)

            with open(szTargetPath1, "w") as fpTarget:
                fpTarget.write(szContent)

    dictConfig = LoadConfig(szConfigPath)
    for szTemplatePath, szTargetPath in dictTemplatePath2TargetPath.items():
        RenderSingleConfig(szTemplatePath, szTargetPath, dictConfig)
