# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 3/22/2020 11:17 AM

# desc:
import os
import logging
import logging.config
import common.notify.mail_mgr as mail_mgr
import common.scheduler.scheduler_mgr as scheduler_mgr
import common.notify.ding_ding_mgr as ding_ding_mgr


class BaseApp:
    def __init__(self):
        self.m_LoggerObj = logging.getLogger("myLog")
        self.m_CLMObj = None
        self.m_bTest = False
        self.m_ConfigLoader = None
        self.m_ProfileObj = None
        self.m_MailMgr = None
        self.m_DingDingMgr = None
        self.m_SchedulerMgr = None
        self.m_dictCommand = {}

    # ############################# main process
    def DoInit(self, args):
        self.Info("Do init")

        # 生成render配置文件
        self._RenderConfig()

        # command line
        self._ParseCommandArg(args)

        # test flag
        self._SetTestFlag()

        # 加载配置表
        self._LoadConfig()

        # 邮件系统初始化
        self._InitMailMgr()

        # 钉钉系统初始化
        self._InitDingDingMgr()

        # 定时器
        self._InitSchedulerMgr()

        # 注册所有的命令
        self._RegisterAllCommand()

        # 初始化
        self.OnInit()

        self.Info("Do init end\n")

    def DoLogic(self):
        self._BeginProfile()

        szCmdName = self._GetCommandName()
        if szCmdName is not None:
            CommandObj = self._GetCommand(szCmdName)
            CommandObj.Init(self)
            CommandObj.Do()
        else:
            if self._DoHelp():
                pass
            else:
                self.OnLogic()

        self._EndProfile()

    def Destroy(self):
        self._DestroyMailMgr()
        self._DestroySchedulerMgr()
        pass

    @property
    def CLM(self):
        return self.m_CLMObj

    @property
    def ConfigLoader(self):
        return self.m_ConfigLoader

    # public function
    def IsTest(self):
        return self.m_bTest

    def GetMailMgr(self):
        assert self.m_MailMgr is not None, "未初始化"
        return self.m_MailMgr

    def GetDingDingMgr(self):
        assert self.m_DingDingMgr is not None, "未初始化"
        return self.m_DingDingMgr

    def GetSchedulerMgr(self):
        assert self.m_SchedulerMgr is not None, "未初始化"
        return self.m_SchedulerMgr

    def SendMail(self, szTitle, szMsg, listTo=None):
        self.m_MailMgr.Send(szTitle, szMsg, listTo=listTo)
    
    def SendDingDing(self, szMsg, listTo=None):
        self.m_DingDingMgr.Send(szMsg, listTo)

    # ############################# log
    def Debug(self, szMsg, *listArgs, **dictArgs):
        self.m_LoggerObj.debug(szMsg, *listArgs, **dictArgs)

    def Info(self, szMsg, *listArgs, **dictArgs):
        self.m_LoggerObj.info(szMsg, *listArgs, **dictArgs)

    def Warning(self, szMsg, *listArgs, **dictArgs):
        self.m_LoggerObj.warning(szMsg, *listArgs, **dictArgs)

    def Error(self, szMsg, *listArgs, **dictArgs):
        self.m_LoggerObj.error(szMsg, *listArgs, **dictArgs)

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

    # ############################# profile
    def _GetProfileName(self):
        return self.m_CLMObj.GetOpt("-p", "--cProfile")

    def _BeginProfile(self):
        szProfileName = self._GetProfileName()
        if szProfileName is None:
            return

        import cProfile
        self.m_ProfileObj = cProfile.Profile()
        self.m_ProfileObj.enable()

    def _EndProfile(self):
        szProfileName = self._GetProfileName()
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

    # ############################# help function
    @staticmethod
    def _GetBaseCommandOpt():
        return "hc:p:mstd", ["help", "config=", "cProfile=", "mail", "scheduler", "test", "dingding"]

    def _GetCommandName(self):
        return self.m_CLMObj.GetArg(0)

    def _SetTestFlag(self):
        self.Info("Start set test flag")
        self.m_bTest = self.m_CLMObj.HasOpt("-t", "--test")
        self.Info("End set test flag")

    def _LoadConfig(self):
        self.Info("Start load config file")

        ConfigLoaderCls = self.GetConfigLoaderCls()
        szConf = self.m_CLMObj.GetOpt("-c", "--config")
        szConfFullPath = ConfigLoaderCls.CheckConf(szConf)
        self.m_ConfigLoader = ConfigLoaderCls(szConfFullPath)
        self.m_ConfigLoader.ParseConf()

        self.Info("End load config file\n")

    def _DoHelp(self):
        bHelp = self.m_CLMObj.HasOpt("-h", "--help")
        self.Info("Help option:%s", bHelp)

        if not bHelp:
            return False

        self.Info("Help msg")
        with open(self.ConfigLoader.HelpPath, "r", encoding="utf-8") as fp:
            self.Info("\n\n%s\n\n", "".join(fp.readlines()))

        self.Info("Help msg end and exit(0)")

        return True

    def _InitMailMgr(self):
        if not self.m_CLMObj.HasOpt("-m", "--mail"):
            return

        self.Info("Start mail mgr")
        self.m_MailMgr = mail_mgr.MailMgr()
        self.m_MailMgr.SetDefaultConfig(self.ConfigLoader.MailHost, self.ConfigLoader.MailUser,
                                        self.ConfigLoader.MailPassword, self.ConfigLoader.MailTo)
        self.m_MailMgr.Send("启动小小服务", "你好，我是小小助手，我已经启动了，你可以直接找我哈")

        self.Info("End mail mgr\n")

    def _DestroyMailMgr(self):
        if self.m_MailMgr is not None:
            self.m_MailMgr.Destroy()

    def _InitDingDingMgr(self):
        if not self.m_CLMObj.HasOpt("-d", "--dingding"):
            return

        self.Info("Start dingding mgr")
        self.m_DingDingMgr = ding_ding_mgr.DingDingMgr(
            self.ConfigLoader.DingDingWebhook,
            self.ConfigLoader.DingDingSecret,
            self.ConfigLoader.DingDingKeyword,
            [self.ConfigLoader.DingDingTo]
        )

        self.m_DingDingMgr.Send(
            "你好，我是小小助手，我已经启动了，你可以直接找我哈"
        )

        self.Info("End dingding mgr\n")

    def _DestroyDingDingMgr(self):
        if self.m_DingDingMgr is not None:
            self.m_DingDingMgr.Destroy()

    def _InitSchedulerMgr(self):
        if not self.m_CLMObj.HasOpt("-s", "--scheduler"):
            return

        self.Info("Start scheduler mgr")
        assert self.m_MailMgr is not None, "scheduler mgr depend on mail mgr"

        self.m_SchedulerMgr = scheduler_mgr.SchedulerMgr()
        self.m_SchedulerMgr.SetMailMgr(self.m_MailMgr)
        if self.m_DingDingMgr is not None:
            self.m_SchedulerMgr.SetDingDingMgr(self.m_DingDingMgr)
        self.m_SchedulerMgr.Init()
        self.m_SchedulerMgr.Start()

        self.Info("End scheduler mgr\n")

    def _DestroySchedulerMgr(self):
        if self.m_SchedulerMgr is not None:
            self.m_SchedulerMgr.Destroy()

    def _GetCommand(self, szName):
        assert szName in self.m_dictCommand, "command not register:{0}".format(
            szName)
        return self.m_dictCommand[szName]

    def _ParseCommandArg(self, args):
        self.Info("Start parse command line")

        import common.command_line_arg_mgr as command_line_arg_mgr
        szBaseShortOpt, listBaseLongOpt = self._GetBaseCommandOpt()
        szShortOpt, listLongOpt = self.GetCommandOpt()
        self.m_CLMObj = command_line_arg_mgr.CommandLineArgMgr(szBaseShortOpt + szShortOpt,
                                                               listBaseLongOpt + listLongOpt)
        self.m_CLMObj.Parse(args)

        self.Info("End parse command line\n")

    def _RenderConfig(self):
        self.Info("Start rendering config")

        szRenderYmlPath = "config/render.yml"
        if not os.path.exists(szRenderYmlPath):
            self.Error(
                "copy config/render_template.yml to config/render.yml, then config it")
            raise FileNotFoundError(szRenderYmlPath)

        import common.util as util
        dictTemplatePath2TargetPath = {
            "config/config_template.conf": "config/config.conf"
        }

        util.RenderConfig("config/render.yml", dictTemplatePath2TargetPath)
        self.Info("End rendering config\n")

    def _RegisterAllCommand(self):
        import main_frame.command.cmd_excel2py as cmd_excel2py
        Excel2PyCmdObj = cmd_excel2py.CmdExcel2Py()
        self._RegisterCommmand(Excel2PyCmdObj)
        import main_frame.command.cmd_merge_monthly_report as cmd_merge_monthly_report
        MergeMonthlyReportCmdObj = cmd_merge_monthly_report.CmdMergeMonthlyReport()
        self._RegisterCommmand(MergeMonthlyReportCmdObj)

        import main_frame.command.cmd_merge_monthly_report2 as cmd_merge_monthly_report2
        MergeMonthlyReport2CmdObj = cmd_merge_monthly_report2.CmdMergeMonthlyReport2()
        self._RegisterCommmand(MergeMonthlyReport2CmdObj)

    def _RegisterCommmand(self, CommandObj):
        szName = CommandObj.GetName()
        assert szName not in self.m_dictCommand
        self.m_dictCommand[szName] = CommandObj

    def _UnRegisterCommand(self, szName):
        if szName in self.m_dictCommand:
            del self.m_dictCommand[szName]
