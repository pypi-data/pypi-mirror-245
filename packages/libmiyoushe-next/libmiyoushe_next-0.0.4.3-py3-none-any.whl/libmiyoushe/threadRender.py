"""
将文章的部分内容（表情包、指向米游社的部分链接）进行替换
"""
import json
import re
from delta import html

from . import replace_regex


def replaceAllFromDelta(contents: list | str, emotionDict: dict, customReplaceList: list[list[str, str]] = None):
    """
    将表情包文本进行转义
    :param customReplaceList: 自定义替换样式列表，[正则表达式，要替换内容的模板（内容使用{}占位）]
    :param contents: 结构化文章内容
    :param emotionDict: 表情包集合
    :return:
    """
    if type(contents) is str:
        contents = json.loads(contents)

    return replaceAll(html.render(contents), emotionDict, customReplaceList)


def replaceAll(contents: str, emotionDict: dict, customReplaceList: list[list[str, str]] = None):
    """
    将文章的部分内容（表情包、指向米游社的部分链接）进行替换
    :param customReplaceList: 自定义替换样式列表，[正则表达式，要替换内容的模板（内容使用{}占位）]
    :param contents: 文章内容
    :param emotionDict: 表情包集合
    :return:
    """
    contents = re.sub(r"_\((.*?)\)",
                      lambda m: '<img class="emoticon-image emotionIcon" src="{}">'.format(emotionDict[m.group(1)]),
                      contents)
    if customReplaceList is not None:
        for item in customReplaceList:
            contents = re.sub(item[0], lambda m: item[1].format(m.group(1)), contents)
    return contents
