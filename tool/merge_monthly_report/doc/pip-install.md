* 安装源是国外的不稳定导致安装失败[[1][]]
  * 升级 pip 到最新的版本 (>=10.0.0) 
  * 安装源设置成清华大学的

  ```
  pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pip -U
  pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
  ```

[1]: https://www.cnblogs.com/ScarecrowMark/p/11249353.html "Python安装模块失败原因汇总"