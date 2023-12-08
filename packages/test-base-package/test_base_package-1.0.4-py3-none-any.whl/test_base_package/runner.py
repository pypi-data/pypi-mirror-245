# -*- coding: utf-8 -*-
import os
import pytest

if __name__ == '__main__':
    # 更新测试报告
    pytest.main(['-s', '-q', '--clean-alluredir', '--alluredir=allure-results'])
    os.system(r"allure generate -c -o ./allure-report")
