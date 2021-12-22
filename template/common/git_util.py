# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2018/11/23 12:15:10

# desc: git的工具库

import os
import subprocess


class GitUtil(object):
    def __init__(self):
        pass

    @staticmethod
    def Up(szFullPath):
        print("GitUtil.Up:" + szFullPath)
        szCurPath = os.getcwd()
        os.chdir(szFullPath)

        szCmd = "git pull"
        processObj = subprocess.Popen(szCmd, shell=True)
        (stdoutdata, stderrdata) = processObj.communicate()

        os.chdir(szCurPath)
        return processObj.returncode == 0

    @staticmethod
    def GetVersion(szFullPath):
        print(szFullPath)
        szCurPath = os.getcwd()
        os.chdir(szFullPath)

        szVersion = str(subprocess.check_output(["git", "log", "-n", "1", "--pretty=format:\"%H\""]))[3:11]

        os.chdir(szCurPath)
        return szVersion

    @staticmethod
    def Clean(szFullPath):
        print("GiUtil.Clean:" + szFullPath)

        szCurPath = os.getcwd()
        os.chdir(szFullPath)

        szCmd = "git checkout . && git clean -df"
        processObj = subprocess.Popen(szCmd, shell=True)
        (stdoutdata, stderrdata) = processObj.communicate()

        os.chdir(szCurPath)
        return processObj.returncode == 0

    @staticmethod
    def GetChangeFiles(szFullPath):
        print("GiUtil.GetChangeFiles:" + szFullPath)

        szCurPath = os.getcwd()
        os.chdir(szFullPath)

        szCmd = "git status . -s -u"
        processObj = subprocess.Popen(szCmd, shell=True)
        (stdoutdata, stderrdata) = processObj.communicate()

        szChangeFiles = str(subprocess.check_output(["git", "status", ".", "-s", "-u"]), "utf-8")
        os.chdir(szCurPath)

        listChangeFile = szChangeFiles.split('\n')

        return listChangeFile
