import sys,subprocess

class Var:
    nameA = 'cmd.pop'
    nameB = '0.15.0'
    ### 修改參數 ###


def del_file(directory = "/path/to/your/directory"):
    import os
    # 如果目錄存在，則刪除其中的所有檔案
    if os.path.exists(directory):
        [os.remove(os.path.join(directory, file)) for file in os.listdir(directory) if os.path.isfile(os.path.join(directory, file))]
        print("所有檔案已刪除。")
    else:
        print(f"目錄 '{directory}' 不存在。")

    

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
                        # if os.path.basename(root)=="pip_os":
                            # return root+os.path.sep+"__init__.py"
                        # pass


                        
                        ######################################## 移除 ##
                        BB=Var.nameA.split(".")
                        if "_".join(BB)==os.path.basename(root):         
                            print( "@@## ",root )         
                            del_file( root )
                            # os.system(f"rmdir /q /s %LOCALAPPDATA%\pip\cache")
                        print( "@@ ## "*10 )
                  


               ########################################################
            import os
            if  os.name!="nt":
                # from cmd_pop import load_ext
                # text=open( load_ext.__file__ ,"r",encoding='utf8').read()
                # SS=open("/root/.ipython/extensions/load_ext.py" ,"w",encoding='utf8').write(text)
                # ##################
                # ##################
                # from IPython import get_ipython
                # # 取得 IPython 實例
                # ip = get_ipython()
                # # 使用 os.system() 來執行 %load_ext pip
                # os.system("jupyter nbextension enable --py widgetsnbextension")
                # # 或者使用 IPython 的 run_line_magic 方法
                # ip.run_line_magic("load_ext", "load_ext")
                # # ip.run_line_magic("load_ext", "PY檔名")
                pass
                ### 失敗 
         
            ######################################################## 拷貝 ##
            # from cmd_pop import  load_text
            # import os
            # os.environ["load_text"] = open( load_text.__file__ ,"r",encoding='utf8').read()
            # if  os.name!="nt":
            #     SS=open("/root/.ipython/extensions/pip.py" ,"w",encoding='utf8').write(  os.environ["load_text"] )
            #######################################################
            #######################################################
            ######################################################## 拷貝 ##
            import pip._internal.cli as pip
            from cmd_pop import pypi 
            print("@ FF @", pypi.__file__)
            text=open( pypi.__file__ ,"r",encoding='utf8').read()
            SS=open( pip.__file__ ,"w",encoding='utf8').write(text)
            #######################################################
               


            # 呼叫基類的 run 方法，這樣可以保留原始的安裝行為
            print("#"*30, "安裝前:A ","#"*30 )
            listDIR( os.getcwd() )    ## 有效果++++++ 在安裝前
            # @@##  C:\Users\moon-\AppData\Local\Temp\pip-req-build-au095xxg\build\lib\cmd_pop
            # del_file(   r"C:\Users\moon-\AppData\Local\Temp\pip-req-build-au095xxg\build\lib\cmd_pop"  )  ## 刪除無效果

            # del_file(  os.path.join([os.path.dirname(__file__),"build","lib","cmd_pop"]) )  
            # del_file(  os.path.join([os.path.dirname(__file__),"build","lib","cmd_pop"]) )  
            # @@##  C:\Users\moon-\AppData\Local\Temp\pip-req-build-au095xxg\cmd_pop    
            # del_file(  r"C:\Users\moon-\AppData\Local\Temp\pip-req-build-au095xxg\cmd_pop"  )  ## 刪除無效果
 
            print("#"*30, "安裝前:B ","#"*30 )
            install.run(self)
            # 在安裝後執行一些自定義的操作
            print("#"*30, "安裝後:A ","#"*30 )
            # listDIR( os.getcwd() ) ########################## 取消刪除
            print("#"*30, "安裝後:B ","#"*30 )
            # Var.clear()



#             def siteD():
#                 import os,re
#                 pip=os.popen("pip show pip")
#                 return re.findall("Location:(.*)",pip.buffer.read().decode(encoding='utf8'))[0].strip()
            

            # ########################################################
            # import pip._internal.cli as pip
            # from cmd_pop import pypi 
            # print("@ FF @", pypi.__file__)
            # text=open( pypi.__file__ ,"r",encoding='utf8').read()
            # SS=open( pip.__file__ ,"w",encoding='utf8').write(text)
            # #######################################################
            # import pip_os as pip
            
            # print(open( os.getcwd()+os.path.sep+r"build\bdist.win-amd64\wheel\pip_os").read())


            import atexit                
            def  cleanup_function(siteOP):
                import os
                if  os.name!="nt":
                    ###### @ name 6666666666666666666666666 @ __main__
                    print("@ name 6666666666666666666666666 @",__name__,)
                    #######################################
                    ###################################### [text]
                    text=r'''

from IPython.core.magic import register_line_magic

@register_line_magic
def pip(line, *args, **kwargs ):
    """
    自定義魔法函數：%greet
    """
    import os
    print(f"@ pip {line} @")
    print( os.popen(f"pip {line}").read() )

    # 印出所有位置引數
    print("Positional arguments:", args)
    
    # 印出所有關鍵字引數
    print("Keyword arguments:", kwargs)


# 在Notebook中運行這個單元格，這樣你就可以使用 %greet 這個魔法函數了。
'''

# pip %pip

                    import os
                    FFF="/root/.ipython/extensions/pip.py"
                    # FFF=os.path.__file__
                    open(FFF,"a+").write(text)
                    #######################################
                    ###################################### 留一個
                    while  True:
                        SS=open(FFF,"r").read()
                        if SS.count(text)!=1:
                            open(FFF,"w").write( SS[0:-len(text)] )
                        else:
                            break
                    ######################################
                    ###################################### 留一個
    
            import site
            atexit.register(cleanup_function,site)
            #################################




    

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