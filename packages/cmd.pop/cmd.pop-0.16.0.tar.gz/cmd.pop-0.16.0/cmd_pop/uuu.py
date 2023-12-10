
#######################################################
if  "-u" in sys.argv and "-p" in sys.argv:
    if     (sys.argv.index("-u")+1) == len(sys.argv):
           BL=False
    elif   (sys.argv.index("-p")+1) == len(sys.argv):
            BL=False
    else:
            BL=True 
else:
    BL=False
#######################################################
if  BL:
    if  sys.argv.index("-u") >  sys.argv.index("-p"):
        NN=sys.argv.index("-u")
        sys.argv.pop(NN)
        AAA= sys.argv.pop(NN)
        #######################
        NN=sys.argv.index("-p")
        sys.argv.pop(NN)
        BBB= sys.argv.pop(NN)
    else:
        NN=sys.argv.index("-p")
        sys.argv.pop(NN)
        BBB= sys.argv.pop(NN)
        #######################
        NN=sys.argv.index("-u")
        sys.argv.pop(NN)
        AAA= sys.argv.pop(NN)
##################################################################