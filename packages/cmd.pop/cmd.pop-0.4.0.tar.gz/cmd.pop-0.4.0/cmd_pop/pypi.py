import sys,subprocess

class Var:
    # nameA = 'pip'
    # nameB = '0.2.0'
    ### 修改參數 ###
    @classmethod
    def update_names(cls, name=None, vvv=None):
        """
        更新
        """
        if name is not None and vvv is not None:
            cls.nameA = name
            cls.nameB = vvv
          
            print(f"已更新 nameA={cls.nameA}, nameB={cls.nameB}")
            print("-"*50)

            # 修改文件内容
            # filename = __file__   # 替换成你的脚本文件名
            with open( "setup.py" , 'r+', encoding='utf-8') as f:
                lines = f.readlines()
                for i, line in enumerate(lines):
                    if "### 修改參數 ###" in line:
                        lines[i-2] = f"    nameA = '{name}'\n"
                        lines[i-1] = f"    nameB = '{vvv}'\n"
                        break  # 找到后就退出循环
                f.seek(0)
                f.writelines(lines)
                f.truncate()
                # 刷新檔案緩衝區
                f.flush()
                f.close()
              
               ##  這邊會導致跑二次..............關掉一個
       
             
        else:
            print("未提供足够的参数")
    
    @classmethod
    def gitNAME(cls,name="name"):
        import subprocess
        # 讀取 Git 使用者名稱
        result = subprocess.run(['git', 'config', f'user.{name}'], capture_output=True, text=True)

        # 如果命令成功執行，則輸出使用者名稱
        if result.returncode == 0:
            git_user_name = result.stdout.strip()
            # print(f"Git 使用者名稱: {git_user_name}")
            return git_user_name
        else:
            # print("無法讀取 Git 使用者名稱")
            return False
    # name=gitNAME()
    # pypi=gitNAME('pypi')
    
    
def pip_api(moon="moon-start",name=""):
    token=gitNAME('api').split(":")
    token=False if len(token)==1 else token[1]
    if not token:
        return token
    ###################################
    if  not token :
        print(f"@ token {token} 不存在 @")
        os._exit(0)
    # !curl --header "PRIVATE-TOKEN: KEY" "https://gitlab.com/api/v4/projects/moon-start%2FBAT."
    import requests
    url = f"https://gitlab.com/api/v4/projects/{moon}%2F{name}"
    headers = {"PRIVATE-TOKEN": token }
    # headers = {"PRIVATE-TOKEN": "KEY"}
    response = requests.get(url, headers=headers)
    # print(response.status_code==200)
    # print(response.json())
    return response.status_code==200

def pip_tag(moon="moon-start",name=""):
    token=gitNAME('api').split(":")
    token=False if len(token)==1 else token[1]
    if not token:
        return token
    # namespace = "moon-start"
    ###################################
    if  not token :
        print(f"@ token {token} 不存在 @")
        os._exit(0)
    # !curl --header "PRIVATE-TOKEN: KEY" "https://gitlab.com/api/v4/projects/moon-start%2FBAT."
    import requests
    # url = f"https://gitlab.com/api/v4/projects/moon-start%2F{name}"
    url_tag = f"https://gitlab.com/api/v4/projects/{moon}%2F{name}/repository/tags"
    headers = {"PRIVATE-TOKEN": token }
    # headers = {"PRIVATE-TOKEN": "KEY"}
    response = requests.get(url_tag, headers=headers)
    # print(response.status_code==200)
    # print(response.json())
    # return response.status_code==200
    RR=[]
    if response.status_code == 200:
        tags_info = response.json()
        # print("Project Versions:")
        for tag in tags_info:
            # print(tag.get("name"))
            RR.append(tag.get("name"))
    # else:
        # print(f"Error getting tags: {response.status_code}")
    ## 排序
    keyIF = lambda x: tuple(map(int, x.split('.')))
    TG=sorted(RR,key=keyIF)
    return TG

