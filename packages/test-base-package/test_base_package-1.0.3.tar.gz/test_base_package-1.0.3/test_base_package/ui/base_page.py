# -*- coding:utf-8 -*-
from playwright.sync_api import expect, Page, Locator

from test_base_package.common.plugin import exception_plugin
from test_base_package.ui.build_in_library import BuildInLibrary
from test_base_package.utils.logger import logger


class BasePage:
    """
    继承原始page类
    """

    def __init__(self, page: Page):
        self.page = page

    def goto(self, url):

        self.page.goto(url=url)

    def title(self) -> str:
        """
        获取网页标题
        :return:
        """
        self.page.title()
        return self.page.title()

    @exception_plugin
    def query_selector(self, locator: str, frame_locator=None) -> "BasePage":
        """
        判断元素是否存在
        :param locator:
        :param frame_locator:
        :return:
        """
        if self.page.query_selector(locator) is None:
            err_msg = "页面元素不存在:%s" % locator
            logger.error(err_msg)
            raise err_msg

        if frame_locator is not None:
            if self.page.query_selector(frame_locator) is None:
                err_msg = "页面frame元素不存在:%s" % locator
                logger.error(err_msg)
                raise err_msg
            return self.page.frame_locator(frame_locator).query_selector(locator)

        return self.page.query_selector(locator)

    def get_by_text(self, locator: str, frame_locator=None, exact=bool) -> "BasePage":
        """
        根据text文本获取
        :param text:
        :param frame_locator:
        :param exact:
        :return:
        """
        if frame_locator is not None:
            return self.page.frame_locator(frame_locator).get_by_text(text, exact=exact)

        return self.page.get_by_text(locator, exact=exact)

    def get_by_placeholder(self, locator: str, frame_locator=None, exact=bool) -> "BasePage":
        """
        根据placeholder字符获取
        :param text:
        :param frame_locator:
        :param exact:
        :return:
        """
        if frame_locator is not None:
            return self.page.frame_locator(frame_locator).get_by_placeholder(text, exact=exact)

        return self.page.get_by_placeholder(text, exact=exact)

    def get_by_title(self, locator: str, frame_locator=None, exact=bool) -> "BasePage":
        """
        根据title文本获取
        :param text:
        :param frame_locator:
        :param exact:
        :return:
        """
        if frame_locator is not None:
            return self.page.frame_locator(frame_locator).get_by_title(text, exact=exact)

        return self.page.get_by_title(text, exact=exact)

    def get_by_label(self, locator: str, frame_locator=None, exact=bool) -> "BasePage":
        """
        根据label文本获取
        :param text:
        :param frame_locator:
        :param exact:
        :return:
        """
        if frame_locator is not None:
            return self.page.frame_locator(frame_locator).get_by_label(text, exact=exact)
        return self.page.get_by_label(text, exact=exact)

    def get_by_alt_text(self, locator: str, frame_locator=None, exact=bool) -> "BasePage":
        """
        根据alt_text文本获取
        :param text:
        :param frame_locator:
        :param exact:
        :return:
        """
        if frame_locator is not None:
            return self.page.frame_locator(frame_locator).get_by_alt_text(text, exact=exact)
        return self.page.get_by_alt_text(text, exact=exact)

    @exception_plugin
    def click(self, locator: str, frame_locator=None):
        """
        点击元素
        :param locator: 传入元素定位器
        :param frame_locator: 传入frame框架的的定位器，如果没有传入，则一般点击
        :return:
        """
        if frame_locator is not None:
            self.page.frame_locator(frame_locator).locator(locator).click()

        self.page.click(locator)

    def hover(self, locator: str, frame_locator=None):
        """
        点击元素
        :param locator: 传入元素定位器
        :param frame_locator: 传入frame框架的的定位器，如果没有传入，则一般点击
        :return:
        """

        if frame_locator is not None:
            self.frame_locator(frame_locator).locator(locator).hover()

        self.page.hover(locator)

    @exception_plugin
    def fill(self, locator: str, value, frame_locator=None):
        """
        定位元素，输入内容
        :param locator:传入元素定位器
        :param value:传入输入的值
        :param frame_locator: 传入frame框架
        :return:
        """

        value = BuildInLibrary().repalce_parameter(value)

        if frame_locator is not None:
            self.page.frame_locator(selector=frame_locator).locator(selector_or_locator=locator).fill(value)

        self.page.fill(selector=locator, value=value)

    def type(self, locator: str, value, frame_locator=None):
        """
        模拟人工输入，一个键一个键的输入
        :param locator:传入元素定位器
        :param value:传入输入的值
        :param frame_locator: 传入frame框架
        :return:
        """
        value = BuildInLibrary().repalce_parameter(value)

        if frame_locator is not None:
            self.page.frame_locator(selector=frame_locator).locator(selector_or_locator=locator).type(text=value,
                                                                                                      delay=100)
        self.page.type(selector=locator, text=value, delay=100)

    def file(self, locator: str, files, frame_locator=None):
        """
        上传文件的方法
        :param locator: 定位器
        :param files: 单个文件名，或者列表存放多个文件
        :param frame_locator: iframe框架定位器，如果没有就不传
        :return:
        """

        if frame_locator is not None:
            self.page.frame_locator(frame_locator).locator(locator).set_input_files(files=files)

        self.page.locator(locator).set_input_files(files=files)

    def ele_to_be_visible(self, locator: str):
        """断言元素可见"""
        return expect(self.page.locator(locator)).to_be_visible()

    def ele_to_be_visible_force(self, locator: str, frame_locator=None, timout: int = 5):
        """强制等待某个元素可见"""
        ele = None
        if frame_locator is not None:
            ele = self.page.frame_locator(frame_locator).locator(locator)
        else:
            ele = self.page.locator(locator)
        for t in range(0, timout):
            self.page.wait_for_timeout(500)
            if ele.is_visible():
                break
        else:
            logger.warning("%s:元素未找到!" % locator)
            raise Exception("元素未找到!")

    def ele_is_checked(self, locator: str):
        """判断元素是否被选选中"""
        return self.page.is_checked(selector)

    def browser_operation(self, reload=False, forward=False, back=False):
        """浏览器操作，reload 刷新，forward 前进，back 后退"""
        if reload:
            self.page.reload()
        if back:
            self.page.go_back()
        if forward:
            self.page.go_forward()

    def screenshot(self, path, full_page=True, locator=None):
        """截图功能，默认截取全屏，如果传入定位器表示截取元素"""
        if locator is not None:
            self.page.locator(locator).screenshot(path=path)
            return path
        self.page.screenshot(path=path, full_page=full_page)
        return path
