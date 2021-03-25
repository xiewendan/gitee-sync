# 1. xx_net

## 1.1. 流程图 

```mermaid
graph TD;

主线程-->xx_net.Listen-->获得监听锁-->放到监听队列里面-->释放监听锁
主线程-->xx_net.Send-->获得发送锁-->添加到发送队列里面-->释放发送锁
主线程-->xx_net.Recv-->获得接收锁-->从接收队列中获取数据-->释放接收锁

socket读写事件处理
收发线程-->select-->socket事件处理-->写事件-->ip_port发送buff-->发送数据-->数据发送完成-->设置socket读事件
                                                              发送数据-->数据未发送完成-->不设置socket事件

                   socket事件处理-->读事件-->读取数据-->ip_port接收buff

                   socket事件处理-->accept_socket-->不存在连接-->添加到socket映射表-->设置socket读事件
                                   accept_socket-->存在连接-->放弃连接-->记录log

从发送队列到发送buff
收发线程-->xx_net.GetSendData-->获得发送锁-->获取发送队列信息-->释放发送锁-->序列化-->ip_port发送buff

修改写标识
ip_port发送buff-->遍历ip_port获得socket-->存在socket-->设置socket读写事件
                 遍历ip_port获得socket-->不存在socket-->发起连接-->添加到socket映射表-->设置socket读写事件

从接收buff到接收队列
ip_port接收buff-->数据完整-->反序列-->获得接收锁-->放到接收队列-->释放接收锁

socket监听注册
收发线程-->获得监听锁-->socket监听队列-->释放监听锁-->是否监听该端口-->没有监听过该端口-->启动监听
                                                   是否监听该端口-->有监听过该端口-->放弃-->记录log
```

## 1.2. 边界

边界1：发送数据时，存在连接或不存在连接
边界2：监听，已经存在监听或不存在监听
边界3：accept socket需要确保是否已经存在连接，避免存在多个1对1连接，最后发送数据，会有问题

边界4：网络断开，可能会导致整个发送异常(可能性比较小，但一旦出现，问题会比较大)

## 1.3. 类接口设计

~~~
xx_net
    m_queueSendData
    m_queueRecvData
    m_queueListenData

    Listen(ip, port)
    
    Send(ip, port, dictData)
    _RequireAddSendData()
    
    HandleRecv()
    _RequireGetRecvData()-->listDictData(包含ip和端口):需要获得接收锁
    _Handle(listDictData)
    
    GetSendData()
    _RequireGetSendData():需要获得发送锁
    
    AddRecvData():需要获得接收锁
    _RequireAddRecvData()
~~~


~~~
xx_socket_mgr
    m_dictID2Socket
    m_dictIPPort2ID
    
    Run()
    _HandleSocketEvent()
      _Read
      _Write
      _ReadWrite
      _Accept
    _SerializeSendData()
    _UpdateWriteEvent()
    _HandleListen()
~~~

# 2. xx_connection

## 2.1. 需求点
* XxDispatcher：socket封装，进行监听

## 2.2. 流程图

```
nConnectionID = XxConnectionMgr.CreateConnection(type)
    需要提前注册好类型
    根据传入的类型，创建Connection
    Dispatcher：需要创建出socket，并设置好nonblocking

XxConnectionFactory.CreateConnection(type)
    封装一层Factory，更符合工厂模式设计
     
XxConnectionMgr.Listen(nConnectionID， szIp, nPort)
    确定ConnectionID存在，且是可以监听的（通过connection类型来区分）
    Connection存在一个DispatcherID，并调用Listen(nDispatcherID, szIp, nPort)
    Dipsatcher：Listen：参考_HandleListen写法，边界，需要考虑重复监听的报错处理

XxConnectionMgr.Connect(nConnectionID, szTargetIp, nTargetPort)
    Connection:注意检查Connection的状态，每个操作之前，需要确保状态是处于尚未连接状态
    Dispatcher：参考Asyncore，connect需要注意返回值怎么获得？

XxConnectionMgr.Send(nConnectionID, dictData)
    Connection:转发到底层
    BufferDispatcher：将dictData序列化，其中，需要添加报头和数据，并转成二进制
    Dispatcher：调用send接口发送数据，参考asyncore处理异常，根据返回的发送成功大小，更新现有发送BytesIO

XxConnectionMgr.Update()
    定时处理底层的poll

XxConnectionMgr.Close(nConnectionID)
    Connection.Close：根据创建过程，重新初始化变量
    Dispatcher.Close：根据创建过程，重新初始化变量

XxConnectionMgr.Destroy()
    对象自身销毁过程，调用每一个Connection的Destroy

XxDataPack
    headersize | headerdata | data

    Serialize
        先将dictData转成二进制
        再将二进制数据加上报头
    Unserialize
        先读取报头大小
        在读取整个数据长度
        总体解析

    需要简单测试代码，测试接口是否正常

XxDataHeader
    m_nHeaderSize
    m_nDataSize
```


