## 流程图 

```mermaid
graph TD;

aa-->bb


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

## 边界

边界1：发送数据时，存在连接或不存在连接
边界2：监听，已经存在监听或不存在监听
边界3：accept socket需要确保是否已经存在连接，避免存在多个1对1连接，最后发送数据，会有问题

边界4：网络断开，可能会导致整个发送异常(可能性比较小，但一旦出现，问题会比较大)

## 类接口设计

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