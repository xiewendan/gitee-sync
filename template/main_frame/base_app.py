# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 3/22/2020 11:17 AM
# desc:

import importlib
import os
import re

import common.my_log as my_log


class BaseApp:
    def __init__(self):
        self.m_LoggerObj = my_log.MyLog(__file__)
        self.m_CLMObj = None
        self.m_bTest = False
        self.m_ConfigLoader = None
        self.m_ProfileObj = None
        self.m_CurCommandObj = None
        self.m_dictCommand = {}
        self.m_dictService = {}
        self.m_dictServiceOpt2Name = {}

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

        # 注册
        self._RegisterAll()

        # 初始化服务
        self._InitAllService()

        # 初始化
        self.OnInit()

        self.m_LoggerObj.info("Do init end\n")

    def DoLogic(self):
        self._BeginProfile()

        szCmdName = self._GetCommandName()
        if szCmdName is not None:
            CommandObj = self._GetCommand(szCmdName)
            CommandObj.Init(self)
            self.m_CurCommandObj = CommandObj
            CommandObj.Do()
        else:
            if self._DoHelp():
                pass
            else:
                self.OnLogic()

        self._EndProfile()

    def Destroy(self):
        self._DestroyAllService()

        self._UnRegisterAllService()

    @property
    def CLM(self):
        return self.m_CLMObj

    @property
    def ConfigLoader(self):
        return self.m_ConfigLoader

    # public function
    def IsTest(self):
        return self.m_bTest

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

    def _RegisterAll(self):
        # 注册命令
        self._AutoRegisterCommand(
            os.path.join(os.getcwd(), "main_frame/command"),
            r"^cmd[_a-zA-Z0-9]*.py$")

        # 注册服务
        self._AutoRegisterService(
            os.path.join(self.ConfigLoader.CWD, "main_frame/service"),
            r"^[a-zA-Z0-9_]*service.py$")

    # ********************************************************************************
    # service
    # ********************************************************************************
    def GetService(self, szName):
        assert szName in self.m_dictService
        return self.m_dictService[szName]

    def _AutoRegisterService(self, szFullPath, szRegPattern):
        self.m_LoggerObj.debug("full path:%s, regpattern:%s", szFullPath, szRegPattern)

        import main_frame.service_base as service_base
        listServiceClassObj = self._FilterClassObj(szFullPath, szRegPattern, service_base.ServiceBase)

        for ServiceClassObj in listServiceClassObj:
            ServiceObj = ServiceClassObj()
            self._RegisterService(ServiceObj)

    def _UnRegisterAllService(self):
        self.m_LoggerObj.debug("")
        listServiceName = list(self.m_dictService.keys())
        for szServiceName in listServiceName:
            self._UnRegisterService(szServiceName)

    def _RegisterService(self, ServiceObj):
        self.m_LoggerObj.debug("service name:%s, service obj:%s", ServiceObj.GetName(), str(ServiceObj))

        szName = ServiceObj.GetName()
        assert szName not in self.m_dictService, "重复 service name:%s" % szName
        self.m_dictService[szName] = ServiceObj

        listOpt = ServiceObj.GetOptList()
        for szOpt in listOpt:
            assert szOpt not in self.m_dictServiceOpt2Name, "重复opt name:%s" % szOpt
            self.m_dictServiceOpt2Name[szOpt] = szName

    def _UnRegisterService(self, szName):
        if szName in self.m_dictService:
            self.m_LoggerObj.debug("service del, service name:%s", szName)

            ServiceObj = self.m_dictService[szName]
            listOpt = ServiceObj.GetOptList()
            for szOpt in listOpt:
                assert szOpt in self.m_dictServiceOpt2Name
                del self.m_dictServiceOpt2Name[szOpt]

            del self.m_dictService[szName]

        else:
            self.m_LoggerObj.error("service not found, service name:%s", szName)

    def _InitAllService(self):
        self.m_LoggerObj.debug("_InitAllService")

        dictOption = self.CLM.GetOptionDict()
        for szKey, szValue in dictOption.items():
            if szKey in self.m_dictServiceOpt2Name:
                szServiceName = self.m_dictServiceOpt2Name[szKey]
                self.GetService(szServiceName).Init(self, [])

    def _DestroyAllService(self):
        for szName, ServiceObj in self.m_dictService.items():
            ServiceObj.Destroy()

    # ********************************************************************************
    # command
    # ********************************************************************************
    def GetCurCommand(self):
        return self.m_CurCommandObj

    def _GetCommand(self, szName):
        assert szName in self.m_dictCommand, "command not register:{0}".format(
            szName)
        return self.m_dictCommand[szName]

    def _AutoRegisterCommand(self, szFullPath, szRegPattern):
        self.m_LoggerObj.debug("full path:%s, reg pattern:%s", szFullPath, szRegPattern)

        import main_frame.cmd_base as cmd_base
        listCommandClassObj = self._FilterClassObj(szFullPath, szRegPattern, cmd_base.CmdBase)

        for CommandClassObj in listCommandClassObj:
            CommandObj = CommandClassObj()
            self._RegisterCommmand(CommandObj)

    def _RegisterCommmand(self, CommandObj):
        self.m_LoggerObj.debug("command name:%s, command obj:%s", CommandObj.GetName(), str(CommandObj))

        szName = CommandObj.GetName()
        assert szName not in self.m_dictCommand
        self.m_dictCommand[szName] = CommandObj

    def _UnRegisterCommand(self, szName):
        if szName in self.m_dictCommand:
            self.m_LoggerObj.debug("command del, command name:%s", szName)
            del self.m_dictCommand[szName]
        else:
            self.m_LoggerObj.error("command not found, command name:%s", szName)

    def _FilterClassObj(self, szClassFullDir, szRegPattern, BaseClass):
        self.m_LoggerObj.debug("dir:%s, reg pattern:%s, base class:%s", szClassFullDir, szRegPattern, str(BaseClass))

        assert os.path.exists(szClassFullDir), "目录不存在:" + szClassFullDir

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
