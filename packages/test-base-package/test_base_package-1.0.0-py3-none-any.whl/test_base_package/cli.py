# -*- coding: utf-8 -*-
import argparse

from test_base_package.utils import sys_util

from test_base_package.template.ui import (
    conftest_template,
    requirements_template
)
from test_base_package.template.public import (
    init_template,
    config_template,
    pytest_template,
    runner_template,
)


def main():
    parser = argparse.ArgumentParser(description='A command-line tool.')
    parser.add_argument('project_name', help='项目名称为必填项')
    parser.add_argument('project_type', type=int, default=1, choices=[1, 2], help='测试用例类型:\n'
                                                                                  '1、ui自动化测试。\n'
                                                                                  '2、api自动化测试。')
    parser.add_argument('--case_name', type=str, help='测试用例模块为选填项')

    args = parser.parse_args()

    if args.project_type == 2:
        # TODO 初始化api项目方法暂未实现l
        pass

    init_ui_project(args.project_name)


def init_ui_project(project_name: str):
    """
    初始化测试项目
    :param project_name:
    :return:
    """
    base_dir = sys_util.join_path(sys_util.get_base_dir(), project_name)

    # 测试用例文件夹路径
    cases_dir_path = sys_util.join_path(base_dir, "cases")

    sys_util.create_file(sys_util.join_path(cases_dir_path, "__init__.py"))
    # 测试用例文件夹路径
    sys_util.create_dir(sys_util.join_path(base_dir, "logs"))

    pages_dir_path = sys_util.join_path(base_dir, "pages")

    sys_util.create_file(sys_util.join_path(pages_dir_path, "__init__.py"))

    sys_util.create_dir(sys_util.join_path(base_dir, "screenshots"))

    project_init_file = sys_util.join_path(base_dir, "__init__.py")

    # 初始化项目__init__.py文件
    with open(project_init_file, "w", encoding="utf-8") as f:
        f.write(init_template)

    # 初始化项目config.py文件
    project_config_file = sys_util.join_path(base_dir, "config.py")

    with open(project_config_file, "w", encoding="utf-8") as f:
        f.write(config_template)

    # 初始化项目conftest.py文件
    project_conftest_file = sys_util.join_path(base_dir, "../conftest.py")

    with open(project_conftest_file, "w", encoding="utf-8") as f:
        f.write(conftest_template)

    # 初始化项目pytest.ini文件
    project_pytest_file = sys_util.join_path(base_dir, "pytest.ini")

    with open(project_pytest_file, "w", encoding="utf-8") as f:
        f.write(pytest_template)

    # 初始化项目requirements.txt文件
    project_requirements_file = sys_util.join_path(base_dir, "requirements.txt")

    with open(project_requirements_file, "w", encoding="utf-8") as f:
        f.write(requirements_template)

    # 初始化项目runner.py文件
    project_runner_file = sys_util.join_path(base_dir, "runner.py")

    with open(project_runner_file, "w", encoding="utf-8") as f:
        f.write(runner_template)


def init_test_case():
    pass


if __name__ == '__main__':
    main()
