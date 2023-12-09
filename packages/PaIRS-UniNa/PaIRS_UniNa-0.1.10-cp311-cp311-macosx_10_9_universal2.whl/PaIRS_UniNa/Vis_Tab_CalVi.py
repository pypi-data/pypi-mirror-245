from .ui_Vis_Tab_CalVi import*
from .TabTools import*
from .calib import Calib, CalibWorker,CalibTasks, calibTasksText, CalibFunctions, calibFunctionsText
from .imageviewer import CalibView

if __name__ == "__main__":
    cfgName='../../img/calib/NewCam0.cfg'
    cfgName='../../img/calib/NewCam0_Mod.cfg'
    FlagRun=True
else:
    cfgName=''
    FlagRun=False

class VISpar_CalVi(TABpar):
    FlagVis=True

    def __init__(self):
        self.setup()
        super().__init__()
        self.name='VISpar'
        self.surname='VIS_Tab'
        self.unchecked_fields+=[]

    def setup(self):
        self.cfgName=cfgName
        self.FlagRun=FlagRun

        self.nPlane=0
        self.plane=0
        self.nCam=0
        self.cam=0
        #self.scaleFactor=1.0
        self.LLim=0
        self.LMin=0
        self.LMax=0

        self.MaskType=0
        self.FlagShowMask=1
        self.FlagPlotMask=0

        self.xOriOff=0
        self.yOriOff=0
        self.xm=0
        self.xp=0
        self.ym=0
        self.yp=0

