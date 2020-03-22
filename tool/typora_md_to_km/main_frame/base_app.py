# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 3/22/2020 11:17 AM

# desc:
import logging
import logging.config
import os
import sys
import time


class BaseApp:
    def __init__(self):
        self.m_ConfigLoader = None
        self.m_CLMObj = None
        self.m_ProfileObj = None

    def DoInit(self, args):
        # 生成render配置文件
        import common.util as util
        dictTemplatePath2TargetPath = {
            "conf/conf.conf": "conf/conf.conf"
        }
        util.RenderConfig("conf/render_template.yml", dictTemplatePath2TargetPath)

        # command line
        import common.command_line_arg_mgr as command_line_arg_mgr
        szShortOpt, listLongOpt = self.GetCommandOpt()
        self.m_CLMObj = command_line_arg_mgr.CommandLineArgMgr(szShortOpt, listLongOpt)
        self.m_CLMObj.Parse(args)
        szConf = self.m_CLMObj.GetOpt("-c", "-config")

        # 加载配置表
        ConfigLoaderCls = self.GetConfigLoaderCls()
        szConfFullPath = ConfigLoaderCls.CheckConf(szConf)
        self.m_ConfigLoader = ConfigLoaderCls(szConfFullPath)
        self.m_ConfigLoader.ParseConf()

        self.OnInit()

    def DoLogic(self):
        szProfileName = self.m_CLMObj.GetOpt("-p", "--cProfile")
        if szProfileName is not None:
            self.BeginProfile()

        self.OnLogic()

        if szProfileName is not None:
            self.EndProfile(szProfileName)

    def BeginProfile(self):
        import cProfile
        self.m_ProfileObj = cProfile.Profile()
        self.m_ProfileObj.enable()

    def EndProfile(self, szProfileName):
        import pstats
        self.m_ProfileObj.disable()
        # Sort stat by internal time.
        sortby = "tottime"
        ps = pstats.Stats(self.m_ProfileObj).sort_stats(sortby)
        ps.dump_stats(szProfileName)
        ps.strip_dirs().sort_stats("cumtime").print_stats(10, 1.0, ".*")

    def OnLogic(self):
        pass

    @staticmethod
    def GetCommandOpt():
        return "hc:p:", ["help", "config=", "cProfile="]

    @staticmethod
    def GetConfigLoaderCls():
        import main_frame.config_loader as config_loader
        return config_loader.ConfigLoader

    def GetConfigLoader(self):
        return self.m_ConfigLoader

    def OnInit(self):
        pass
