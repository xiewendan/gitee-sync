# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2020/4/18 8:58 下午

# desc: 

import os
import re
import logging
import xlrd

import common.git_util as git_util
import common.my_exception as my_exception
import common.my_path as my_path
import main_frame.cmd_base as cmd_base
import common.my_log as my_log


class CmdExcel2Py(cmd_base.CmdBase):
    def __init__(self):
        super().__init__()

        self.m_LoggerObj = my_log.MyLog(__file__)

    @staticmethod
    def GetName():
        return "excel2py"

    def Do(self):
        self.m_LoggerObj.info("Start DoExcel2Py")

        szCWD = self.m_AppObj.ConfigLoader.CWD

        szExcelPath = self.m_AppObj.CLM.GetArg(1)
        szSettingPath = self.m_AppObj.CLM.GetArg(2)
        self.m_LoggerObj.info("DoExcel2Py! ExcelPath:%s, SettingPath:%s", szExcelPath, szSettingPath)

        szExcelFullPath = os.path.join(szCWD, szExcelPath)
        szSettingFullPath = os.path.join(szCWD, szSettingPath)
        self.m_LoggerObj.info("DoExcel2Py! ExcelFullPath:%s, SettingFullPath:%s", szExcelFullPath, szSettingFullPath)

        # get change file
        listChangeFile = git_util.GitUtil.GetChangeFiles(os.path.join(szCWD, szExcelPath))
        self.m_LoggerObj.debug("change files:%s", str(listChangeFile))

        # filter excel file
        listExcelChangeFile = self._FilterExcelFile(listChangeFile)
        self.m_LoggerObj.debug("excel change files:%s", str(listExcelChangeFile))

        # convert
        for szExcelFile in listExcelChangeFile:
            ExcelCfgObj = ExcelCfg(os.path.join(szExcelFullPath, szExcelFile))
            szPyFileFullPath = os.path.join(szSettingFullPath, szExcelFile.replace(".xlsx", ".py"))
            ExcelCfgObj.ConvertToPy(szPyFileFullPath)

    @staticmethod
    def _FilterExcelFile(listChangeFile):
        listExcelFile = []
        for szFile in listChangeFile:
            MatchObj = re.match("^[ ?MA][ ?MA] ([0-9a-zA-Z_/]+.xlsx)$", szFile)
            if MatchObj is None:
                continue

            listExcelFile.append(MatchObj.groups()[0])

        return listExcelFile