class Vis_Tab_CalVi(gPaIRS_Tab):
    class VIS_Tab_Signals(gPaIRS_Tab.Tab_Signals):
        run=Signal(bool)
        pass
    def closeEvent(self,event):
        ''' called when closing 
        I had to add this to be sure that calib was destroyed'''
        
        #self.calibView.imageViewerThreadpool.clear()
        pri.Info.white("Vis_Tab_CalVi closeEvent")
        del self.calibView
    
    def resizeEvent(self,event):
        super().resizeEvent(event)
        self.setZoom()

    def __init__(self,*args):
        parent=None
        self.flagInit=True
        if len(args): parent=args[0]
        if len(args)>1: self.flagInit=args[1]
        super().__init__(parent,Ui_VisTab_CalVi,VISpar_CalVi)
        self.signals=self.VIS_Tab_Signals(self)

        #------------------------------------- Graphical interface: widgets
        self.ui: Ui_VisTab_CalVi
        ui=self.ui

        self.setupWid()  #---------------- IMPORTANT
        #introducing CalibView
        self.scrollArea = QtWidgets.QScrollArea(self)
        self.scrollArea.setBackgroundRole(QtGui.QPalette.Dark)
        self.calibView=CalibView(self.scrollArea,self.outFromCalibView,self.outToStatusBarFromCalibView,self.textFromCalib,self.workerCompleted)
        self.scrollArea.setWidget(self.calibView)
        self.ui.splitter.insertWidget(0,self.scrollArea)

        #------------------------------------- Graphical interface: miscellanea
        self.ui.status_L.setText('')
        self.ui.status_R.setText('')
        self.FlagFirstShow=False
        self.FlagSettingNewCalib=False
        self.setLogFont(fontPixelSize-dfontLog)

        #------------------------------------- Declaration of parameters 
        self.VISpar_base=VISpar_CalVi()
        self.VISpar:VISpar_CalVi=self.TABpar
        self.VISpar_old:VISpar_CalVi=self.TABpar_old
        self.defineSetTABpar(self.setVISpar)
        
        
        #------------------------------------- Callbacks 
        self.setupCallbacks()
        self.FlagSettingPar=False
        self.FlagAddPrev=False
        self.updateGCalVi= lambda: None
        self.calibView.flagCurrentTask=CalibTasks.stop

        #------------------------------------- Initializing       
        if self.flagInit:
            self.initialize()


    def initialize(self):
        pri.Info.yellow(f'{"*"*20}   VIS initialization   {"*"*20}')
        self.defaultSplitterSize()

        if self.VISpar.cfgName:
            #self.VISpar.FlagRun=True
            flagOp=self.calibView.calib.readCfg()
            self.calibView.calib.readImgs() #todo verificare eventuali errori e dimensioni delle immagini in questo momento non da errore e l'img viene tagliata
            
            self.calib2VIS(flagReset=True,flagSettingNewCalib=True)
            self.setVISpar()
            
            #self.signals.run.emit(not flagOp)
            self.runCalVi('_Mod' in self.VISpar.cfgName)
        #self.ui.plot.show() 
        #self.setTABpar(True)  #with bridge
    
    def defaultSplitterSize(self):
        self.ui.splitter.setSizes([self.width()-self.ui.w_Commands.minimumWidth(),self.ui.w_Commands.minimumWidth()])

    @Slot(bool)
    def runCalVi(self,flagMod=False):
        self.calibView.flagFirstTask=CalibTasks.findPlanesFromOrigin if flagMod else CalibTasks.findAllPlanes
        self.VISpar.plane=self.VISpar.cam=0
        self.setVISpar()
        if self.calibView.executeCalibTask(self.calibView.flagFirstTask):
            self.setTaskButtonsText()
            self.resetScaleFactor()

    def stopCalVi(self):
        self.calibView.executeCalibTask(CalibTasks.stop)
        self.setTaskButtonsText()
        self.plotPlane()

    def show(self):
        super().show()
        if not self.FlagFirstShow:
            self.FlagFirstShow=True
            self.resetScaleFactor()

    def setupCallbacks(self):
        self.ui.button_zoom_minus.clicked.connect(self.addParWrapper(lambda:self.zoom(0.8),'Zoom'))
        self.ui.button_zoom_equal.clicked.connect(self.addParWrapper(self.resetScaleFactor,'Zoom'))
        self.ui.button_zoom_plus.clicked.connect(self.addParWrapper(lambda:self.zoom(1.25),'Zoom'))
        self.ui.splitter.addfuncout['setScrollAreaWidth']=self.setZoom
        

        self.taskButtons=[self.ui.button_findAll,
                          self.ui.button_find,
                          self.ui.button_calibrate,
                          self.ui.button_saveCoord,
                          ]
        self.taskButton_callbacks=[]
        for k,ind in enumerate([f.value for f in CalibTasks if f.value>0]):
            self.taskButton_callbacks.append(lambda dum=ind, flag=k!=3,ff=self.taskButtonPressed: ff(CalibTasks(dum),flag))
            self.taskButtons[k].clicked.connect(self.taskButton_callbacks[k])

        self.buttonsToDisableNotCalibrated=[] #used to gray buttons if not calibrated
        self.functionButtons=[
                              self.ui.button_deleteErr,
                              self.ui.button_focusErr,
                              self.ui.button_copyGrid,
                              ]
        self.functionButtons_callbacks=[]
        for k,ind in  enumerate([f.value for f in CalibFunctions if f.value>0]):
            self.functionButtons_callbacks.append(lambda dum=ind, flag=True,ff=self.functionButtonPressed: ff(CalibFunctions(dum),flag))
            self.functionButtons[k].clicked.connect(self.functionButtons_callbacks[k])
            self.buttonsToDisableNotCalibrated.append(self.functionButtons[k])

        
        functionButtons_insert=[0,0,0]
        for k,ind in  enumerate([f.value for f in CalibFunctions]):
            action=QAction(self.functionButtons[k].icn,calibFunctionsText[abs(ind)],self)
            self.calibView.contextMenuActions.insert(functionButtons_insert[k],action)
            action.triggered.connect(lambda dum=ind, flag=True,ff=self.functionButtonPressed: ff(CalibFunctions(dum),flag))
            if ind>0:
                self.buttonsToDisableNotCalibrated.append(action)

        self.originOffbox=self.ui.g_OriOff
        self.remPoinsBox=self.ui.g_GriLim
        self.buttonsToDisable=[
                              self.ui.spin_plane,
                              self.originOffbox,
                              self.remPoinsBox,
                             ] #used to gray buttons when calibrating
        
        self.spin_plane_callback=self.spinImgChanged
        self.spin_cam_callback=self.spinImgChanged
        self.spin_xOriOff_callback=lambda off: self.spin_OriOff_callback(off,self.ui.spin_xOriOff,True)
        self.spin_yOriOff_callback=lambda off: self.spin_OriOff_callback(off,self.ui.spin_xOriOff,False)

        self.spin_yp_callback=lambda off: self.spin_remPoi_callback(off, self.ui.spin_yp,False,True)
        self.spin_ym_callback=lambda off: self.spin_remPoi_callback(off, self.ui.spin_ym,False,False)
        self.spin_xp_callback=lambda off: self.spin_remPoi_callback(off, self.ui.spin_xp,True,True)
        self.spin_xm_callback=lambda off: self.spin_remPoi_callback(off, self.ui.spin_xm,True,False)
        self.ui.button_copyGrid.clicked.connect(self.copyRemPoints)
        
        spin_names=['plane',
                    'cam',
                    'LMin',
                    'LMax',
                    'yOriOff',
                    'xOriOff',
                    'yp',
                    'ym',
                    'xp',
                    'xm',
                    ]
        spin_tips=['Plane number (from 1 to number of planes)',
                   'Camera number  (from 1 to number of cameras)',
                   'Minimum value of the image intensity',
                   'Maximum value of the image intensity',
                   'Shift the origin along y with respect to the first selected point in current target image',
                   'Shift the origin along x with respect to the first selected point in current target image',
                   'Maximum y limit for the point grid',
                   'Minimum y limit for the point grid',
                   'Maximum x limit for the point grid',
                   'Minimum x limit for the point grid',
                   ]
        self.setSpinCallbacks(spin_names,spin_tips)

        self.button_restore_callback=self.addParWrapper(self.restoreLevels,'Restore image levels')
        self.ui.button_restore.clicked.connect(self.button_restore_callback)

        self.radio_showMask_callback=self.addParWrapper(self.showMask,'Show/hide correlation mask')
        self.ui.radio_showMask.clicked.connect(self.radio_showMask_callback)

        self.tool_plotMask_callback=self.addParWrapper(self.plotMask,'Plot correlation mask')
        self.ui.tool_plotMask.clicked.connect(self.tool_plotMask_callback)

        self.signals.run.connect(self.runCalVi)
        return
    
    def setLogFont(self,fPixSize):
        logfont=self.ui.log.font()
        logfont.setFamily('Courier New')
        logfont.setPixelSize(fPixSize)
        self.ui.log.setFont(logfont)

