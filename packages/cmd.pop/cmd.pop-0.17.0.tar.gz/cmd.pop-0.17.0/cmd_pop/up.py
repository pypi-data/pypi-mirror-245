https://gitlab.com/moon-0516/cmd.pop@0.13.0


@classmethod
def pip_twine( cls,URL="https://gitlab.com/moon-0516/cmd.pop@0.11.0" ):
    import os
    if  os.name=="nt":
        print("條件必須[linux]環境")
    elif URL.count("@")==1:
        os.chdir("/content")
        A,B=URL.split("@")
        NU= ">nul 2>&1" if os.name=="nt" else  ">/dev/null 2>&1"
        print(f"git clone -b {B} {A} {NU}")  
        

cmd.pop
0.13.0

'cmd.pop==0.6.0', 



    

import sys
if len(sys.argv)==3 or len(sys.argv)==4:
    # print("++ ",sys.argv)
    # ++  ['C:\\Users\\moon-\\AppData\\Local\\Temp\\pip-req-build-kbajej58\\setup.py', 'egg_info', '--egg-base', 'C:\\Users\\moon-\\AppData\\Local\\Temp\\pip-pip-egg-info-jzs8kkmy']
    # if  str(sys.argv[1]) not in [f"{Var.nameA}",f"{Var.nameB}"] and str(sys.argv[2],"install") not in [f"{Var.nameA}",f"{Var.nameB}","install"]:
    if  sys.argv[1]== 'bdist_wheel' or sys.argv[1]== 'sdist' or  sys.argv[1]=='install' or sys.argv[1]=="egg_info" or sys.argv[1]=='clean':
        # print("++99 ",sys.argv[1])
        # ++99  egg_info
        # ++99  bdist_wheel
        import site
        print("@ 1 @[setup.py]--[site]:",id(site))
        import atexit                
        def     cleanup_function(siteOP):
                print("@ 2 @[setup.py]--[site]:",id(site))
                import os
                os.system("git config --global user.moon moon-0516")
        atexit.register(cleanup_function,site)
        #################################

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
