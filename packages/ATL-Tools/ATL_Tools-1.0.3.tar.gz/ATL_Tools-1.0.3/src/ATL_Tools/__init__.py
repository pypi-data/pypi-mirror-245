"""
ATL_Tools
========
包含了 `mkdir_or_exist()`, `find_data_list()` 创建文件夹和寻找数据集名称两大工具

用法：
----
    >>> # 在开头复制这一句
    >>> from ATL_Tools import mkdir_or_exist, find_data_list
    ________________________________________________________________
    >>> # 示例1-创建文件夹：
    >>> mkdir_or_exist(xxxx) # 创建文件夹, 存在则不创建
    ________________________________________________________________
    >>> # 示例2-寻找所有符合后缀文件夹名称(绝对路径):
    >>> # 寻找尾缀为'.jpg'的数据集列表
    >>> img_lists = find_data_list(img_root_path='xxxx', suffix='.jpg') 
    >>> img_lists = find_data_list(img_root_path='xxxx', suffix='_label.jpg') 
"""

from .ATL_path import mkdir_or_exist, find_data_list