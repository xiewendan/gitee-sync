# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2020/11/11 8:10

# desc:
# 所有命令类的基类
# 1、希望实现新的类型时，需要继承与CmdBase，然后，实现GetName，Init，Do等函数
# 2、在base_app.py中的_RegisterAllCommand函数，注册新类型
# 3、在启动中传入命令名和命令需要的参数

# 以配置表转表工具为例
# 1、新类型的代码：main_frame.command.cmd_excel2py.py，其中CmdExcel2Py是我们实现的命令类，其继承与CmdBase，实现了GetName，Init，Do等函数

# 2、在base_app.py中注册类型代码如下：
# def _RegisterAllCommand(self):
#    import main_frame.command.cmd_excel2py as cmd_excel2py
#    Excel2PyCmdObj = cmd_excel2py.CmdExcel2Py()
#    self._RegisterCommmand(Excel2PyCmdObj)

# 3、启动脚本如下，其中excel2py是命令名，即GetName返回的名字，后面两个是在命令类中需要用到的参数
#   python main_frame/main.py excel2py config/excel config/setting


class CmdBase:
    def __init__(self):
        self.m_AppObj = None

    @staticmethod
    def GetName():
        return "base_command"

    def Init(self, AppObj):
        """初始化AppObj"""
        self.m_AppObj.Info("Init AppObj")
        self.m_AppObj = AppObj

    def Do(self):
        """执行命令"""
        self.m_AppObj.Info("Start DoExcel2Py")

        szCWD = self.m_AppObj.ConfigLoader.CWD

        # 可以通过self.m_AppObj.CLM获得参数
        # szExcelPath = self.m_AppObj.CLM.GetArg(1)
        # szSettingPath = self.m_AppObj.CLM.GetArg(2)