def gitNAME(name="name"):
    import subprocess
    # 讀取 Git 使用者名稱
    result = subprocess.run(['git', 'config', f'user.{name}'], capture_output=True, text=True)


    # 如果命令成功執行，則輸出使用者名稱
    if result.returncode == 0:
        git_user_name = result.stdout.strip()
        # print(f"Git 使用者名稱: {git_user_name}")
        return git_user_name
    else:
        # print("無法讀取 Git 使用者名稱")
        return False
moon="moon-0516"
# moon="moon-start"
name=gitNAME()
pypi=gitNAME('api')
##########################################################
import sys,os   
if len(sys.argv)==3:
    if   sys.argv[1]=="name":
        import os
        name=str(sys.argv[2])
        os.system(f"git config --global user.name {name}")
        os._exit(0)
    elif sys.argv[1]=="api":
        import os
        KEY=str(sys.argv[2])
        ###################################################
        # if os.name=="nt":
        #     os.system("rmdir /s /q .git")
        # else:
        #     os.system("rm -rf .git")
        ###################################################
     
            # if not BBL:
            #     print("@ 重新執行 @")
            #     os._exit(0)
        if ".git"  in os.listdir(os.getcwd()):
            pypi = os.popen("git config --global user.api").read().strip()
            SA =  os.path.basename(os.popen("git remote get-url gitlab").read().strip())
            os.system(f"git remote  set-url gitlab https://{ pypi }@gitlab.com/{moon}/{SA}")
            print(f"@ [位置] @ git remote  set-url   https://{ pypi }@gitlab.com/{moon}/{SA} @")
   

        ###################################################
        os.system(f"git config --global  user.api {KEY}")
        os._exit(0)
 
if len(sys.argv)==2:
    # print("!!")
    if  sys.argv[1]=="api":
        import os
        os.system("git config --global --unset user.api")
        print("@ git config --global --unset user.api @") 
        os._exit(0)
    elif sys.argv[1]=="pop":
        import os
        dictQ={i.split("=")[0][5::] : i.split("=")[1] for i in os.popen("git config --global --list").read().split("\n")if i[0:4]=="user"}
        # if "name" in dictQ.keys():
        #   S=dictQ["name"]
        #   print(S)
        print(f"@ user: {dictQ} @")
        os._exit(0)
    elif sys.argv[1]=="init":
        import os
        NN= os.path.basename(os.getcwd()).split(".")
        if len(NN)==2:
            # 创建目录
            os.makedirs( "_".join(NN) , exist_ok=True)
            # 在目录中创建 __init__.py 文件
            open( "."+os.path.sep+"_".join(NN)+os.path.sep+"__init__.py" , 'w').write(" ")

        # print( len(NN) )
        os._exit(0)


