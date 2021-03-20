"""
文件缓存系统，可以将文件缓存到指定的缓存空间，当空间不足时，会自动删除最久未使用的文件

FileCacheSystemObj = FileCacheSystem("d:/data", 10 000 000 000)         # 单位为byte，这里是10G
FileCacheSystemObj.CheckExistSameFile(szMd5, szFileName, nSize)         # 判断是否存在相同的文件
FileCacheSystemObj.SaveFile(szMd5, szFileName, nSize, szSrcFPath)       # 没有的话，可以把文件存储进去
FileCacheSystemObj.UseFile(szMd5, szFileName, nSize)                    # 使用一次，返回文件路径，会更新缓存系统使用文件时间，确保后续清理流程
FileCacheSystemObj.Destroy()                                            # 销毁流程，会保持缓存系统的索引文件
"""

from .file_cache_system import FileCacheSystem

__version__ = '1.0.0'
__author__ = 'xiaobao'
__date__ = "2021/3/20 15:34"

# __all__ = file_cache_system.__all__

__all__ = ["FileCacheSystem"]
