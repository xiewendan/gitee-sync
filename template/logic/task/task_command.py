class TaskCommand:
    """"""

    def __init__(self, szCommandFormat: str):
        self.m_szComandFormat = szCommandFormat

    def ToStr(self):
        return self.m_szComandFormat
