# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2021/3/31 2:05

# desc:

import common.base_factory as base_factory


class TaskFactory(base_factory.BaseFactory):
    def __init__(self):
        super().__init__()

        self.RegisterAll()

    def GetClassData(self):
        """

        :return:
            [
                [
                    "common/async_net/connection", # 相对当前目录
                    r"^xx_[_a-zA-Z0-9]*.py$", # 文件正则表达式
                    xx_connection_base.XxConnectionBase # 基类
                ]
            ]
        """
        import logic.task.base_task as base_task

        return [
            [
                "logic/task",  # 相对当前目录
                r"^[_a-zA-Z0-9]*_task.py$",  # 文件正则表达式
                base_task.BaseTask,  # 基类
            ]
        ]


g_TaskFactory = TaskFactory()
Create = g_TaskFactory.Create
