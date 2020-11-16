<!-- TOC -->

- [1. 目的](#1-%E7%9B%AE%E7%9A%84)
- [2. 流程](#2-%E6%B5%81%E7%A8%8B)
- [3. 使用](#3-%E4%BD%BF%E7%94%A8)
    - [3.1. 配置](#31-%E9%85%8D%E7%BD%AE)
    - [3.2. 发布](#32-%E5%8F%91%E5%B8%83)
    - [3.3. 运行](#33-%E8%BF%90%E8%A1%8C)
- [4. 文献](#4-%E6%96%87%E7%8C%AE)

<!-- /TOC -->

# 1. 目的

整合月报工具，方便更好的整合月报

# 2. 流程
* 拷贝`工作内容`和`天数`，并保留他们的格式
* 合并单元格：`时间`、`微调`、`总计`
* 调整`总计`公式的范围
* 根据模板，赋予默认值：`重要程度`、`代码质量`、`实现难度`、`交付效率`
* 异常天数报错：一个月总天数默认22天，超过天数会报错。默认天数通过启动脚本参数传入。


# 3. 使用

## 3.1. 配置

* 配置文件路径：
~~~
cp config/render_template.yml config/render.yml
对render.yml配置
~~~

## 3.2. 发布
~~~
cd bin

release_exe.bat
~~~

* 会在binexe目录下生成main.exe


## 3.3. 运行
* windows运行
~~~
cd bin
run_exe.bat
~~~

run_exe.bat说明:
~~~
cd ..

binexe\main.exe merge_monthly_report data/xx月贡献评分.xlsx data/src data/dest 22

cd bin

pause
~~~

* merge_monthly_report：命令名，不能修改
* data/xx月贡献评分.xlsx：月报模板，必须有xx，会自动转成上个月
* data/src：团队成员的月报存放文件夹。月报模板汇总表中声明有几个人，就必须几份，否则会报错。
* data/dest：输出月报。如10月贡献评分。
* 22：表示本月天数。如果天数总和超过该天数，会报错提醒，需要自己核实一下该同学的天数是否正常。

# 4. 文献