class ExcelCfg:
    def __init__(self, szExcelFileFullPath):
        self.m_szExcelFileFullPath = szExcelFileFullPath

        self.m_listKey = []
        self.m_dictKey2Type = {}

        self.m_dictCellValue = {}  # 二维的数据结构，[ID][Key] = CellData

        # format output
        self.m_dictKey2Index = {}
        self.m_listSortID = []  # 排序后的ID

    def ConvertToPy(self, szPyFileFullPath):
        logging.getLogger("myLog").debug("ExcelFileFullPath:%s, PyFileFullPath:%s", self.m_szExcelFileFullPath,
                                         szPyFileFullPath)

        self._LoadFile()

        self._CheckType()

        self._ConvertType()

        self._SavePy(szPyFileFullPath)

    def _LoadFile(self):
        logging.getLogger("myLog").debug("")

        try:
            WorkBookObj = xlrd.open_workbook(self.m_szExcelFileFullPath)
        except FileNotFoundError as e:
            raise my_exception.MyException("Excel file not exist:" + self.m_szExcelFileFullPath + str(e))
        except xlrd.XLRDError as e:
            raise my_exception.MyException("Excel file format error:" + self.m_szExcelFileFullPath + str(e))

        listSheetName = WorkBookObj.sheet_names()
        if len(listSheetName) == 0:
            raise my_exception.MyException("Excel file has no sheet:" + self.m_szExcelFileFullPath)

        WorkSheetObj = WorkBookObj.sheet_by_name(listSheetName[0])

        self.m_listKey = []
        self.m_dictKey2Type = {}
        self.m_dictCellValue = {}  # 二维的数据结构，[ID][Key] = CellData

        for nRowIndex in range(WorkSheetObj.nrows):
            # key
            if nRowIndex == 0:
                for nColIndex in range(WorkSheetObj.ncols):
                    CellValue = WorkSheetObj.cell_value(nRowIndex, nColIndex)
                    if CellValue is None:
                        raise my_exception.MyException(
                            "%s title %s is none".format(self.m_szExcelFileFullPath, nColIndex))
                    self.m_listKey.append(CellValue)
            # type
            elif nRowIndex == 1:
                for nColIndex in range(WorkSheetObj.ncols):
                    CellValue = WorkSheetObj.cell_value(nRowIndex, nColIndex)
                    if CellValue is None:
                        raise my_exception.MyException(
                            "%s type %s is none".format(self.m_szExcelFileFullPath, nColIndex))

                    szKey = self.m_listKey[nColIndex]
                    self.m_dictKey2Type[szKey] = CellValue
            else:
                dictData = {}
                for nColIndex in range(WorkSheetObj.ncols):
                    CellValue = WorkSheetObj.cell_value(nRowIndex, nColIndex)
                    if (CellValue is None or CellValue == "") and nColIndex == 0:
                        break

                    szKey = self.m_listKey[nColIndex]
                    dictData[szKey] = CellValue

                if len(dictData):
                    ID = WorkSheetObj.cell_value(nRowIndex, 0)
                    szFileNameWithExt = my_path.FileNameWithExt(self.m_szExcelFileFullPath)
                    assert ID is not None, "check"
                    if ID in self.m_dictCellValue:
                        szError = "key 冲突:{0}, table name:{1}, Row:{2}".format(ID, szFileNameWithExt, nRowIndex)
                        assert False, szError
                    self.m_dictCellValue[ID] = dictData

    def _CheckType(self):
        for szID, dictData in self.m_dictCellValue.items():
            for szKey, CellValue in dictData.items():
                szType = self.m_dictKey2Type[szKey]

                szError = self._CheckValueType(CellValue, szType)
                if szError:
                    szFileNameWithExt = my_path.FileNameWithExt(self.m_szExcelFileFullPath)
                    szCellValuePos = "table name:{0}, Row:{1}, Col:{2}".format(szFileNameWithExt, szID, szKey)
                    assert False, "{0} {1}".format(szError, szCellValuePos)

    @staticmethod
    def _CheckValueType(CellValue, szType):
        dictTypeStr2Type = {"int": (int, float),
                            "str": (str,),
                            "float": (float, int),
                            "num": (float, int),
                            "bool": (bool,)}
        if CellValue == "":
            return ""

        if szType in ("all", "str"):
            return ""

        if type(CellValue) == str and CellValue not in ("True", "False"):
            szCellValue = CellValue.encode("UTF-8")
        else:
            szCellValue = CellValue

        if szType in dictTypeStr2Type:
            if type(eval(str(szCellValue))) in dictTypeStr2Type[szType]:
                return ""
            else:
                return "type error, col type is {0}, but the value is {1}({2}).".format(szType, CellValue,
                                                                                        type(CellValue))

        elif szType[:5] == "list-":
            szListEleType = szType[6:]
            listCellValue = eval(str(szCellValue))
            if not isinstance(listCellValue, list):
                return "type error, col type is list."

            if szListEleType == "*":
                return ""
            else:
                for EleObj in listCellValue:
                    if ExcelCfg._CheckValueType(EleObj, szListEleType):
                        return "list element type error, col type is {0}.".format(szType)

        elif szType[:5] == "dict-":
            szDictType = szType[6:]
            szDictKeyType, szDictValueType = szDictType.split(':')

            dictCellValue = eval(str(szCellValue))
            if not isinstance(dictCellValue, dict):
                return "type error, col type is dict."

            if szDictKeyType not in ("*", "str"):
                for szDictKey in dictCellValue.keys():
                    if ExcelCfg._CheckValueType(szDictKey, szDictKeyType):
                        return "dict key type error. col type is {0}.".format(szType)

            if szDictValueType != "*":
                for szDictValue in dictCellValue.values():
                    if ExcelCfg._CheckValueType(szDictValue, szDictValueType):
                        return "dict value type error. col type is {0}.".format(szType)

        return ""

    def _ConvertType(self):
        dictCellValue = {}
        for szID, dictData in self.m_dictCellValue.items():
            szIDType = self.m_dictKey2Type[self.m_listKey[0]]
            szNewID = self._ConvertValueType(szID, szIDType)
            dictCellValue[szNewID] = {}

            for szKey, CellValue in dictData.items():
                szType = self.m_dictKey2Type[szKey]
                if szID == 513008 and szKey == "cn":
                    print("xjc")
                NewCellValue = self._ConvertValueType(CellValue, szType)
                dictCellValue[szNewID][szKey] = NewCellValue

        self.m_dictCellValue = dictCellValue

    @staticmethod
    def _ConvertValueType(CellValue, szType):
        if szType in ("all", "str", "bytes"):
            if type(CellValue) in (str, bytes):
                return CellValue.replace("\n", "\\n")
            else:
                return CellValue

        if CellValue == "":
            dictTypeStr2EmptyValue = {"int": 0,
                                      "float": 0,
                                      "str": "",
                                      "num": 0,
                                      "bool": False,
                                      }

            if szType in dictTypeStr2EmptyValue:
                return dictTypeStr2EmptyValue[szType]
            elif szType[:4] == "list":
                return []
            elif szType[:4] == "dict":
                return {}
            else:
                return ""

        dictTypeStr2Type = {"int": int,
                            "float": float,
                            "str": str,
                            "num": float,
                            "bool": bool
                            }
        if szType in dictTypeStr2Type:
            return dictTypeStr2Type[szType](CellValue)

        elif szType[:4] == "list":
            return CellValue

        elif szType[:4] == "dict":
            return CellValue
        else:
            assert False, "Value:{1}, unknown type:{0}".format(CellValue, szType)

    def _SavePy(self, szPyFileFullPath):
        szFileName = my_path.FileName(szPyFileFullPath)

        # format
        self._FormatOutput()

        listOutputLine = ["# -*- coding: utf-8 -*-\n\n"]

        for szKey in self.m_listKey:
            szKeyVarName = self._GetKeyVarName(szKey)
            listOutputLine.append("{0} = {1}\n".format(szKeyVarName, self._ChangeToString(szKey)))

        listOutputLine.append("\n")
        listOutputLine.append("{0} = {{\n".format(szFileName))

        listOutputLine.append("\n")
        for szID in self.m_listSortID:
            listOutputLine.append('\t{0}: {{\n'.format(self._ChangeToString(szID)))
            dictRowData = self.m_dictCellValue[szID]

            for szKey, szValue in dictRowData.items():
                listOutputLine.append(
                    "\t\t{0}: {1},\n".format(self._GetKeyVarName(szKey),
                                             self._ChangeToString(szValue)))

            listOutputLine.append('\t}},\n\n'.format(self._ChangeToString(szID)))

        listOutputLine.append("}}\n".format(szFileName))

        # file
        my_path.CreateFileDir(szPyFileFullPath)
        with open(szPyFileFullPath, "w", encoding="utf-8") as fp:
            fp.writelines(listOutputLine)

    def _FormatOutput(self):
        self.m_dictKey2Index = {}
        for nIndex, szKey in enumerate(self.m_listKey):
            self.m_dictKey2Index[szKey] = nIndex

        listID = list(self.m_dictCellValue.keys())
        listID.sort()
        self.m_listSortID = listID

    def _GetKeyVarName(self, szKey):
        nIndex = self.m_dictKey2Index[szKey]
        return "Key{0}".format(nIndex)

    @staticmethod
    def _ChangeToString(data):
        if type(data) in (int, float, bool, list, dict, tuple):
            return ExcelCfg._StringObj(data)
        szNewData = "'" + data + "'"
        return szNewData

    @staticmethod
    def _StringObj(data):
        szResult = ""
        if type(data) in (int, float, str):
            return str(data)
        elif isinstance(data, dict):
            szResult = ""
            for k, v in data.items():
                szResult += ExcelCfg._CheckToString(k)

                szResult += ":"
                szResult += ExcelCfg._CheckToString(v)
                szResult += ","
            szResult = "{" + szResult + "}"
        elif isinstance(data, list):
            szResult = ""
            for k in data:
                szResult += ExcelCfg._CheckToString(k)
                szResult += ","
            szResult = "[" + szResult + "]"
        elif isinstance(data, tuple):
            szResult = ""
            for k in data:
                szResult += ExcelCfg._CheckToString(k)
                szResult += ","
            szResult = "(" + szResult + ")"

        return szResult

    @staticmethod
    def _CheckToString(strobj):
        if isinstance(strobj, str):
            return "{}".format("\"" + strobj + "\"")
        else:
            return "{}".format(strobj)
