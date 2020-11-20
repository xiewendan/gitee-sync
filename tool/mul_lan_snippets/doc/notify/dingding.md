

<!-- TOC -->

- [1. problem](#1-problem)
- [2. code](#2-code)
- [3. config](#3-config)
- [4. conclusion](#4-conclusion)
- [5. reference](#5-reference)

<!-- /TOC -->







------------------------------------------------------------------------------
# 1 problem
try to use weixin to send warning msg, but weixin limit use. we find dingding is good at send warning msg to phone. we choose it.

# 2 code
`common/notify/ding_ding_mgr.py`

# 3 config
* open the dingding system. you should set dingding variable(webhook, secret, keyword, to) in config/render.yml. dingding variable can reference[[][2]]

  ~~~
      dingding:
          webhook: xx
          secret: xx
          keyword: xx
          to: xx
  ~~~

* run
  ~~~
  python3 main_frame/main.py -d
  or
  python3 main_frame/main.py --dingding
  ~~~

------------------------------------------------------------------------------
# 4 conclusion
* now we can easy get notify from dingding




------------------------------------------------------------------------------
# 6 reference
[1]: https://www.jianshu.com/p/03600ef60ea1 "使用钉钉发送消息到群"
[2]: https://ding-doc.dingtalk.com/doc#/serverapi2/qf2nxq "使用钉钉机器人"
[3]: https://blog.csdn.net/weixin_30551963/article/details/98959436?utm_medium=distribute.pc_relevant_t0.none-task-blog-BlogCommendFromMachineLearnPai2-1.channel_param&depth_1-utm_source=distribute.pc_relevant_t0.none-task-blog-BlogCommendFromMachineLearnPai2-1.channel_param "钉钉返回消息解析"