#********************************************* Setting parameters
    def setVISpar(self):
        FlagImg=bool(len(self.calibView.calib.imgs))
        FlagMask=self.VISpar.MaskType not in (2,3) and bool(len(self.calibView.calib.ccMask))
        if FlagImg:
            self.ui.g_Image.setEnabled(True)
            self.ui.spin_plane.setEnabled(self.VISpar.nPlane>1)
            self.ui.spin_cam.setEnabled(self.VISpar.nCam>1)
        else:
            self.ui.g_Image.setEnabled(False)     

        FlagZoomLevels=FlagImg or FlagMask
        self.ui.g_Zoom.setEnabled(FlagZoomLevels)
        self.ui.g_Levels.setEnabled(FlagZoomLevels)
        
        self.ui.g_Mask.setVisible(FlagMask)
        self.ui.radio_showMask.setChecked(self.VISpar.FlagShowMask)
        self.ui.tool_plotMask.setEnabled(self.VISpar.FlagShowMask)
        self.ui.tool_plotMask.setChecked(self.VISpar.FlagPlotMask and self.VISpar.FlagShowMask)
        
        self.ui.w_Commands.setVisible(self.VISpar.FlagRun)
        flagNewRun=self.VISpar.isDifferentFrom(self.VISpar_old,[],['FlagRun'],True)
        if flagNewRun: self.defaultSplitterSize()
        if self.VISpar.FlagRun:
            self.calibView.contextMenu =QtWidgets.QMenu(self)
            for a in self.calibView.contextMenuActions:
                self.calibView.contextMenu.addAction(a)
            self.calibView.contextMenu.insertSeparator(self.calibView.contextMenuActions[1])
        else:
            self.calibView.contextMenu =None
            
        self.ui.status_L.setText('')
        self.ui.status_R.setText('')
        self.setSpinMaxMinLimValues()
        self.setZoom()
        self.plotPlane()
        flagPlotMask=self.VISpar.isDifferentFrom(self.VISpar_old,[],['FlagPlotMask'],True)
        if  flagPlotMask or flagNewRun or self.FlagSettingNewCalib:
            self.FlagSettingNewCalib=False
            if flagPlotMask:
                self.restoreLevels()
                self.setSpinMaxMinLimValues()

            self.resetScaleFactor()
            self.setZoom()
            self.plotPlane()
        return
    
    def calib2VIS(self,flagReset=True,flagSettingNewCalib=True):
        c=self.calibView.calib
        self.VISpar.nPlane=c.nPlanesPerCam
        self.VISpar.nCam=c.nCams
        """
        if flagReset:
            self.VISpar.plane=0
            self.VISpar.cam=0
        else:
            self.VISpar.plane=c.nPlanesPerCam if self.VISpar.plane>c.nPlanesPerCam else self.VISpar.plane
            self.VISpar.cam=c.nCams if self.VISpar.cam>c.nCams else self.VISpar.cam
        """
        
        c.setLMinMax()
        self.VISpar.LLim=c.LLim
        if flagReset: 
            self.VISpar.LMin=c.LMin
            self.VISpar.LMax=c.LMax
        else:
            self.VISpar.LMax=c.LMax if self.VISpar.LMax>c.LLim else self.VISpar.LMax
            self.VISpar.LMin=self.VISpar.LMax-1 if self.VISpar.LMin >self.VISpar.LMax-1 else self.VISpar.LMin

        self.VISpar.MaskType=abs(self.calibView.calib.cal.data.FlagPos)
        if self.VISpar.MaskType in (2,3):
            self.VISpar.FlagShowMask=0
            self.VISpar.FlagPlotMask=0
        self.FlagSettingNewCalib=flagSettingNewCalib
        #self.setVISpar()

    def setSpinMaxMinLimValues(self):
        spins=['plane','cam','LMin','LMax']
        vals=[]
        for s in spins: vals.append(getattr(self.VISpar,s))
        self.setSpinMaxMin()
        for s,v in zip(spins,vals): setattr(self.VISpar,s,v)
        self.setSpinValues()

    def setSpinMaxMin(self):
        self.ui.spin_plane.setMinimum(1*bool(self.VISpar.nPlane))
        self.ui.spin_plane.setMaximum(self.VISpar.nPlane)
        self.ui.spin_cam.setMinimum(1*bool(self.VISpar.nCam))
        self.ui.spin_cam.setMaximum(self.VISpar.nCam)

        self.ui.spin_LMin.setMinimum(-self.VISpar.LLim)
        self.ui.spin_LMin.setMaximum(self.VISpar.LMax-1)
        self.ui.spin_LMax.setMinimum(self.VISpar.LMin+1)
        self.ui.spin_LMax.setMaximum(self.VISpar.LLim)

    def setSpinValues(self):
        spin_p1=['plane','cam']
        spins=self.findChildren(MyQSpin)+self.findChildren(MyQDoubleSpin)
        for s in spins:
            s:MyQSpin
            nameSpin=s.objectName().split('spin_')[-1]
            if nameSpin in spin_p1: d=1
            else: d=0
            s.setValue(getattr(self.VISpar,nameSpin)+d)

    def spin_LMin_callback(self):
        self.VISpar.LMin=self.calibView.calib.LMin=self.ui.spin_LMin.value()
        if self.ui.spin_LMin.hasFocus():
            self.ui.spin_LMax.setMinimum(self.VISpar.LMin+1)
            #self.plotPlane()

    def spin_LMax_callback(self):
        self.VISpar.LMax=self.calibView.calib.LMax=self.ui.spin_LMax.value()
        if self.ui.spin_LMax.hasFocus():
            self.ui.spin_LMin.setMaximum(self.VISpar.LMax-1)
            #self.plotPlane()

    def restoreLevels(self):
        pc=self.VISpar.plane
        c=self.VISpar.cam
        p=pc+c*self.calibView.calib.nPlanesPerCam
        c=self.calibView.calib
        c.setLMinMax(p)
        self.VISpar.LLim=c.LLim
        self.VISpar.LMin=c.LMin
        self.VISpar.LMax=c.LMax

    def plotPlane(self):
        if not self.calibView.calib.cal.data.Numpiani: 
            self.calibView.hide()
            return
        else:
            self.calibView.show()
        pc=self.VISpar.plane
        c=self.VISpar.cam
        p=pc+c*self.calibView.calib.nPlanesPerCam
        self.calibView.plotPlane(p)

    def spin_OriOff_callback(self,Off,spin:QSpinBox,flagX):
        self.focusOnTarget(False)
        nameSpin=spin.objectName().split('spin_')[-1]
        setattr(self.VISpar,nameSpin,spin.value())
        self.calibView.spinOriginChanged(Off, spin,flagX)

    def spin_remPoi_callback(self,Off,spin:QSpinBox,flagX,flagPos):
        self.focusOnTarget(False)
        nameSpin=spin.objectName().split('spin_')[-1]
        setattr(self.VISpar,nameSpin,spin.value())
        self.calibView.spinRemPoints(Off,spin,flagX,flagPos)
    
    def copyRemPoints(self):
        self.focusOnTarget(False)
        self.calibView.copyRemPoints()

    def showMask(self):
        self.VISpar.FlagShowMask=self.ui.radio_showMask.isChecked()
        if not self.VISpar.FlagShowMask: self.VISpar.FlagPlotMask=False
        self.calibView.calib.flagShowMask=self.VISpar.FlagShowMask
        self.calibView.calib.flagPlotMask=self.VISpar.FlagPlotMask
    
    def plotMask(self):
        self.VISpar.FlagPlotMask=self.ui.tool_plotMask.isChecked()
        self.calibView.calib.flagPlotMask=self.VISpar.FlagPlotMask
        #self.restoreLevels()

