# -*- coding: utf-8 -*-
init_template = """# -*- coding: utf-8 -*-
from config import get_root_dir

get_root_dir()
"""

config_template = '''# -*- coding: utf-8 -*-
import os


def get_root_dir() -> str:
    """
    获取项目运行路径
    :return:
    """
    root_dir = os.environ.get("root_dir")

    if not root_dir:
        root_dir = os.path.dirname(os.path.abspath(__file__))

        os.environ["root_dir"] = root_dir
'''

pytest_template = """[pytest]
base_url = 
addopts = -vs --alluredir ./tmp/allure_results --clean-alluredir
testpaths = ./cases
python_files = test_*.py
python_classes = Test*
"""

runner_template = """# -*- coding: utf-8 -*-
import os
import pytest

if __name__ == '__main__':
    # 更新测试报告
    pytest.main(['-s', '-q', '--clean-alluredir', '--alluredir=allure-results'])
    os.system(r"allure generate -c -o ./allure-report")
"""
