# -*- coding: utf-8 -*-

Key0 = 'ID'
Key1 = 'name'
Key2 = 'desc'
Key3 = 'prefix'
Key4 = 'python'
Key5 = 'csharp'
Key6 = 'cpp'
Key7 = 'markdown'
Key8 = 'java'

mul_lan = {

	10001: {
		Key0: 10001,
		Key1: '包含库',
		Key2: '包含库',
		Key3: 'fimport',
		Key4: 'import sys',
		Key5: '',
		Key6: '#include <iostream>',
		Key7: '',
		Key8: '',
	},

	10002: {
		Key0: 10002,
		Key1: '使用namespace',
		Key2: '使用namespace',
		Key3: 'fusing',
		Key4: '',
		Key5: 'using System;',
		Key6: 'using namespace std;',
		Key7: '',
		Key8: '',
	},

	10003: {
		Key0: 10003,
		Key1: '定义函数',
		Key2: '定义函数',
		Key3: 'function',
		Key4: '''def Main():
    print("Hello World\r")

''',
		Key5: '''static void Main(string[] args)
{
        System.Console.WriteLine("Hello World\r");
}''',
		Key6: '''int main()
{
    cout << "Hello World\r"; 
    return 0;
}''',
		Key7: '',
		Key8: '',
	},

	10004: {
		Key0: 10004,
		Key1: '定义类',
		Key2: '定义类',
		Key3: 'fclass',
		Key4: '''class $1:
    def __init__(self):
        pass
        $2''',
		Key5: '''public class $TM_FILENAME_BASE
{
    $1
}''',
		Key6: '',
		Key7: '',
		Key8: '',
	},

	10005: {
		Key0: 10005,
		Key1: '块注释',
		Key2: '块注释',
		Key3: 'fblock',
		Key4: '''# ********************************************************************************
# $1
# ********************************************************************************''',
		Key5: '',
		Key6: '',
		Key7: '',
		Key8: '',
	},

	10006: {
		Key0: 10006,
		Key1: '标题1',
		Key2: '行注释',
		Key3: 'fa',
		Key4: '#################### $1',
		Key5: '//################### $1',
		Key6: '',
		Key7: '',
		Key8: '',
	},

	10007: {
		Key0: 10007,
		Key1: '标题2',
		Key2: '行注释',
		Key3: 'faa',
		Key4: '########## $1',
		Key5: '//########## $1',
		Key6: '',
		Key7: '',
		Key8: '',
	},

	10008: {
		Key0: 10008,
		Key1: '文件头',
		Key2: '文件头',
		Key3: 'fileheader',
		Key4: '''# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = $CURRENT_YEAR/$CURRENT_MONTH/$CURRENT_DATE $CURRENT_HOUR:$CURRENT_MINUTE:$CURRENT_SECOND

# desc: desc''',
		Key5: '',
		Key6: '''# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = $CURRENT_YEAR/$CURRENT_MONTH/$CURRENT_DATE $CURRENT_HOUR:$CURRENT_MINUTE:$CURRENT_SECOND

# desc: desc''',
		Key7: '',
		Key8: '',
	},

	10009: {
		Key0: 10009,
		Key1: '文件log',
		Key2: '文件log',
		Key3: 'filelog',
		Key4: 'logging.getLogger("myLog").info("%s", )',
		Key5: '',
		Key6: '',
		Key7: '',
		Key8: '',
	},

	10010: {
		Key0: 10010,
		Key1: 'print',
		Key2: 'print',
		Key3: 'fprint',
		Key4: 'print("xjcprint---------------$TM_FILENAME_BASE, {}".format($1))',
		Key5: 'Debug.Log("xjclog-$TM_FILENAME_BASE"$1)',
		Key6: '',
		Key7: '',
		Key8: '',
	},

	10011: {
		Key0: 10011,
		Key1: 'colorprint',
		Key2: 'colorprint',
		Key3: 'fcolorprint',
		Key4: 'Debug.Log("<color=blue>xjclog-$TM_FILENAME_BASE</color>"$1)',
		Key5: '',
		Key6: '',
		Key7: '',
		Key8: '',
	},

	10012: {
		Key0: 10012,
		Key1: 'try',
		Key2: 'try',
		Key3: 'ftry',
		Key4: '''try:
    pass
except Exception as e:
    print e''',
		Key5: '',
		Key6: '',
		Key7: '',
		Key8: '',
	},

	10013: {
		Key0: 10013,
		Key1: '遍历文件夹',
		Key2: '遍历文件夹',
		Key3: 'fwalk',
		Key4: '''for szParentPath, listDirName, listFileName in os.walk("F:/temp"):
    for szDirName in listDirName:
        szFullPath = os.path.join(szParentPath, szDirName)
        print(szFullPath)
    for szFileName in listFileName:
        szFullPath = os.path.join(szParentPath, szFileName)
        print(szFullPath)''',
		Key5: '',
		Key6: '',
		Key7: '',
		Key8: '',
	},

	10014: {
		Key0: 10014,
		Key1: 'leetcode模板',
		Key2: 'leetcode模板',
		Key3: 'fleetcodetemplate',
		Key4: '''# 思路

# 代码
class Solution:
    pass
    
# 边界
solution = Solution()
assert(solution)''',
		Key5: '',
		Key6: '',
		Key7: '',
		Key8: '',
	},

	10015: {
		Key0: 10015,
		Key1: 'main',
		Key2: 'main',
		Key3: 'fmain',
		Key4: '''if __name__ == "__main__":
    pass''',
		Key5: '',
		Key6: '',
		Key7: '',
		Key8: '',
	},

	10016: {
		Key0: 10016,
		Key1: '单元测试',
		Key2: '单元测试',
		Key3: 'funittest',
		Key4: '''import logging
import unittest


class TestXXXX(unittest.TestCase):
    def setUp(self):
        logging.getLogger("myLog").debug("TestXXXX setUp:")

    def test_FileExt(self):
        self.assertEqual(1, 1)

    def tearDown(self):
        logging.getLogger("myLog").debug("TestXXXX tearDown\r\r\r")''',
		Key5: '',
		Key6: '',
		Key7: '',
		Key8: '',
	},

	10017: {
		Key0: 10017,
		Key1: '打印对象',
		Key2: '打印对象',
		Key3: 'fprintobj',
		Key4: 'print("\r".join(["%s:%s" % item for item in .__dict__.items()]))',
		Key5: '',
		Key6: '',
		Key7: '',
		Key8: '',
	},

	10018: {
		Key0: 10018,
		Key1: 'todo',
		Key2: 'todo',
		Key3: 'ftodo',
		Key4: '# xjctodo',
		Key5: '// xjctodo',
		Key6: '// xjctodo',
		Key7: '',
		Key8: '',
	},

	10019: {
		Key0: 10019,
		Key1: '',
		Key2: '',
		Key3: '',
		Key4: '',
		Key5: '',
		Key6: '',
		Key7: '',
		Key8: '',
	},

	20001: {
		Key0: 20001,
		Key1: '时间统计',
		Key2: '时间统计',
		Key3: 'fstopwatch',
		Key4: '',
		Key5: '''System.Diagnostics.Stopwatch $1Stopwatch = new System.Diagnostics.Stopwatch();
$1Stopwatch.Start();
$1Stopwatch.Stop();''',
		Key6: '',
		Key7: '',
		Key8: '',
	},

}
