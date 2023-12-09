from .gCalVi import *

def run():
    gui:gCalVi
    app,gui=launchCalVi()
    quitCalVi(app)

def cleanRun():
    if os.path.exists(lastcfgname_CalVi):
        os.remove(lastcfgname_CalVi)
    run()
   
def debugRun():
    gui:gCalVi
    app,gui=launchCalVi(flagInputDebug=True)
    quitCalVi(app)


