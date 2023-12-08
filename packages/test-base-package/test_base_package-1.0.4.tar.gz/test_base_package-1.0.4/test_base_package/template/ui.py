# -*- coding: utf-8 -*-

conftest_template = '''# -*- coding: utf-8 -*-
import allure
import os

import pytest

from playwright.sync_api import sync_playwright, Playwright

from test_base_package.ui.base_page import BasePage
from test_base_package.utils import sys_util, time_util
from test_base_package.utils.logger import logger


@pytest.fixture(scope='session')
def playwright(request):
    base_url = request.config.getoption('base_url')

    if not base_url:
        logger.error("config.ini 文件中没有设置base_url参数")
        raise "config.ini 文件中没有设置base_url参数"
    with sync_playwright() as playwright:
        yield playwright


@pytest.fixture(scope='module')
def browser(playwright):
    browser = playwright.chromium.launch(headless=False)
    yield browser
    browser.close()


@pytest.fixture()
def context(browser):
    context = browser.new_context()
    yield context


@pytest.fixture()
def page(context):
    new_page = context.new_page()
    page = BasePage(new_page)
    yield page
    page.close()


@pytest.fixture()
def login():
    pass


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    root_dir = sys_util.get_base_dir()
    outcome = yield
    report = outcome.get_result()  # rep可以拿到用例的执行结果详情

    if report.when == 'call' and report.failed:

        screenshot_dir = os.path.join(root_dir, "screenshots")  # 拼接文件夹目录

        if not sys_util.is_dir_exists(screenshot_dir):  # 判断文件是否存在，不存在则创建
            sys_util.create_dir(screenshot_dir)

        image_file_name = '{}.png'.format(time_util.current_date("%Y%m%d%H%M%S"))
        image_file_path = os.path.join(screenshot_dir, "images", image_file_name)

        if sys_util.is_file_exists(image_file_path):
            return report

        item.funcargs['page'].screenshot(path=image_file_path)

        with open(image_file_path, "rb") as f:
            allure.attach(
                name='失败截图',
                body=f.read(),
                attachment_type=allure.attachment_type.PNG
            )
    return report

'''

requirements_template = """
allure-pytest==2.13.2
playwright==1.37.0
pytest-base-url==2.0.0
test-base-package
"""
