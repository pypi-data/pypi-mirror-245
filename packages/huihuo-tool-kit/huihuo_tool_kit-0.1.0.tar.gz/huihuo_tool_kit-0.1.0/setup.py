from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name='huihuo_tool_kit',  # 项目名称
    description="huihuo tool kit",  # 项目描述
    url='https://github.com/hui-huo',  # 项目主页
    version='0.1.0',  # 版本
    author='huihuo',  # 作者
    # packages=['huihuo_tool_kit'],# 项目包列表
    packages=find_packages(),  # 自动查找包
    install_requires=[  # 项目依赖
        "build"
    ],
    entry_points={  # 入口点
        'console_scripts': [  # 脚本入口
            'excel2case = huihuo_tool_kit.excel_tool:ExcelTool.excel2case',  # 命令名=包名.模块名:类名.函数名
        ],
    },
    long_description=long_description,
    long_description_content_type='text/markdown'
)
