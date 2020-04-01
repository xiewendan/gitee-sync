import os
import shutil


def main():
    szProjectPath = input("请输入项目名：")
    szProjectPath = "tool/" + szProjectPath

    if os.path.exists(szProjectPath):
        print("Error: 项目名已存在")
        return

    szTemplatePath = "template"
    shutil.copytree(szTemplatePath, szProjectPath)


if __name__ == '__main__':
    main()
