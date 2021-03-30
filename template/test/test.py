# import os
# import shutil
#
# dictDirHasFile = {}
# szRootFPath = "C:/Users/gzxiejinchun/Desktop/a"
# dictDirHasFile[szRootFPath] = True
# nLenRootFPath = len(szRootFPath)
#
# dictDirToDel = []
#
# for szParentFPath, _, listFileName in os.walk(szRootFPath):
#     if len(listFileName) != 0:  # 空文件夹
#         szParentRPath = szParentFPath[nLenRootFPath + 1:]
#         szParentRPath = szParentRPath.replace("\\", "/")
#         listDirName = szParentRPath.split("/")
#
#         szCurFPath = szRootFPath
#         for nIndex in range(0, len(listDirName)):
#             szCurFPath += "/" + listDirName[nIndex]
#             if szCurFPath not in dictDirHasFile:
#                 dictDirHasFile[szCurFPath] = True
#
# for szParentFPath, listDirName, listFileName in os.walk(szRootFPath):
#     szParentFPath = szParentFPath.replace("\\", "/")
#     if szParentFPath not in dictDirHasFile:
#         dictDirToDel.append(szParentFPath)
#
# for szPath in dictDirToDel:
#     if os.path.exists(szPath):
#         shutil.rmtree(szPath)
#
#

from jinja2 import Template

TemplateObj = Template("{{fpath1}} input {{fpath2}} out {{fpath3}}")
dictConfig = {}
dictConfig["fpath1"] = "1.exe"
dictConfig["fpath2"] = "2.png"
dictConfig["fpath3"] = "3.png"
szContent = TemplateObj.render(dictConfig)
print(szContent)

szCommand = "{{exe_fpath}} {{tga_file}} {{temp_dir}}  -s fast -c etc2 -f RGBA -ktx"

VarDict = {
    "exe_fpath": {
        "type": "file",
        "iot": "input",
        "fpath": "E:/project/xiewendan/tools/template/data/test/etcpack.exe",
        "md5": "24fd208ed546eaad8a8c5ec5528391d2",
        "size": 378880,
        "filename": "etcpack.exe"
    },
    "tga_file": {
        "type": "file",
        "iot": "input",
        "fpath": "E:/project/xiewendan/tools/template/data/test/cqs_ground_06.tga",
        "md5": "7fa8ab3da449c511da5aac832440c923",
        "size": 524332,
        "filename": "cqs_ground_06.tga",
    },
    "temp_dir": {
        "type": "dir",
        "iot": "temp",
        "fpath": "E:/project/xiewendan/tools/template/data/test/cqs_ground_06.ktx",
        "md5": "",
        "size": 0,
    },
    "ktx_file": {
        "type": "file",
        "iot": "output",
        "fpath": "E:/project/xiewendan/tools/template/data/test/cqs_ground_06.ktx/cqs_ground_06.ktx",
        "md5": "",
        "size": 0,
        "filename": "cqs_ground_06.ktx"
    }
}

import uuid
print(uuid.uuid1())