if len(sys.argv)==4:
    if  sys.argv[1]=="setup.py":
        SA,SB = sys.argv[2],sys.argv[3]
        ########################################################
        NU= ">nul 2>&1" if os.name=="nt" else  ">/dev/null 2>&1"
        if os.system(f'git remote get-url gitlab {NU}')!=0:
            os.system(f"git init")
            os.system(f"git remote add gitlab https://{ pypi }@gitlab.com/{moon}/{SA}")
            print(f"@ [位置] @ git remote add gitlab https://pypi:{ pypi }@gitlab.com/{moon}/{SA} @")
        else:
            import re
            URL = os.popen("git remote get-url gitlab").read().strip()
            KEY=re.findall(r'https://([^/^@]+)@gitlab\.com/[^/^@]+/[^/^@]+$',URL)
            if len(KEY)!=0:
               KEY=KEY[0]
               URL = re.sub( f"//{KEY}@", f"//{pypi}@" ,URL )
            else:
                os.system(f"git remote  set-url gitlab {URL}")
                print(f"@ [位置] @ git remote  set-url  {URL} @")
                print("-"*50)
                os._exit(0)

            # print("@!! URL ",KEY,pypi,URL)
            # print("@ URL ",URL)

     
        #####################################################
        Var.update_names( SA,SB )

        
        if  not pip_api(moon,SA):
            print(f"@ 專案不存在 @")
            os._exit(0)


        # # print("@ SA :",pip_tag(moon,SA),SB)
        # if  pip_tag(moon,SA)==[]:
        #     print("# ",os.popen(f"git add . ").read())
        #     print("# ",os.popen(f"git commit -m \"{ SB }\" ").read())
        #     print("# ",os.popen(f"git tag { SB } ").read())
        #     #########################################################
        #     print("# ",os.popen(f"git push -u gitlab main").read())
        #     print("# ",os.popen(f"git push --tags").read())
        # else:
        #     # print( "@ SB :" ,SB in pip_tag(moon,SA)  )
        #     if  SB in pip_tag(moon,SA):
        #         # 刪除本地標籤
        #         os.popen(f"git tag -d { SB }")
        #         # 推送新標籤到遠端
        #         os.popen(f"git push gitlab :refs/tags/{ SB }")
        #         ###################################################
        #         ###################################################
        #     #######################################################
        #     print("# ",os.popen(f"git add . ").read())
        #     print("# ",os.popen(f"git commit -m \"{ SB }\" ").read())
        #     print("# ",os.popen(f"git tag { SB } ").read())
        #     #########################################################
        #     print("# ",os.popen(f"git push -u gitlab main").read())
        #     print("# ",os.popen(f"git push --tags").read())


        if  SB in pip_tag(moon,SA):
            # 刪除本地標籤
            os.popen(f"git tag -d { SB }  {NU}")
            # 推送新標籤到遠端
            os.popen(f"git push gitlab :refs/tags/{ SB }  {NU}")
            ###################################################
            ###################################################
       
        #######################################################
        print("# ",os.popen(f"git add .  {NU}").read())
        print("# ",os.popen(f"git commit -m \"{ SB }\"  {NU}").read())
        print("# ",os.popen(f"git tag { SB }  {NU}").read())
        #########################################################
        print("# ",os.popen(f"git push -u gitlab main  {NU}").read())
        print("# ",os.popen(f"git push --tags").read())
        os.system(f"pip uninstall {SA} -y")
        os._exit(0)
        
#############################################################
if len(sys.argv)>=2 and name and pypi:
    print("@ [使用] user.api 認證 @")
    # print(f"@ {sys.argv} @",os.environ["username"])
    args = sys.argv[1:]
    # if args is None:
    #     args = sys.argv[1:]
    if  "install" in sys.argv:
        NN = args.index("install")+1
        # KEY= os.environ["KEY"]
        if  args[NN].find(r"==")!=-1:
            SA,SB=args[NN].split(r"==")
            # print(f"@1 {SA} {SB}")
            args[NN]=f"git+https://{pypi}@gitlab.com/{moon}/{SA}@{SB}"
            # print(f"@1 {args} {pypi}")
        else:
            SA=args[NN]
            # print(f"@2 {SA}")
            args[NN]=f"git+https://{pypi}@gitlab.com/{moon}/{SA}"
            # print(f"@2 {args} {pypi}")
        ################################################################
        
        # print("@!! ",pip_api(SA))
        if not pip_api( moon ,SA):
            import re
            # 定義正規表達式模式
            pattern = re.compile(r'^git\+https://[^/^@]+@gitlab\.com/[^/^@]+/[^/^@]+[@]?[^/^@]?$')
            args = sys.argv[1:]              ## 條件需要::不要移動 
            if  not pattern.match( args[NN] ):
                print(f"@ 專案 {SA} 不存在 @")
                os._exit(0)
        else:
            if 'SB' in globals():
                # print("存在名为 SB 的变量")
                if  SB in pip_tag( moon ,SA):
                    print(f"@ 目前沒有 {SB} 版本 @")
                    os._exit(0)
        ##############################
        # print(f"@ 專案 {SA} 存在 @")
        sys.argv=[sys.argv[0]]
        sys.argv.extend( args )
        # print("@ argv @",sys.argv)
        ##############################
