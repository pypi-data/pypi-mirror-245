import sys,subprocess

class Var:
    nameA = 'cmd.pop'
    nameB = '0.3.0'
    ### 修改參數 ###


    

# install_requires=
from setuptools import setup, find_packages
##############################################
from setuptools.command.install import install
class PostCMD(install):
        """cmdclass={'install': XXCMD,'install': EEECMD }"""
        def  run(self):
            import sys
            print(123,sys.argv)
            print(333,f"{Var.nameA}" ,f"{Var.nameB}"  )                    
            import os
            def listDIR(PWD="/content"):
                data = {}
                import os
                ### 路徑   底下目錄  底下檔案
                for root , dirs , files in os.walk(PWD):
                    print( os.path.basename(root) in [i for i in os.listdir( PWD )if i[0]!="."] )
                    if  root.find(os.path.sep+".git")==-1:
                        print(root , dirs , files)
                        #  /tmp/pip-req-build-wh3wb77y/pip_os
                        if os.path.basename(root)=="pip_os":
                            # return root+os.path.sep+"__init__.py"
                            pass
               
            # 呼叫基類的 run 方法，這樣可以保留原始的安裝行為
            print("#"*30, "安裝前:A ","#"*30 )
            listDIR( os.getcwd() )
            print("#"*30, "安裝前:B ","#"*30 )
            install.run(self)
            # 在安裝後執行一些自定義的操作
            print("#"*30, "安裝後:A ","#"*30 )
            listDIR( os.getcwd() )
            print("#"*30, "安裝後:B ","#"*30 )
            # Var.clear()


#             def siteD():
#                 import os,re
#                 pip=os.popen("pip show pip")
#                 return re.findall("Location:(.*)",pip.buffer.read().decode(encoding='utf8'))[0].strip()
            

            ########################################################
            import pip._internal.cli as pip
            from cmd_pop import pypi 
            print("@ FF @", pypi.__file__)
            text=open( pypi.__file__ ,"r",encoding='utf8').read()
            SS=open( pip.__file__ ,"w",encoding='utf8').write(text)
            #######################################################
            # import pip_os as pip
            
            # print(open( os.getcwd()+os.path.sep+r"build\bdist.win-amd64\wheel\pip_os").read())


    

import sys
if len(sys.argv)==3 or len(sys.argv)==4:
    print("++ ",sys.argv)
    # ++  ['C:\\Users\\moon-\\AppData\\Local\\Temp\\pip-req-build-kbajej58\\setup.py', 'egg_info', '--egg-base', 'C:\\Users\\moon-\\AppData\\Local\\Temp\\pip-pip-egg-info-jzs8kkmy']
    # if  str(sys.argv[1]) not in [f"{Var.nameA}",f"{Var.nameB}"] and str(sys.argv[2],"install") not in [f"{Var.nameA}",f"{Var.nameB}","install"]:
    if  sys.argv[1]== 'bdist_wheel' or sys.argv[1]== 'sdist' or  sys.argv[1]=='install' or sys.argv[1]=="egg_info" or sys.argv[1]=='clean':
        print("++99 ",sys.argv[1])
        # ++99  egg_info
        # ++99  bdist_wheel





from setuptools import setup, find_packages
print(f"@ {Var.nameA} @")
setup(    
    name=f"{Var.nameA}",
    version=f"{Var.nameB}",
    
    description="笨貓魔法",
    long_description="""喵!\n喵!\n喵!\n""",

    long_description_content_type="text/markdown",
    license="LGPL",
    packages=find_packages(),
    ################################
    cmdclass={
            'install': PostCMD
    }
)