# -*- coding: utf-8 -*-

Key0 = 'ID'
Key1 = 'name'
Key2 = 'desc'
Key3 = 'prefix'
Key4 = 'cpp'
Key5 = 'python'
Key6 = 'csharp'
Key7 = 'go'
Key8 = 'java'

mul_lan = {

	1: {
		Key0: 1,
		Key1: 'include',
		Key2: '包含库',
		Key3: '*import',
		Key4: '#include <iostream>',
		Key5: 'import sys',
		Key6: '',
		Key7: '',
		Key8: '',
	},

	2: {
		Key0: 2,
		Key1: 'using',
		Key2: '使用namespace',
		Key3: '*using',
		Key4: 'using namespace std;',
		Key5: '',
		Key6: 'using System;',
		Key7: '',
		Key8: '',
	},

	3: {
		Key0: 3,
		Key1: 'function',
		Key2: '定义函数',
		Key3: '*fun',
		Key4: '''int main()
{
    cout << "Hello World\r"; 
    return 0;
}''',
		Key5: '''def Main():
    print("Hello World\r")

''',
		Key6: '''static void Main(string[] args)
{
        System.Console.WriteLine("Hello World\r");
}''',
		Key7: '',
		Key8: '',
	},

}
