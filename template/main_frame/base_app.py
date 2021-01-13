# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 3/22/2020 11:17 AM

# desc:
import os
import re
import importlib
import os
import logging
import logging.config
import common.notify.mail_mgr as mail_mgr
import common.scheduler.scheduler_mgr as scheduler_mgr
import common.notify.ding_ding_mgr as ding_ding_mgr
import common.my_log as my_log


class BaseApp:
    def __init__(self):
        self.m_LoggerObj = my_log.MyLog(__file__)
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
        self.m_LoggerObj.info("Do init")

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

        self.m_LoggerObj.info("Do init end\n")

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
        self.m_LoggerObj.debug("\n\n\n\n")
        # noinspection SpellCheckingInspection
        ps.strip_dirs().sort_stats("cumtime").print_stats(10, 1.0, ".*")

    # ############################# help function
    @staticmethod
    def _GetBaseCommandOpt():
        return "hc:p:mstd", ["help", "config=", "cProfile=", "mail", "scheduler", "test", "dingding"]

    def _GetCommandName(self):
        return self.m_CLMObj.GetArg(0)

    def _SetTestFlag(self):
        self.m_LoggerObj.info("Start set test flag")
        self.m_bTest = self.m_CLMObj.HasOpt("-t", "--test")
        self.m_LoggerObj.info("End set test flag")

    def _LoadConfig(self):
        self.m_LoggerObj.info("Start load config file")

        ConfigLoaderCls = self.GetConfigLoaderCls()
        szConf = self.m_CLMObj.GetOpt("-c", "--config")
        szConfFullPath = ConfigLoaderCls.CheckConf(szConf)
        self.m_ConfigLoader = ConfigLoaderCls(szConfFullPath)
        self.m_ConfigLoader.ParseConf()

        self.m_LoggerObj.info("End load config file\n")

    def _DoHelp(self):
        bHelp = self.m_CLMObj.HasOpt("-h", "--help")
        self.m_LoggerObj.info("Help option:%s", bHelp)

        if not bHelp:
            return False

        self.m_LoggerObj.info("Help msg")
        with open(self.ConfigLoader.HelpPath, "r", encoding="utf-8") as fp:
            self.m_LoggerObj.info("\n\n%s\n\n", "".join(fp.readlines()))

        self.m_LoggerObj.info("Help msg end and exit(0)")

        return True

    def _InitMailMgr(self):
        if not self.m_CLMObj.HasOpt("-m", "--mail"):
            return

        self.m_LoggerObj.info("Start mail mgr")
        self.m_MailMgr = mail_mgr.MailMgr()
        self.m_MailMgr.SetDefaultConfig(self.ConfigLoader.MailHost, self.ConfigLoader.MailUser,
                                        self.ConfigLoader.MailPassword, self.ConfigLoader.MailTo)
        self.m_MailMgr.Send("启动小小服务", "你好，我是小小助手，我已经启动了，你可以直接找我哈")

        self.m_LoggerObj.info("End mail mgr\n")

    def _DestroyMailMgr(self):
        if self.m_MailMgr is not None:
            self.m_MailMgr.Destroy()

    def _InitDingDingMgr(self):
        if not self.m_CLMObj.HasOpt("-d", "--dingding"):
            return

        self.m_LoggerObj.info("Start dingding mgr")
        self.m_DingDingMgr = ding_ding_mgr.DingDingMgr(
            self.ConfigLoader.DingDingWebhook,
            self.ConfigLoader.DingDingSecret,
            self.ConfigLoader.DingDingKeyword,
            [self.ConfigLoader.DingDingTo]
        )

        self.m_DingDingMgr.Send(
            "你好，我是小小助手，我已经启动了，你可以直接找我哈"
        )

        self.m_LoggerObj.info("End dingding mgr\n")

    def _DestroyDingDingMgr(self):
        if self.m_DingDingMgr is not None:
            self.m_DingDingMgr.Destroy()

    def _InitSchedulerMgr(self):
        if not self.m_CLMObj.HasOpt("-s", "--scheduler"):
            return

        self.m_LoggerObj.info("Start scheduler mgr")
        assert self.m_MailMgr is not None, "scheduler mgr depend on mail mgr"

        self.m_SchedulerMgr = scheduler_mgr.SchedulerMgr()
        self.m_SchedulerMgr.SetMailMgr(self.m_MailMgr)
        if self.m_DingDingMgr is not None:
            self.m_SchedulerMgr.SetDingDingMgr(self.m_DingDingMgr)
        self.m_SchedulerMgr.Init()
        self.m_SchedulerMgr.Start()

        self.m_LoggerObj.info("End scheduler mgr\n")

    def _DestroySchedulerMgr(self):
        if self.m_SchedulerMgr is not None:
            self.m_SchedulerMgr.Destroy()

    def _GetCommand(self, szName):
        assert szName in self.m_dictCommand, "command not register:{0}".format(
            szName)
        return self.m_dictCommand[szName]

    def _ParseCommandArg(self, args):
        self.m_LoggerObj.info("Start parse command line")

        import common.command_line_arg_mgr as command_line_arg_mgr
        szBaseShortOpt, listBaseLongOpt = self._GetBaseCommandOpt()
        szShortOpt, listLongOpt = self.GetCommandOpt()
        self.m_CLMObj = command_line_arg_mgr.CommandLineArgMgr(szBaseShortOpt + szShortOpt,
                                                               listBaseLongOpt + listLongOpt)
        self.m_CLMObj.Parse(args)

        self.m_LoggerObj.info("End parse command line\n")

    def _RenderConfig(self):
        self.m_LoggerObj.info("Start rendering config")

        szRenderYmlPath = "config/render.yml"
        if not os.path.exists(szRenderYmlPath):
            self.m_LoggerObj.error(
                "copy config/render_template.yml to config/render.yml, then config it")
            raise FileNotFoundError(szRenderYmlPath)

        import common.util as util
        dictTemplatePath2TargetPath = {
            "config/config_template.conf": "config/config.conf"
        }

        util.RenderConfig("config/render.yml", dictTemplatePath2TargetPath)
        self.m_LoggerObj.info("End rendering config\n")

    def _AutoRegisterCommand(self, szFullPath, szRegPattern):
        listCommandClassObj = self._FilterCommandObj(szFullPath, szRegPattern)

        for CommandClassObj in listCommandClassObj:
            CommandObj = CommandClassObj()
            self._RegisterCommmand(CommandObj)

    @staticmethod
    def _FilterCommandObj(szCommandFullDir, szRegPattern):
        assert os.path.exists(szCommandFullDir), "目录不存在:" + szCommandFullDir
        import main_frame.cmd_base as cmd_base

        listCommandObj = []

        szCwd = os.getcwd()
        for szParentPath, listDirName, listFileName in os.walk(szCommandFullDir):
            for szFileName in listFileName:
                szFullPath = os.path.join(szParentPath, szFileName)

                if not re.match(szRegPattern, szFileName):
                    continue

                szRelPath = os.path.relpath(szFullPath, szCwd)
                szRelPathNoExt = os.path.splitext(szRelPath)[0]
                szModuleName = szRelPathNoExt.replace("\\", "/").replace("/", ".")

                ModuleObj = importlib.import_module(szModuleName)

                for szAttr in dir(ModuleObj):
                    CommandClassObj = getattr(ModuleObj, szAttr)
                    if isinstance(CommandClassObj, type) and issubclass(CommandClassObj, cmd_base.CmdBase):
                        listCommandObj.append(CommandClassObj)

        return listCommandObj

    def _RegisterAllCommand(self):
        self._AutoRegisterCommand(os.path.join(os.getcwd(), "main_frame/command"), r"^cmd[_a-zA-Z0-9]*.py$")

    def _RegisterCommmand(self, CommandObj):
        szName = CommandObj.GetName()
        assert szName not in self.m_dictCommand
        self.m_dictCommand[szName] = CommandObj

    def _UnRegisterCommand(self, szName):
        if szName in self.m_dictCommand:
            del self.m_dictCommand[szName]