## 2.3. 基本接口
~~~
XxConnection
    m_szTargetIp
    m_nTargetPort
    OnConnect
    OnDisconnect
~~~

~~~
XxConnectionMgr
    m_XxNetObj
    m_dictID2Connection

    XxConnectionMgr()

    CreateConnection(szTargetIp, nTargetPort, dictData)-->nConnectionID
    Listen(szIp, nPort)

    Connect(nConnectionID)

    Send(nConnectionID, dictData)

    Update()

    Close(nConnectionID)

    Destroy()
~~~

## 2.4. 调研
* listen重复监听的报错是啥
* MsgHeader相关代码阅读

## 2.5. 实现

## 2.6. 边界
* 模块测试
  * DataPack序列化和反序列化
* 整合测试
  * 一个客户端：发起连接
               连接成功，发送数据
               接收数据直接关闭

  * 一个服务端：接收请求
               接收数据
               返回数据
               等待对方关闭


# 3. 集群

## 3.1. 图

### 3.1.1. Reg
* 架构图
```mermaid
flowchart TD;

subgraph Reg 
    Reg
end

subgraph Exe3 
    Exe3
end

subgraph Exe2 
    Exe2
end

subgraph Exe1 
    Exe1
end

Reg<-->Exe1
Reg<-->Exe2
Reg<-->Exe3

```
* 注册流程
```mermaid
flowchart TD;

subgraph Reg 
    Reg
    ExeInReg
end
subgraph Exe
    Exe2Reg
end

Exe2Reg--1-->Reg
Reg--2-->ExeInReg
ExeInReg--3-->Exe2Reg
```

* 1 向Reg发起注册
* 2 Reg创建ExeInReg连接
* 3 ExeInReg和Exe2Reg可以正常通信
* Exe2Reg会发送自身的信息给ExeInReg，放到ExecutorMgr中

### 3.1.2. Exe任务图

* 任务架构图
```mermaid
flowchart TD;

subgraph Reg 
    Reg
end

subgraph Exe2 
    Exe2
    FileExe2
    Exe2Exe2
    FileExe2Exe2
end

subgraph Exe1 
    Exe1
    FileExe1
    ExeInExe1
    FileExeInExe1
end

Reg<-->Exe1
Reg<-->Exe2
Exe2Exe2<-->ExeInExe1
FileExe2Exe2<-->FileExeInExe1
```

* 任务流程图
```mermaid
flowchart TD;

subgraph Reg 
    ExeInReg1
end

subgraph Exe1 
    Exe2Reg1
    Exe1
    ExeInExe1
    FileExeInExe1
    FileExe1
end

subgraph Exe2 
	Exe2Reg2
	Exe2Exe2
	FileExe2Exe2
end

Exe2Reg1--1-->ExeInReg1
ExeInReg1--2-->Exe2Reg2
Exe2Reg2--3-->Exe2Exe2
Exe2Exe2--4-->Exe1
Exe1--5-->ExeInExe1
ExeInExe1--6-->Exe2Exe2
Exe2Exe2--7-->FileExe2Exe2
FileExe2Exe2--8-->FileExe1
FileExe1--9-->FileExeInExe1
FileExeInExe1--10-->FileExe2Exe2


```

* 1、 Exe2Reg1发布任务

* 2、 ExeInReg1分配任务给Exe2Reg2

* 3、Exe2Reg2创建连接Exe2Exe2

* 4、Exe2Exe2连接Exe1

* 5、Exe1创建ExeInExe1

* 6、ExeInExe1和Exe2Exe2形成连接

* 7、Exe2Exe2检查任务需求，需要文件的话，创建FileExe2Exe2

* 8、FileExe2Exe2连接FileExe1

* 9、FileExe1创建FileExeInExe1

* 10、FileExeInExe1和FileExe2Exe2形成连接，FileExe2Exe2获得在FileExeInExe1的ID

* 请求文件流程图
```mermaid
flowchart TD;

subgraph Exe1 
    ExeInExe1
    FileExeInExe1
end

subgraph Exe2 
	Exe2Exe2
	FileExe2Exe2
	完成回调
end

Exe2Exe2--1-->ExeInExe1--2-->FileExeInExe1--3-->FileExe2Exe2--4-->完成回调

```

