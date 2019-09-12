##  目的
因为vscode启动项目，只能添加exclude，不能配置指定后缀的文件才加载。
为此，写这个工具，会遍历vscode的工程配置文件，遍历所有的目录，获得所有文件的后缀列表，除了白名单里面的后缀，其余全部加载exclude file里面，从而，尽量减少vscode加载的文件数量，并且保证在使用过程如查找的不会那么卡。


## 配置

* 配置文件路径：conf/conf.conf
~~~
[common]
VSCodeWorkspacePath = E:\project\dm109\py3_2019\trunk\Project.code-workspace
ExtList = .json,.cs,.py
ExcludeList = **/.vscode,**/.idea,**/__pycache__
~~~
  * VSCodeWorkspacePath:指定vscode的workspace路径，需要配置为完整路径
  * ExtList: 白名单的后缀列表
  * ExcludeList: 一定要加到Exclude的列表，可以理解为是黑名单

> 注意需要确保Project.code-workspace文件是json格式正确的文件，否则会报错

## 运行准备


## 运行
bin/run.bat

## 版本修改
### 1.0
* conf文件是配置文件，添加到白名单里面