#********************************************* Zoom functions
    def resetScaleFactor(self):
        ''' reset the scale factor so that the image perfectly feet the window'''
        self.calibView.resetScaleFactor(self.scrollArea.size())
        self.zoomImage(1)

    def zoom(self,zoom):
        ''' zooms f a factor zoom if negative reset to no zoom '''
        if zoom<=0:
            zoom =self.calibView.scaleFactor = 1.0
        self.zoomImage(zoom)
  
    def zoomImage(self, zoom):
        ''' zooms the image of self.CalibView.scaleFactor times a factor zoom
        adjust also the scrollBars'''
        self.calibView.scaleFactor *= zoom
        self.setZoom()
        self.adjustScrollBar(self.scrollArea.horizontalScrollBar(), zoom)
        self.adjustScrollBar(self.scrollArea.verticalScrollBar(), zoom)
        
    def setZoom(self):
        self.calibView.resize(self.calibView.scaleFactor * self.calibView.pixmap().size())
        
    def adjustScrollBar(self, scrollBar:QScrollBar, factor):
        ''' adjust the position when zooming in or out 
        # TBS copied and possibly modified wrongly'''  
        scrollBar.setValue(int(factor * scrollBar.value()+ ((factor - 1) * scrollBar.pageStep()/2)))


#********************************************* CalibView function
    def outFromCalibView(self,out:str):
        ''' output From CalibView called from plotImg'''
        calib=self.calibView.calib
        da=calib.cal.vect
        p=calib.plane
        c=int(p/calib.nPlanesPerCam)
        pc=p-c*calib.nPlanesPerCam
        
        self.ui.spin_plane.setValue(pc+1)
        self.ui.spin_cam.setValue(c+1)
        self.ui.spin_xOriOff.setValue(da.xOrShift[p])
        self.ui.spin_yOriOff.setValue(da.yOrShift[p])

        self.ui.spin_xm.setValue(da.remPointsLe[p])
        self.ui.spin_xp.setValue(da.remPointsRi[p])
        self.ui.spin_ym.setValue(da.remPointsDo[p])
        self.ui.spin_yp.setValue(da.remPointsUp[p])

        if self.VISpar.FlagPlotMask:
            out2=' [CC mask]'
        else:
            out2=' [target image]'
        self.ui.status_R.setText(out+out2)
        self.calibView.setStatusTip(out+out2)

    def outToStatusBarFromCalibView(self,out:str):
        ''' output to status bar From CalibView '''
        self.ui.status_L.setText(out)
        #self.calibView.setToolTip(out)

    Slot(str)
    def textFromCalib(self,out:str):
        ''' set single line text from calib'''
        self.ui.log.setText(out)

    def workerCompleted(self):
        ''' called when worker has completed '''
        if  not self.calibView.flagCurrentTask is CalibTasks.stop:# pylint: disable=unneeded-not
            if self.calibView.executeCalibTask(CalibTasks.stop):
                self.setTaskButtonsText()

    def setTaskButtonsText(self):
        ''' set all the button texts and enable/disable them '''
        flagEnab=True if (self.calibView.flagCurrentTask==CalibTasks.stop) else False
        self.updateGCalVi()
        for f in  [f for f in CalibTasks if f.value>0]:
            if flagEnab:  # stop the process -> enable all buttons and restore text
                self.taskButtons [f.value-1].setText(calibTasksText[f.value])
                self.taskButtons [f.value-1].setEnabled(True)
            else:
                if self.calibView.flagCurrentTask is f: 
                    self.taskButtons [f.value-1].setText(calibTasksText[0])
                else:
                    self.taskButtons [f.value-1].setEnabled(False)
        for b in self.buttonsToDisable:
            b.setEnabled(flagEnab)
        for b  in  self.buttonsToDisableNotCalibrated:      
            b.setEnabled(self.calibView.calib.cal.flagCalibrated)    
        #for b in self.functionButtons:      b.setEnabled(flagEnab)
   
    def taskButtonPressed(self,flag:CalibTasks,flagFocus):
        ''' one of the button has been  pressed '''
        if flagFocus: self.focusOnTarget()
        if self.calibView.executeCalibTask(flag):
            self.setTaskButtonsText()
    
    def functionButtonPressed(self,flag:CalibTasks,flagFocus):
        ''' one of the button has been  pressed '''
        if flagFocus: self.focusOnTarget()
        self.calibView.executeCalibFunction(flag)  

    def focusOnTarget(self,flagCallback=True):
        if self.VISpar.FlagPlotMask:
            self.ui.tool_plotMask.setChecked(False)
            self.tool_plotMask_callback()

#********************************************* Spin callbacks
    def spinImgChanged(self):
        ''' changes the plotted image'''
        pc=self.ui.spin_plane.value()-1
        self.VISpar.plane=pc
        c=self.ui.spin_cam.value()-1
        self.VISpar.cam=c
        self.plotPlane()

if __name__ == "__main__":
    import sys
    app=QApplication.instance()
    if not app:app = QApplication(sys.argv)
    app.setStyle('Fusion')
    object = Vis_Tab_CalVi(None)
    object.show()
    app.exec()
    app.quit()
    app=None