* 1、Exe2Exe2请求文件，包含FileExeInExe1的ID，同时把完成回调ID发送过去。注意，需要考虑超时机制：暂定5分钟。
* 2、ExeInExe1通知FileExeInExe1发送文件，包含回调ID
* 3、FileExeInExe1发送文件
* 4、FileExe2Exe2中接收到数据，并调用传入过来的回调ID

### 3.1.3. 下载文件

```mermaid
flowchart LR;

文件名大小MD5传入下载系统-->检测空间是否足够-->更新文件时间-->返回需要下载的文件块-->发送包到exe2-->接收包放到文件队列中修改可写标志-->可写回调-->从文件队列获取文件并写到缓存中-->持续发送文件
下载系统每次接收文件-->更新文件内容-->更新索引信息-->根据累计下载文件总量判断是否下载完成-->下载完成-->触发下载完成回调

```

* 边界1：download预设大小，空间超出大小，触发资源回收 done ok
* 边界2：下载系统，断点续传 done ok
* 边界3：回调函数，可能存在多个 done ok
* 边界4：回调函数，在重启后，需要清理【下载文件系统支持断点续传，但回调系统不支持断点续传】 done ok
* 边界5：断开连接，记得需要清理：1、接收包发送文件队列，2、发送缓冲 3、接收缓冲清理。Accept连接需要销毁 done ok
* 边界6：文件大小md5重复，可以添加到现有下载任务的完成回调中，不需要新增任务 done ok
* 边界11：下载失败，通知上层回调 
  * 下载系统超时 done ok
  * 断开连接
  * 下载完成，Md5、文件大小加测失败 done 
  * 缓存空间不足：单个文件超出下载空间，或任务需要的多个文件总空间超出上限 done ok

* 接口实现
~~~
DownloadSystem
    Download(szMd5, fileName, nSize, nCbID)
        现有系统已经有下载好的文件，更新使用时间，返回给外部系统处理

        现有系统是否已经存在下载任务
        
        现有系统空间是否足够

        空间不足，如何清理空间
        如何管理回调id
        
        失败返回报错信息

        返回需要下载的文件块信息
    
    Write(szMd5, fileName, nSize, nBlockIndex, DataBlock):
        判断文件一致性
        检查大小是否ok，及nOffset+Data
        写入文件
        更新索引，检查文件是否接受完毕
        接受完毕，检查文件是否正常，是否触发完成回调
    
    CheckOvertime():定时调用，需要使用定时器实现
        每个下载任务检查是否超时，对于执行超时的任务，需要结束下载任务，并通知上层，并清理下载回调
~~~

bug：目前的定时器是进程定时器，属于异步定时器，可以考虑实现同步定时器，来实现在主线程中，触发定时操作.

* download_system目录设计
  files：保存已经下载部分的代码
  index.json：[
      [szMd5, filename, size, nTime, downloaded_size, default_block_size, last_block_size, listDownloadedBlockIndex]
  ]

* 索引，解决空间清理

* donwload_system：解决文件管理和执行回调


# 4. 任务发布

```mermaid
graph TD;

新建任务放到任务发布系统-->发送给register服-->register服分配任务给其它执行服-->执行服接收任务放到接受管理器-->请求执行所需数据-文件-->回调检测-->所有数据收集完毕执行任务-->执行完毕-->通知发布服取结果文件-->发布服主动取结果文件-->结果文件取完-->通知执行服任务结束-->发布服通知外部任务执行结束把结果返回

回调检测-->失败通知原服务器执行失败
```

DisTask：分布式任务
    

DisTaskMgr：发布任务管理器

AcceptTask：接受任务

AcceptTaskMgr

AssignTaskMgr


所有异常情况处理情况:

> 发送给register服，可以优化为单独的任务分配服，register服只负责注册

## 4.1. 异常处理
* 1 发布失败
  * 没有连接上register服，直接报错
  * DisTaskMgr需要定时触发，检查所有尚未分配的任务，并走分配流程
  * 允许重复发布任务
  * 等待分配和领取时间1分钟（可以指定分配领取时间）
  * 等待执行结果返回5分钟（可以指定过期时间）

* 2 分配失败：
  * 可能没有其它服务器，报错，并等待继续发布
  * 任务分配即删除

* 3 接收任务
  * 无法连接到远端，直接放弃任务
  * 无法请求文件，直接放弃任务
  * 无法执行，任务环境有问题，直接放弃任务
  * 执行报错，直接放弃任务

* 4 放弃任务
  * 发送一条消息，通知发布服：为了简化，暂时不需要发送

* 5 请求结果数据失败
  * 

