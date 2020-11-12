<!-- TOC -->

- [1. 问题](#1-%E9%97%AE%E9%A2%98)
- [2. 思路](#2-%E6%80%9D%E8%B7%AF)
- [3. 解决方案](#3-%E8%A7%A3%E5%86%B3%E6%96%B9%E6%A1%88)
    - [3.1. 命令基类](#31-%E5%91%BD%E4%BB%A4%E5%9F%BA%E7%B1%BB)
    - [3.2. app中注册类管理](#32-app%E4%B8%AD%E6%B3%A8%E5%86%8C%E7%B1%BB%E7%AE%A1%E7%90%86)
    - [3.3. app启动检查](#33-app%E5%90%AF%E5%8A%A8%E6%A3%80%E6%9F%A5)
    - [3.4. 实现一个新命令](#34-%E5%AE%9E%E7%8E%B0%E4%B8%80%E4%B8%AA%E6%96%B0%E5%91%BD%E4%BB%A4)
        - [3.4.1. 以配置表转表工具为例](#341-%E4%BB%A5%E9%85%8D%E7%BD%AE%E8%A1%A8%E8%BD%AC%E8%A1%A8%E5%B7%A5%E5%85%B7%E4%B8%BA%E4%BE%8B)
- [4. 结论](#4-%E7%BB%93%E8%AE%BA)
- [5. 展望](#5-%E5%B1%95%E6%9C%9B)
- [6. 文献](#6-%E6%96%87%E7%8C%AE)

<!-- /TOC -->



------------------------------------------------------------------------------
# 1 问题
目前系统，新增一个功能，就得去新建一个app，对于一些简单的功能，新建app感觉有点太笨重了，框架不够灵活，为此，希望实现一个command-system，该系统实现功能放到一个文件中，然后在base_app中注册，最后，执行的时候传入参数即可，满足拓展轻量的、简单功能的需求。




------------------------------------------------------------------------------
# 2 思路
* 实现一个命令基类
* 实现app注册命令类相关方法
* app启动，自动检测命令，并执行相应命令机制
* 新增一个命令的过程



------------------------------------------------------------------------------
# 3 解决方案

## 命令基类
* GetName：命令的名字
* Init：初始化，可以通过self.m_AppObj.CLM获得命令参数
* Do：实际执行
~~~
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

        # 可以通过self.m_AppObj.CLM获得参数
        # szExcelPath = self.m_AppObj.CLM.GetArg(1)

    def Do(self):
        """执行命令"""
        self.m_AppObj.Info("Start DoExcel2Py")

        szCWD = self.m_AppObj.ConfigLoader.CWD
~~~


## app中注册类管理

* 用一个dict管理命令名字到命令对象的映射关系，`self.m_dcitCommand`
* 提供_RegisterAllCommand，_RegisterCommand，_UnRegisterCommand等函数，实现注册和注销命令

~~~
    def _RegisterAllCommand(self):
        import main_frame.command.cmd_excel2py as cmd_excel2py
        Excel2PyCmdObj = cmd_excel2py.CmdExcel2Py()
        self._RegisterCommmand(Excel2PyCmdObj)

    def _RegisterCommmand(self, CommandObj):
        szName = CommandObj.GetName()
        assert szName not in self.m_dictCommand
        self.m_dictCommand[szName] = CommandObj

    def _UnRegisterCommand(self, szName):
        if szName in self.m_dictCommand:
            del self.m_dictCommand[szName]
~~~

## app启动检查
* 检查是否存在命令名，如果存在，则从`self.m_dictCommand`中找到命令对象并执行
~~~
    szCmdName = self.m_CLMObj.GetArg(0)
    if szCmdName is not None:
        CommandObj = self._GetCommand(szCmdName)
        CommandObj.Init(self)
        CommandObj.Do()

~~~

* 传入参数列表中，第一个非选项参数（即不是以-或--开头的选项），我们认为是命令名，后续为该命令的参数
  举个栗子
~~~
python main_frame/main.py excel2py config/excel config/setting
~~~
  * `excel2py`是第一个非选项的参数，我们解析为命令名
  * `config/excel`，`config/setting`，我们认为是命令需要的一些参数，需要命令自己去解析

## 实现一个新命令

* 1、希望实现新的类型时，需要继承与CmdBase，然后，实现GetName，Init，Do等函数
* 2、在base_app.py中的_RegisterAllCommand函数，注册新类型
* 3、在启动中传入命令名和命令需要的参数

### 以配置表转表工具为例
 
* 1、新类型的代码：main_frame.command.cmd_excel2py.py，其中CmdExcel2Py是我们实现的命令类，其继承与CmdBase，实现了GetName，Init，Do等函数
* 2、在base_app.py中注册类型代码如下：
~~~
 def _RegisterAllCommand(self):
    import main_frame.command.cmd_excel2py as cmd_excel2py
    Excel2PyCmdObj = cmd_excel2py.CmdExcel2Py()
    self._RegisterCommmand(Excel2PyCmdObj)
~~~

* 3、启动脚本如下，其中excel2py是命令名，即GetName返回的名字，后面两个是在命令类中需要用到的参数
~~~
   python main_frame/main.py excel2py config/excel config/setting
~~~

------------------------------------------------------------------------------
# 4 结论

目前的命令系统基本能够满足我们的需求，后续需要在command发现机制这边进一步优化，实现不需要注册，自动去指定目录下搜索继承与CmdBase的所有类，自动注册到命令系统中



------------------------------------------------------------------------------
# 5 展望




------------------------------------------------------------------------------
# 6 文献


