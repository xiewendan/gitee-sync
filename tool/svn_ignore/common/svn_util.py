# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2018/11/23 12:15:10

# desc: svn的工具库

import subprocess
# import svn_clean
# import lib.svn_clean as svn_clean


import common.util as util

class SvnUtil(object):
    def __init__(self):
        pass

    @staticmethod
    def SvnUp(szFullPath):
        szCmd = "svn up --accept tf \"%s\"" % (szFullPath)

        util.AssertRunCmd(szCmd)

    @staticmethod
    def GetVersion(szFullPath):
        return subprocess.check_output(['svn', 'info', '--show-item', 'revision', szFullPath]).strip()

    @staticmethod
    def SvnClean(szFullPath):
        print("SvnUtil.SvnClean:", szFullPath)
        # svn_clean.svn_clean(szFullPath)

    @staticmethod
    def SvnCopy(szBranchSrc, szBranchDest, szMsg):
        szCmd = "svn copy {0} {1} -m \"{2}\"".format(szBranchSrc, szBranchDest, szMsg)

        util.AssertRunCmd(szCmd)

    @staticmethod
    def SvnSwitch(szBranchUrl, szSvnWorkingDir):
        szCmd = "svn switch {0} {1}".format(szBranchUrl, szSvnWorkingDir)

        util.AssertRunCmd(szCmd)

    @staticmethod
    def CreateExternal(szExternalVal1, szExternalVal2):
        szCmd = "svn propset svn:externals \"{0}\" {1}".format(szExternalVal1, szExternalVal2)

        util.AssertRunCmd(szCmd)

    @staticmethod
    def SvnCommit(szWorkingDir, szMsg):
        szCmd = "svn commit {0} -m \"{1}\"".format(szWorkingDir, szMsg)

        util.AssertRunCmd(szCmd)

    @staticmethod
    def CreateExternalByCfgFile(szWorkingDir, szCfgFile):
        szCmd = "svn propset svn:externals {0} -F {1}".format(szWorkingDir, szCfgFile)

        util.AssertRunCmd(szCmd)

    @staticmethod
    def SvnIgnoreByCfgFile(szPath, szSvnIgnore):
        szCmd = "svn propset svn:ignore -F {0} {1}".format(szSvnIgnore, szPath)

        util.AssertRunCmd(szCmd)
