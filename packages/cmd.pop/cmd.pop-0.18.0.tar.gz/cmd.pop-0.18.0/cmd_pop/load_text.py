#################################
# 在 colab 時候 
# @ name @ load_ext
#################################
# 當 from cmd_pop import load_ext
# @ name @ cmd_pop.load_ext
# print("@ name @",__name__,)

import os
if os.name=="nt" and __name__!="cmd_pop.load_ext":
    print("@ name @",__name__)
    from IPython.core.magic import register_line_magic
    @register_line_magic
    def pip(line):
        """
        自定義魔法函數：%greet
        """
        import os
        print("@ name @",__name__)
        print( os.popen(f"pip {line}").read() )

    # 在Notebook中運行這個單元格，這樣你就可以使用 %greet 這個魔法函數了。
