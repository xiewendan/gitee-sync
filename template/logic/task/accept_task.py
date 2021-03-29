import logic.task.base_task as tasK_base
import logic.task.task_enum as task_enum


class AcceptTask(tasK_base.BaseTask):
    """"""

    def __init__(self, dictTaskData):
        super().__init__(dictTaskData)

    @staticmethod
    def GetType(self):
        return task_enum.ETaskType.eAccept
