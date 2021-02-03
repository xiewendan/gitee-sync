<!-- TOC -->

- [1. 问题](#1-%E9%97%AE%E9%A2%98)
- [2. 思路](#2-%E6%80%9D%E8%B7%AF)
- [3. 解决方案](#3-%E8%A7%A3%E5%86%B3%E6%96%B9%E6%A1%88)
    - [3.1. 服务框架](#31-%E6%9C%8D%E5%8A%A1%E6%A1%86%E6%9E%B6)
        - [3.1.1. 注册服务](#311-%E6%B3%A8%E5%86%8C%E6%9C%8D%E5%8A%A1)
        - [3.1.2. 初始化服务](#312-%E5%88%9D%E5%A7%8B%E5%8C%96%E6%9C%8D%E5%8A%A1)
        - [3.1.3. 获取服务，执行功能](#313-%E8%8E%B7%E5%8F%96%E6%9C%8D%E5%8A%A1%E6%89%A7%E8%A1%8C%E5%8A%9F%E8%83%BD)
        - [3.1.4. 销毁服务](#314-%E9%94%80%E6%AF%81%E6%9C%8D%E5%8A%A1)
        - [3.1.5. 注销服务](#315-%E6%B3%A8%E9%94%80%E6%9C%8D%E5%8A%A1)
    - [3.2. 服务基类](#32-%E6%9C%8D%E5%8A%A1%E5%9F%BA%E7%B1%BB)
    - [3.3. 服务器子类实现举例](#33-%E6%9C%8D%E5%8A%A1%E5%99%A8%E5%AD%90%E7%B1%BB%E5%AE%9E%E7%8E%B0%E4%B8%BE%E4%BE%8B)
- [4. 结论](#4-%E7%BB%93%E8%AE%BA)
- [5. 展望](#5-%E5%B1%95%E6%9C%9B)
- [6. 文献](#6-%E6%96%87%E7%8C%AE)

<!-- /TOC -->



------------------------------------------------------------------------------

# 1. 问题

系统拓展，增加越来越多的可配置开启的功能，如果都写到BaseApp中，BaseApp会不堪重负，为此，希望将可配置的功能封装成服务，在启动时，根据配置，单独开启对应的服务。



------------------------------------------------------------------------------

# 2. 思路
* 服务框架
  * 自动扫描目录，注册服务
  * 根据依赖关系，顺序初始化服务
  * 获取服务，执行功能
  * 销毁服务
  * 注销服务

* 服务基类设计
* 服务子类实现举例


------------------------------------------------------------------------------

# 3. 解决方案

## 3.1. 服务框架

### 3.1.1. 注册服务

> 相关代码请看`BaseApp._AutoRegisterService`

* 创建`main_frame/service`作为`service`的目录，后续将所有的子类，都放到该目录下

* 创建`service_base.py`，`ServiceBase`为所有类的基类，用于实现通用服务框架

* 扫描服务规则
  * 文件名规则符合:`^[0-9a-zA-Z_]*service.py`
  * 文件中的类，继承与`ServiceBase`
  * 直接注册，并维护`dictService`可以为，可以为Name，为此`ServiceBase`增加接口如下
    ~~~
    class ServiceBase:
      @staticmethod
      def GetName(self):
        return "name"
    ~~~

### 3.1.2. 初始化服务

> 相关代码请看`BaseApp._InitAllService`

* 根据配置选项，初始化需要的服务
  * 输入参数中，传入需要开启的服务选项，如
    ~~~
    python main_frame/main.py -d
    ~~~

    `-d`就是服务选项

  * `ServiceBase`添加接口`GetOptList`
    ~~~
    @staticmethod
    def GetOptList():
      return []
    ~~~

    每个子类对应实现。

  * 在注册服务器的时候，会维护`dictServiceOpt2Name`
  * 根据输入参数的选项，去`dictServiceOpt2Name`中查找，如果存在，就初始化对应的`Service`

* 依赖关系，顺序初始化服务
  * 需要知道相互的依赖关系，`ServiceBase`添加接口`_GetDepServiceList`
    ~~~
    def _GetDepServiceList(self):
      return []
    ~~~

    以此，知道当前服务所依赖的服务

  * 初始化的时候，优先初始化依赖的服务，然后再初始化自己（是一个简单的递归）
    ~~~
    listDepServiceName = self._GetDepServiceList()
    for szDepServiceName in listDepServiceName:
        self.m_AppObj.GetService(szDepServiceName).Init(self.m_AppObj, listInitingServiceName)

    self._OnInit()
    ~~~

  * 为了解决依赖环的问题，加了一个`listInitingServiceName`，其实，用`stack`来描述更准确，举例如下
    * 依赖关系如下
      * A->B->C
      * A->D->C
    * stack变化如下
      * 初始化`A`：`A`
      * 根据依赖，初始化`B`：`A`->`B`
      * 根据依赖，初始化`C`:`A`->`B`->`C` 
      * 等C初始化完：`A`->`B`
      * 等B初始化完：`A`
      * 根据依赖，初始化`D`：`A`->`D`
      * 根据依赖，初始化`C`，发现C已经初始化：`A`->`D`
      * D初始化完：`A`
      * A初始化完：
    * 如果依赖关系存在环，如 A->B->C->A，通过堆栈，可以很方便判断出环，并输出环如下:
      ~~~
      ->A
        B
        C
      ->A
      ~~~

      可以清晰的反馈出环依赖报错
    

### 3.1.3. 获取服务，执行功能

* 根据名字去找到服务，然后调用对应服务的接口
  ~~~
  MailMgrObj = self.GetApp().GetService("mail").GetMailMgr()
  ~~~

### 3.1.4. 销毁服务
* 按照顺序销毁Service

### 3.1.5. 注销服务
* 递归，注销Service

## 3.2. 服务基类
* 参见代码`service_base.py`

## 3.3. 服务器子类实现举例
* 要求
  * 放到`main_frame/service`目录下
  * 文件命名符合规则：`^[0-9a-zA-Z_]*service.py`
  * 子类继承于service_base.ServiceBase
  * 重载实现方法
    * GetOptList
    * GetName
    * GetDepServiceList：根据需要重载，非必须
    * _OnInit：根据需要重载，非必须
    * _OnDestroy：根据需要重载，非必须

* 示例
  * `main_frame/service/scheduler_service.py`

------------------------------------------------------------------------------

# 4. 结论
暂时，每个服务都是唯一的，如果同一个服务，需要有多一个，基于名字的机制，会有问题，暂时不考虑




------------------------------------------------------------------------------

# 5. 展望




------------------------------------------------------------------------------

# 6. 文献


