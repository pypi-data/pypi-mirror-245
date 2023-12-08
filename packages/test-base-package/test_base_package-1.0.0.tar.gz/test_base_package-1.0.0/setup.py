# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

__version__ = '1.0.0'  # 版本号
requirements = open('requirements.txt').readlines()  # 依赖文件

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='test_base_package',
    version=__version__,
    author='自动化测试基础包',
    author_email='tianjincn@163.com',
    packages=find_packages(),
    python_requires='>=3.5.0',
    install_requires=requirements,  # 安装依赖
    url="https://www.baidu.com",
    description='python 自动化测试基础包',
    py_modules=['test_base_package'],
    entry_points={
        'console_scripts': [
            'testpkg = test_base_package.cli:main',
        ],
    },
    long_description=long_description,  # 指定文档文件内容
    long_description_content_type='text/markdown',
    readme_renderer="markdown",
)
