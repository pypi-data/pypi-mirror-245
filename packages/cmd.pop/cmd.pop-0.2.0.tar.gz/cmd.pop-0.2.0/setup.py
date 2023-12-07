
##############################################
from setuptools import setup, find_packages
setup(
    name="cmd.pop",
    # name=f"cmd.oss",
    version="0.2.0",
    description="笨貓魔法",
    long_description="""喵!\n喵!\n喵!\n""",
    long_description_content_type="text/markdown",
    license="LGPL",
    # packages=find_packages(),
    install_requires=[
    # setup_requires=[
       "cmd.os@https://gitlab.com/moon-0516/cmd.os"
    #     # 'BAT.oss@git+https://gitlab.com/moon-0516/AT.bat',
    ],
    # dependency_links=[
    #   'git+https://gitlab.com/moon-0516/cmd.os#egg=cmd.os'
    # ],
    #####################################
    # cmdclass={ 'install': PostCMD  }
    #####################################
)
