import os
import shutil


def main():
    szProjectPath = input("请输入项目名：")
    szProjectPath = "tool/" + szProjectPath

    if os.path.exists(szProjectPath):
        print("Error: 项目名已存在")
        return

    szTemplatePath = "template"
    listFileOrDir = [
        "bin/supervisor",
        "bin/run.bat",
        "common",
        "config/config_template.conf",
        "config/render_template.yml",
        "config/__init__.py",
        "lib",
        "logic",
        "main_frame",
        "__init__.py",
        "requirements.txt",
        ".gitignore",
    ]

    for szFileOrDir in listFileOrDir:
        szSrcFull = os.path.join(szTemplatePath, szFileOrDir)
        szDestFull = os.path.join(szProjectPath, szFileOrDir)
        assert os.path.exists(szSrcFull), "目录或文件不存在:" + szSrcFull
        print(szSrcFull)

        if os.path.isfile(szSrcFull):
            szDestDir = os.path.split(szDestFull)[0]
            if not os.path.exists(szDestDir):
                os.makedirs(szDestDir)
            shutil.copyfile(szSrcFull, szDestFull)
        else:
            shutil.copytree(szSrcFull, szDestFull)


if __name__ == '__main__':
    main()
