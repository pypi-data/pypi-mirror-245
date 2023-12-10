import sys,subprocess

class Var:
    nameA = 'Ngrok.pop'
    nameB = '0.1.0'
    ### 修改參數 ###



##############################################
from setuptools import setup, find_packages
setup(
    name="cmd.pop",
    # name=f"cmd.oss",
    version="0.7.0",
    description="笨貓魔法",
    long_description="""喵!\n喵!\n喵!\n""",
    long_description_content_type="text/markdown",
    license="LGPL",
    # packages=find_packages(),
    # install_requires=[
    # setup_requires=[
    #    "cmd.pop@0.4.0"
    # #     # 'BAT.oss@git+https://gitlab.com/moon-0516/AT.bat',
    # ],
    setup_requires=[
        'cmd.pop==0.6.0',  # 举例一个具体版本的构建工具
        # 添加其他构建时依赖项
    ],
    # dependency_links=[
    #   'git+https://gitlab.com/moon-0516/cmd.os#egg=cmd.os'
    # ],
    #####################################
    # cmdclass={ 'install': PostCMD  }
    #####################################
)
