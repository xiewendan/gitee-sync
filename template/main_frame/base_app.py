# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 3/22/2020 11:17 AM

# desc:
import logging
import logging.config


class BaseApp:
    def __init__(self):
        self.m_ConfigLoader = None
        self.m_CLMObj = None
        self.m_ProfileObj = None

    # ############################# main process
    def DoInit(self, args):
        logging.getLogger("myLog").info("Do init")

        # 生成render配置文件
        self.RenderConfig()

        # command line
        self.ParseCommandArg(args)

        # 加载配置表
        self.LoadConfig()

        # 初始化
        self.OnInit()

        logging.getLogger("myLog").info("Do init end\n")

    def LoadConfig(self):
        logging.getLogger("myLog").info("Start load config file")

        ConfigLoaderCls = self.GetConfigLoaderCls()
        szConf = self.m_CLMObj.GetOpt("-c", "-config")
        szConfFullPath = ConfigLoaderCls.CheckConf(szConf)
        self.m_ConfigLoader = ConfigLoaderCls(szConfFullPath)
        self.m_ConfigLoader.ParseConf()

        logging.getLogger("myLog").info("End load config file\n")

    def ParseCommandArg(self, args):
        logging.getLogger("myLog").info("Start parse command line")

        import common.command_line_arg_mgr as command_line_arg_mgr
        szShortOpt, listLongOpt = self.GetCommandOpt()
        self.m_CLMObj = command_line_arg_mgr.CommandLineArgMgr(szShortOpt, listLongOpt)
        self.m_CLMObj.Parse(args)

        logging.getLogger("myLog").info("End parse command line\n")

    @staticmethod
    def RenderConfig():
        logging.getLogger("myLog").info("Start rendering config")
        import common.util as util
        dictTemplatePath2TargetPath = {
            "conf/conf.conf": "conf/conf.conf"
        }
        util.RenderConfig("conf/render_template.yml", dictTemplatePath2TargetPath)
        logging.getLogger("myLog").info("End rendering config\n")

    def DoLogic(self):
        self.BeginProfile()

        self.OnLogic()

        self.EndProfile()

    # ############################# profile
    def GetProfileName(self):
        return self.m_CLMObj.GetOpt("-p", "--cProfile")

    def BeginProfile(self):
        szProfileName = self.GetProfileName()
        if szProfileName is None:
            return

        import cProfile
        self.m_ProfileObj = cProfile.Profile()
        self.m_ProfileObj.enable()

    def EndProfile(self):
        szProfileName = self.GetProfileName()
        if szProfileName is None:
            return

        import pstats
        self.m_ProfileObj.disable()

        # Sort stat by internal time.
        # noinspection SpellCheckingInspection
        szSortBy = "tottime"
        ps = pstats.Stats(self.m_ProfileObj).sort_stats(szSortBy)
        ps.dump_stats(szProfileName)
        logging.getLogger("myLog").debug("\n\n\n\n")
        # noinspection SpellCheckingInspection
        ps.strip_dirs().sort_stats("cumtime").print_stats(10, 1.0, ".*")

    def GetConfigLoader(self):
        return self.m_ConfigLoader

    # ############################# override function
    @staticmethod
    def GetCommandOpt():
        return "hc:p:", ["help", "config=", "cProfile="]

    @staticmethod
    def GetConfigLoaderCls():
        import main_frame.config_loader as config_loader
        return config_loader.ConfigLoader

    def OnLogic(self):
        pass

    def OnInit(self):
        pass
