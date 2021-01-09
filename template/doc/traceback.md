<!-- TOC -->

- [1. 问题](#1-%E9%97%AE%E9%A2%98)
- [2. 思路](#2-%E6%80%9D%E8%B7%AF)
- [3. 解决方案](#3-%E8%A7%A3%E5%86%B3%E6%96%B9%E6%A1%88)
    - [3.1. traceback报错信息格式](#31-traceback%E6%8A%A5%E9%94%99%E4%BF%A1%E6%81%AF%E6%A0%BC%E5%BC%8F)
    - [3.2. 参考cgit.text实现](#32-%E5%8F%82%E8%80%83cgittext%E5%AE%9E%E7%8E%B0)
    - [3.3.](#33)
- [4. 结论](#4-%E7%BB%93%E8%AE%BA)
- [5. 展望](#5-%E5%B1%95%E6%9C%9B)
- [6. 文献](#6-%E6%96%87%E7%8C%AE)

<!-- /TOC -->



------------------------------------------------------------------------------
# 1 问题
游戏运行过程中，会生成traceback，需要及时通知到维护人员进行通知。



------------------------------------------------------------------------------
# 2 思路
* traceback报错信息收集
* traceback报错信息发送通知


------------------------------------------------------------------------------
# 3 解决方案
## traceback报错信息格式
* 需要能够看到堆栈
* 需要能够看到报错处的代码
* 需要能够看到局部变量和报错行使用的变量的值

## 参考cgit.text实现

最终效果如下

~~~
Traceback (most recent call last):
  File "E:/project/xiewendan/tools/template/main_frame/main.py", line 84, in <module>
    Main(sys.argv)
  File "E:/project/xiewendan/tools/template/main_frame/main.py", line 78, in Main
    StartApp(args)
  File "E:/project/xiewendan/tools/template/main_frame/main.py", line 58, in StartApp
    AppObj.DoLogic()
  File "E:\project\xiewendan\tools\template\main_frame\base_app.py", line 67, in DoLogic
    CommandObj.Do()
  File "E:\project\xiewendan\tools\template\main_frame\command\cmd_test_code.py", line 29, in Do
    raise my_exception.MyException("xjc")

     24         szFileFullPath = "{0}/{1}".format(szCWD, szFilePath)
     25 
     26         import hashlib
     27         Md5Obj = hashlib.md5()
     28         import common.my_exception as my_exception
>    29         raise my_exception.MyException("xjc")
     30 
     31         with open(szFileFullPath, "rb") as FileObj:
     32             while True:
     33                 szData = FileObj.read(1024)

  Local var:
    my_exception = <module 'common.my_exception' from 'E:\\project\...endan\\tools\\template\\common\\my_exception.py'>
    Md5Obj = <md5 HASH object @ 0x000001EC36024A58>
    hashlib = <module 'hashlib' from 'D:\\Python36\\lib\\hashlib.py'>
    szFileFullPath = r'E:\project\xiewendan\tools\template/data/aaa.exe'
    szFilePath = 'data/aaa.exe'
    szCWD = r'E:\project\xiewendan\tools\template'
    self = <main_frame.command.cmd_test_code.CmdTestCode object>
    my_exception.MyException = <class 'common.my_exception.MyException'>
~~~

* 1 堆栈
* 2 代码
* 3 局部变量值

> 注：如果遇到try exception，那么堆栈不够完整，此处调用inspect.stack()，可以获得完整堆栈，和以后堆栈信息裁剪整合，可以得到想要的堆栈

## 




------------------------------------------------------------------------------
# 4 结论




------------------------------------------------------------------------------
# 5 展望




------------------------------------------------------------------------------
# 6 文献


