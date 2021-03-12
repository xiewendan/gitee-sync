<!-- TOC -->

- [1. 目的](#1-%E7%9B%AE%E7%9A%84)
- [2. 特性](#2-%E7%89%B9%E6%80%A7)
    - [2.1. 已有特性](#21-%E5%B7%B2%E6%9C%89%E7%89%B9%E6%80%A7)
    - [2.2. 待实现特性](#22-%E5%BE%85%E5%AE%9E%E7%8E%B0%E7%89%B9%E6%80%A7)
- [3. 使用](#3-%E4%BD%BF%E7%94%A8)
    - [3.1. 配置](#31-%E9%85%8D%E7%BD%AE)
    - [3.2. 运行准备](#32-%E8%BF%90%E8%A1%8C%E5%87%86%E5%A4%87)
    - [3.3. 运行](#33-%E8%BF%90%E8%A1%8C)
    - [3.4. linux发布](#34-linux%E5%8F%91%E5%B8%83)
- [4. 文献](#4-%E6%96%87%E7%8C%AE)

<!-- /TOC -->

# 1. 目的

作为工具的模板，以后新建工具，都可以基于该模板创建。log配置以及封装了配置文件加载，并提供了一些常用的库，希望以此为基础，不断完善这个模板，方便后续工具的开发。

# 2. 特性

## 2.1. 已有特性
* log系统：文件log系统，不同levellog
* 支持添加命令行参数
* 支持单元测试
* 支持性能分析
* 配置文件template化，支持变量
* 配置scheduler任务
* 发布到外网
* 帮助文档：输出一份帮助文档。main.py -h，直接输出帮助文档。doc下的一个markdown文档
* excel配置表转py
* 可以发布成exe
* 新增traceback报错,如果有报错，会发dingding提醒

## 2.2. 待实现特性
* enum ConstEnum:不可修改
* enum NoDupEnum:不可重复
* unity python和服务器连接，构建一个有模型有动作的助理，他会有ui的输出，和场景的指引
* 数据库
* UI框架：
* 网络：缺乏网络接口
* 性能分析整合火焰图
* slave客户端
* 多线程框架
* 多进程框架
* https://github.com/semantic-release/semantic-release
* 搜索：
    [实打实的谷歌搜索技巧](https://zhuanlan.zhihu.com/p/25525658)
    [google api](https://developers.google.com/apis-explorer)

# 3. 使用

## 3.1. 配置

* 配置文件路径：
~~~
cp config/render_template.yml config/render.yml
对render.yml配置
~~~

## 3.2. 运行准备


## 3.3. 运行
* windows运行
~~~
bin/run.bat
~~~

## 3.4. linux发布
* 通过git pull更新代码
* linux后台运行
~~~
nohup python3 -u main_frame/main.py  2>&1 &
~~~

> -u可以避免cache 输出
> 2>&1：把错误输出也输出到一起
> nohup command &：做到后台运行，并且控制台关闭也不会停止
>
>


# 4. 文献

