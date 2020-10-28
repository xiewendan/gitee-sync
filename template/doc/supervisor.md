<!-- TOC -->

- [1. 问题](#1-%E9%97%AE%E9%A2%98)
- [2. 思路](#2-%E6%80%9D%E8%B7%AF)
- [3. 解决方案](#3-%E8%A7%A3%E5%86%B3%E6%96%B9%E6%A1%88)
    - [3.1. 官方文档](#31-%E5%AE%98%E6%96%B9%E6%96%87%E6%A1%A3)
    - [3.2. 配置文件](#32-%E9%85%8D%E7%BD%AE%E6%96%87%E4%BB%B6)
    - [3.3. 封装对外脚本](#33-%E5%B0%81%E8%A3%85%E5%AF%B9%E5%A4%96%E8%84%9A%E6%9C%AC)
- [4. 结论](#4-%E7%BB%93%E8%AE%BA)
- [5. 展望](#5-%E5%B1%95%E6%9C%9B)
- [6. 文献](#6-%E6%96%87%E7%8C%AE)

<!-- /TOC -->



------------------------------------------------------------------------------
# 1 问题
项目启动进程和关闭进程，都得通过`ps aux | grep main_frame`得到pid，然后`kill -9 pid`，有一点麻烦，为此依然怒supervisor管理进程，方便启动、关闭，避免重复启动进程，同时，如果出现报错，也可以及时提醒。




------------------------------------------------------------------------------
# 2 思路
* 先看官方文档，总体了解supervisor是什么，有什么特性
* 参考具体的示例，编辑项目中配置文件
* 重构、封装



------------------------------------------------------------------------------
# 3 解决方案

## 官方文档
从官方文档来看，supervisor就像一个进程的管理者或监控者，它管理者所有由它启动的进程，你可以通过它控制进程的启动和关闭，可以通过它查看进程的所有log，通过它在发现进程crash的时候可以自动重启。简单的说，你可以做很多关于启动、停止、查看输出等的进程需求。

## 配置文件
* 在bin/supervisor/etc下配置文件：

~~~
[supervisord]
loglevel=debug
logfile=log/supervisord.log     ;日志文件，默认是 $CWD/supervisord.log
pidfile=log/supervisord.pidfile
nodaemon=false

[rpcinterface:supervisor]
supervisor.rpcinterface_factory = supervisor.rpcinterface:make_main_rpcinterface

[inet_http_server]         ;HTTP服务器，提供web管理界面
port=127.0.0.1:9001        ;Web管理后台运行的IP和端口，如果开放到公网，需要注意安全性
[supervisorctl]
; serverurl=unix:///tmp/supervisor.sock ;通过UNIX socket连接supervisord，路径与unix_http_server部分的file一致
serverurl=http://127.0.0.1:9001 ; 通过HTTP的方式连接supervisord

; [program:xx]是被管理的进程配置参数，xx是进程的名称
[program:template]
;command=/Users/stephenxjc/project/xiewendan/tools/template/bin/run.sh ; 程序启动命令
;command=/Library/Frameworks/Python.framework/Versions/3.6/bin/python3 /Users/stephenxjc/project/xiewendan/tools/template/main_frame/main.py -m -d -s
command=python3 main_frame/main.py -m -d -s
directory=../..
;directory=/Users/stephenxjc/project/xiewendan/tools/template
autostart=true       ; 在supervisord启动的时候也自动启动
startsecs=10         ; 启动10秒后没有异常退出，就表示进程正常启动了，默认为1秒
autorestart=true     ; 程序退出后自动重启,可选值：[unexpected,true,false]，默认为unexpected，表示进程意外杀死后才重启
startretries=3       ; 启动失败自动重试次数，默认是3
; user=tomcat          ; 用哪个用户启动进程，默认是root
priority=999         ; 进程启动优先级，默认999，值小的优先启动
redirect_stderr=true ; 把stderr重定向到stdout，默认false
stdout_logfile_maxbytes=20MB  ; stdout 日志文件大小，默认50MB
stdout_logfile_backups = 20   ; stdout 日志文件备份数，默认是10
; stdout 日志文件，需要注意当指定目录不存在时无法正常启动，所以需要手动创建目录（supervisord 会自动创建日志文件）
stdout_logfile=log/1.out
stopasgroup=false     ;默认为false,进程被杀死时，是否向这个进程组发送stop信号，包括子进程
killasgroup=false     ;默认为false，向进程组发送kill信号，包括子进程
~~~

## 封装对外脚本
* start_supervisord.sh:启动supervisord后台
~~~
supervisord -c etc/supervisor.conf
~~~

* stop_supervisord.sh：停止supervisord后台
~~~
kill -9 $(cat log/supervisord.pidfile) 
~~~

* start.sh：启动所有进程
~~~
supervisorctl start all
~~~

* status.sh：查看所有进程状态
~~~
supervisorctl status
~~~

* stop.sh：关闭所有进程
~~~
supervisorctl stop all
~~~


------------------------------------------------------------------------------
# 4 结论
* 基本实现最初的意图，可以方便启动和停止进程




------------------------------------------------------------------------------
# 5 展望




------------------------------------------------------------------------------
# 6 文献

[1]: http://supervisord.org "官方文档"
[2]: https://www.jianshu.com/p/0b9054b33db3 "示例代码"

