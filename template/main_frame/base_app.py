# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 3/22/2020 11:17 AM

# desc:
import os
import logging
import logging.config
import common.mail_mgr as mail_mgr
import common.scheduler.scheduler_mgr as scheduler_mgr


class BaseApp:
    def __init__(self):
        self.m_LoggerObj = logging.getLogger("myLog")
        self.m_ConfigLoader = None
        self.m_CLMObj = None
        self.m_ProfileObj = None
        self.m_MailMgr = None
        self.m_SchedulerMgr = None

    # ############################# main process
    def DoInit(self, args):
        self.Info("Do init")

        # 生成render配置文件
        self.RenderConfig()

        # command line
        self.ParseCommandArg(args)

        # 加载配置表
        self.LoadConfig()

        # 邮件系统初始化
        self.InitMailMgr()

        # 定时器
        self.InitSchedulerMgr()

        # 初始化
        self.OnInit()

        self.Info("Do init end\n")

    def LoadConfig(self):
        self.Info("Start load config file")

        ConfigLoaderCls = self.GetConfigLoaderCls()
        szConf = self.m_CLMObj.GetOpt("-c", "--config")
        szConfFullPath = ConfigLoaderCls.CheckConf(szConf)
        self.m_ConfigLoader = ConfigLoaderCls(szConfFullPath)
        self.m_ConfigLoader.ParseConf()

        self.Info("End load config file\n")

    def InitMailMgr(self):
        if not self.m_CLMObj.HasOpt("-m", "--mail"):
            return

        self.Info("Start mail mgr")
        self.m_MailMgr = mail_mgr.MailMgr()
        self.m_MailMgr.Login(self.m_ConfigLoader.MailHost, self.m_ConfigLoader.MailUser,
                             self.m_ConfigLoader.MailPassword)

        self.Info("End mail mgr\n")

    def DestroyMailMgr(self):
        if self.m_MailMgr is not None:
            self.m_MailMgr.Destroy()

    def InitSchedulerMgr(self):
        if not self.m_CLMObj.HasOpt("-s", "--scheduler"):
            return
        self.Info("Start scheduler mgr")
        self.m_SchedulerMgr = scheduler_mgr.SchedulerMgr()
        assert self.m_MailMgr is not None, "scheduler mgr depend on mail mgr"
        self.m_SchedulerMgr.SetMailMgr(self.m_MailMgr)
        self.m_SchedulerMgr.Start()
        self.Info("End scheduler mgr\n")

    def DestroySchedulerMgr(self):
        if self.m_SchedulerMgr is not None:
            self.m_SchedulerMgr.Destroy()

    def GetSchedulerMgr(self):
        assert self.m_SchedulerMgr is not None, "未初始化"
        return self.m_SchedulerMgr

    def SendMail(self, szFrom, listTo, szTitle, szMsg):
        self.m_MailMgr.Send(szFrom, listTo, szTitle, szMsg)

    def ParseCommandArg(self, args):
        self.Info("Start parse command line")

        import common.command_line_arg_mgr as command_line_arg_mgr
        szBaseShortOpt, listBaseLongOpt = self.GetBaseCommandOpt()
        szShortOpt, listLongOpt = self.GetCommandOpt()
        self.m_CLMObj = command_line_arg_mgr.CommandLineArgMgr(szBaseShortOpt + szShortOpt,
                                                               listBaseLongOpt + listLongOpt)
        self.m_CLMObj.Parse(args)

        self.Info("End parse command line\n")

    def RenderConfig(self):
        self.Info("Start rendering config")

        szRenderYmlPath = "conf/render.yml"
        if not os.path.exists(szRenderYmlPath):
            self.Error("copy conf/render_template.yml to conf/render.yml, then config it")
            raise FileNotFoundError(szRenderYmlPath)

        import common.util as util
        dictTemplatePath2TargetPath = {
            "conf/conf_template.conf": "conf/conf.conf"
        }

        util.RenderConfig("conf/render.yml", dictTemplatePath2TargetPath)
        self.Info("End rendering config\n")

    def DoLogic(self):
        self.BeginProfile()

        self.OnLogic()

        self.EndProfile()

    def Destroy(self):
        self.DestroyMailMgr()
        self.DestroySchedulerMgr()
        pass

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
        self.Debug("\n\n\n\n")
        # noinspection SpellCheckingInspection
        ps.strip_dirs().sort_stats("cumtime").print_stats(10, 1.0, ".*")

    def GetConfigLoader(self):
        return self.m_ConfigLoader

    # ############################# log
    def Debug(self, szMsg, *listArgs, **dictArgs):
        self.m_LoggerObj.debug(szMsg, *listArgs, **dictArgs)

    def Info(self, szMsg, *listArgs, **dictArgs):
        self.m_LoggerObj.info(szMsg, *listArgs, **dictArgs)

    def Warning(self, szMsg, *listArgs, **dictArgs):
        self.m_LoggerObj.warning(szMsg, *listArgs, **dictArgs)

    def Error(self, szMsg, *listArgs, **dictArgs):
        self.m_LoggerObj.error(szMsg, *listArgs, **dictArgs)

    @staticmethod
    def GetBaseCommandOpt():
        return "hc:p:ms", ["help", "config=", "cProfile=", "mail", "scheduler"]

    # ############################# override function
    @staticmethod
    def GetConfigLoaderCls():
        import main_frame.config_loader as config_loader
        return config_loader.ConfigLoader

    def OnLogic(self):
        pass

    def OnInit(self):
        pass

    @staticmethod
    def GetCommandOpt():
        return "", []
