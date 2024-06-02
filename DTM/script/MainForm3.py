from PyQt6 import QtCore, QtGui, QtWidgets
from draw import Draw
from algorithms import Algorithms
from i_o import IO
from settings import *

class Ui_MainWindow(object):
    '''
    - a class for program´s main window and connecting operations in other classes.

    - Methods:
        - setupUi(settings: QtWidgets.QDialog): Main function called by the constructor
        - openClick() - Loads point cloud data from file chosen via a file dialog
        - analysis functions:
            - only happen if there are at least 3 unique coordinates in X and Y Axis so there are visible results of DT. Otherwise no edge would be visible on a canvas.
            - all the functions trigger DT to provide up-to-date results
            - all the functions check a corresponding button in "View" pane to make the result visible

            - createDTClick() - creates Delaunay triangulation (DT) 
            - createContourLinesClick() - Create contours with parameters min/max elevation, step [m] obtained by a pop-up window (Ui_Settings class)
            - analyzeSlopeClick() - analyzes DT´s triangles´ slope
            - analyzeAspectClick()  - analyzes DT´s triangles´ aspect

        - clear type functions:
            - both reset canvas to initial state

            - clearClick() - clear results
            - clearAllClick() - clear results and input data
        - rescaleClick() - rescales all data to the size of the window

        - view type functions:
            - they display individual features related to DT

            - viewDTClick() - view DT
            - viewContourLinesClick() - view contours
            - viewSlopeClick() - view slope
            - viewAspectClick() - view aspect

        - setParametersClick() - open Ui_Settings class pop-up window to obtain contour parameters
        - closeClick() - close the programme
        - retranslateUi(settings: QtWidgets.QDialog): Method created by Qt, necessary for running the program
    '''
    def setupUi(self, MainWindow: QtWidgets.QMainWindow) -> None:
        self.algo = Algorithms()                                    # make Algorithms class access easier
        MainWindow.setObjectName("MainWindow")                      # main window, Canvas widget, layout and window scaling policy
        MainWindow.resize(1280, 789)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setMinimumSize(QtCore.QSize(0, 0))
        self.centralwidget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.centralwidget.setBaseSize(QtCore.QSize(0, 0))
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.Canvas = Draw(parent=self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Canvas.sizePolicy().hasHeightForWidth())
        self.Canvas.setSizePolicy(sizePolicy)
        self.Canvas.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.Canvas.setObjectName("Canvas")
        self.horizontalLayout.addWidget(self.Canvas)
        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)        # menu bar
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1280, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(parent=self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuAnalysis = QtWidgets.QMenu(parent=self.menubar)
        self.menuAnalysis.setObjectName("menuAnalysis")
        self.menuView = QtWidgets.QMenu(parent=self.menubar)
        self.menuView.setObjectName("menuView")
        self.menuClear = QtWidgets.QMenu(parent=self.menubar)
        self.menuClear.setObjectName("menuClear")
        self.menuSettings = QtWidgets.QMenu(parent=self.menubar)
        self.menuSettings.setObjectName("menuSettings")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(parent=MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.ToolBarArea.TopToolBarArea, self.toolBar)
        self.actionOpen = QtGui.QAction(parent=MainWindow)

        icon = QtGui.QIcon()                                        # icons
        icon.addPixmap(QtGui.QPixmap("icons/open_file.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionOpen.setIcon(icon)
        self.actionOpen.setObjectName("actionOpen")
        self.actionExit = QtGui.QAction(parent=MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("icons/exit.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionExit.setIcon(icon1)
        self.actionExit.setObjectName("actionExit")
        self.actionCreate_DT = QtGui.QAction(parent=MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("icons/triangles2.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionCreate_DT.setIcon(icon2)
        self.actionCreate_DT.setObjectName("actionCreate_DT")
        self.actionCreateContouLines = QtGui.QAction(parent=MainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("icons/contours2.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionCreateContouLines.setIcon(icon3)
        self.actionCreateContouLines.setObjectName("actionCreateContouLines")
        self.actionAnalyzeSlope = QtGui.QAction(parent=MainWindow)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("icons/slope2.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionAnalyzeSlope.setIcon(icon4)
        self.actionAnalyzeSlope.setObjectName("actionAnalyzeSlope")
        self.actionAnalyzeAspect = QtGui.QAction(parent=MainWindow)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("icons/orientation2.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionAnalyzeAspect.setIcon(icon5)
        self.actionAnalyzeAspect.setObjectName("actionAnalyzeAspect")
        self.actionDT = QtGui.QAction(parent=MainWindow)
        self.actionDT.setCheckable(True)
        self.actionDT.setObjectName("actionDT")
        self.actionContour_lines_2 = QtGui.QAction(parent=MainWindow)
        self.actionContour_lines_2.setCheckable(True)
        self.actionContour_lines_2.setObjectName("actionContour_lines_2")
        self.actionSlope = QtGui.QAction(parent=MainWindow)
        self.actionSlope.setCheckable(True)
        self.actionSlope.setObjectName("actionSlope")
        self.actionAspect = QtGui.QAction(parent=MainWindow)
        self.actionAspect.setCheckable(True)
        self.actionAspect.setObjectName("actionAspect")
        self.actionClear_results = QtGui.QAction(parent=MainWindow)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("icons/clear.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionClear_results.setIcon(icon6)
        self.actionClear_results.setObjectName("actionClear_results")
        self.actionClear_all = QtGui.QAction(parent=MainWindow)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap("icons/clear_all.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionClear_all.setIcon(icon7)
        self.actionClear_all.setObjectName("actionClear_all")
        self.actionParameters = QtGui.QAction(parent=MainWindow)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap("icons/settings.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionParameters.setIcon(icon8)
        self.actionParameters.setObjectName("actionParameters")
        self.actionRescale = QtGui.QAction(parent=MainWindow)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap("icons/resize.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionRescale.setIcon(icon9)
        self.actionRescale.setObjectName("actionRescale")

        self.menuFile.addAction(self.actionOpen)                    # menu pane
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuAnalysis.addAction(self.actionCreate_DT)
        self.menuAnalysis.addSeparator()
        self.menuAnalysis.addAction(self.actionCreateContouLines)
        self.menuAnalysis.addAction(self.actionAnalyzeSlope)
        self.menuAnalysis.addAction(self.actionAnalyzeAspect)
        self.menuView.addAction(self.actionDT)
        self.menuView.addAction(self.actionContour_lines_2)
        self.menuView.addAction(self.actionSlope)
        self.menuView.addAction(self.actionAspect)
        self.menuClear.addAction(self.actionClear_results)
        self.menuClear.addSeparator()
        self.menuClear.addAction(self.actionClear_all)
        self.menuSettings.addAction(self.actionParameters)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuAnalysis.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuClear.menuAction())
        self.menubar.addAction(self.menuSettings.menuAction())

        self.toolBar.addAction(self.actionOpen)                     # toolbar
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionCreate_DT)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionCreateContouLines)
        self.toolBar.addAction(self.actionAnalyzeSlope)
        self.toolBar.addAction(self.actionAnalyzeAspect)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionRescale)
        self.toolBar.addAction(self.actionClear_results)
        self.toolBar.addAction(self.actionParameters)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionClear_all)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionExit)

        self.settings = QtWidgets.QDialog()                         #Settings pop-up window
        self.ui = Ui_Settings()
        self.ui.setupUi(self.settings)

        self.retranslateUi(MainWindow)
        
        self.actionOpen.triggered.connect(self.openClick)           #User functions
        self.actionCreate_DT.triggered.connect(self.createDTClick)
        self.actionCreateContouLines.triggered.connect(self.createContourLinesClick)    
        self.actionAnalyzeSlope.triggered.connect(self.analyzeSlopeClick)
        self.actionAnalyzeAspect.triggered.connect(self.analyzeAspectClick) 
        self.actionClear_results.triggered.connect(self.clearClick)
        self.actionClear_all.triggered.connect(self.clearAllClick) 
        self.actionRescale.triggered.connect(self.rescaleClick)
        
        self.actionDT.toggled.connect(self.viewDTClick)
        self.actionContour_lines_2.toggled.connect(self.viewContourLinesClick)
        self.actionSlope.toggled.connect(self.viewSlopeClick)
        self.actionAspect.toggled.connect(self.viewAspectClick)

        self.actionParameters.triggered.connect(self.setParametersClick)

        self.actionExit.triggered.connect(self.closeClick)
        
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def openClick(self) -> None:
        file = QtWidgets.QFileDialog.getOpenFileName(caption = 'Open File', filter = 'JSON compatible (*.txt *.json *.geojson)')[0]
        io = IO()           # Input output framework
        if file != '':      # If a file name was chosen
            points = io.load(file, self.Canvas.getWidth(), self.Canvas.getHeight())         # Load polygons and stretch them to current widget´s size
            if points:
                self.Canvas.setPoints(points)                                               # update data
                self.Canvas.clearResults()
            else:
                self.Canvas.messageBox('Error', 'Failed to load points.')       

    def createDTClick(self) -> None:
        points = self.Canvas.getPoints()                #Get points
        unique_per_dim = self.algo.uniquePerDim(points)         # count of unique coordinates in X, Y axes

        if min(unique_per_dim) >= 3:                    # 3 or more points with unique X and Y coordinate 
            dt = self.algo.createDT(points)             #Create triangulation                
            
            self.Canvas.setDT(dt)                       #Update DT  
            self.actionDT.setChecked(True)              #Check menu item 
            self.Canvas.update()
        else:
            self.Canvas.messageBox('Error', 'Not enough unique points to visualize the result.')
                
    def createContourLinesClick(self) -> None:
        points = self.Canvas.getPoints()                #Get points
        unique_per_dim = self.algo.uniquePerDim(points)         # count of unique coordinates in X, Y axes

        if min(unique_per_dim) >= 3:                    # 3 or more points with unique X and Y coordinate 
            dt = self.algo.createDT(points)             #Create DT
            
            zmin = self.ui.lineEdit.text()
            zmax = self.ui.lineEdit_2.text()
            dz = self.ui.lineEdit_3.text()              #Get contour line parameters   

            settings = (zmin, zmax, dz)
            meanings = ('Minimum contour line height', 'Maximum contour line height', 'Minimum contour line height interval')
            settings_float = []

            try:
                for i in range(3):
                    settings_float.append(float(settings[i]))
            except ValueError:
                self.Canvas.messageBox('Error', f'Parameter "{meanings[i]}" not a number')
            else:
                contours = self.algo.createContourLines(dt, settings_float[0], settings_float[1], settings_float[2])            # Create contour lines
                
                self.Canvas.setDT(dt)                       #Set DT
                self.Canvas.setContours(contours)           #Set results
                self.actionContour_lines_2.setChecked(True) #Check menu item
                self.Canvas.update()
        else:
            self.Canvas.messageBox('Error', 'Not enough unique points to visualize the result.')
                    
    def analyzeSlopeClick(self) -> None:
        points = self.Canvas.getPoints()                        #Get points
        unique_per_dim = self.algo.uniquePerDim(points)         # count of unique coordinates in X, Y axes

        if min(unique_per_dim) >= 3:                            # 3 or more points with unique X and Y coordinate 
            dt = self.algo.createDT(self.Canvas.getPoints())         #Create DT
            dtm_slope = self.algo.analyzeDTMSlope(dt)           #Analyze dtm slope
            
            self.Canvas.setDT(dt)                               #Set DT
            self.Canvas.setDTMSlope(dtm_slope)                  #Set results   

            self.actionSlope.setChecked(True)                   # enable slope drawing
            self.actionAspect.setChecked(False)                 # disable slope drawing

            self.Canvas.update()
        else:
            self.Canvas.messageBox('Error', 'Not enough unique points to visualize the result.')

    def analyzeAspectClick(self) -> None:
        points = self.Canvas.getPoints()                    #Get points
        unique_per_dim = self.algo.uniquePerDim(points)         # count of unique coordinates in X, Y axes

        if min(unique_per_dim) >= 3:                        # 3 or more points with unique X and Y coordinate 
            dt = self.algo.createDT(self.Canvas.getPoints())         #Create DT
            dtm_aspect = self.algo.analyzeDTMAspect(dt)     #Analyze dtm aspect
            
            self.Canvas.setDT(dt)                           #Set DT
            self.Canvas.setDTMAspect(dtm_aspect)            #Set results     

            self.actionAspect.setChecked(True)              # enable aspect drawing
            self.actionSlope.setChecked(False)              # disable slope drawing  

            self.Canvas.update() 
        else:
            self.Canvas.messageBox('Error', 'Not enough unique points to visualize the result.')                           
    
    def clearClick(self) -> None:
        self.Canvas.clearResults()                      #Clear results
        self.Canvas.repaint()                           #Repaint screen
    
    def clearAllClick(self) -> None:
        self.Canvas.clearAll()                          #Clear all data
        self.Canvas.repaint()                           #Repaint screen

    def rescaleClick(self) -> None:
        points = self.Canvas.getPoints()
        unique_per_dim = self.algo.uniquePerDim(points)         # count of unique coordinates in X, Y axes

        if min(unique_per_dim) >= 2:                    # 2 or more points with unique X and Y coordinate 
            points, dt, contours, slope, aspect = self.algo.rescale(points, self.Canvas.getDT(), self.Canvas.getContours(), 
                self.Canvas.getDTMSlope(), self.Canvas.getDTMAspect(), self.Canvas.getWidth(), self.Canvas.getHeight())
            
            self.Canvas.setPoints(points)               # Update the widget
            self.Canvas.setDT(dt)                       # Update the widget
            self.Canvas.setContours(contours)           # Update the widget
            self.Canvas.setDTMSlope(slope)              # Update the widget
            self.Canvas.setDTMAspect(aspect)            # Update the widget

            self.Canvas.repaint()                       #Repaint screen 
        else:
            self.Canvas.messageBox('Error', 'Not enough unique points to rescale.')   
    
    def viewDTClick(self) -> None:
        self.Canvas.setViewDT(self.actionDT.isChecked())        #Enable/disable drawing
        self.Canvas.update()                                    #Update

    def viewContourLinesClick(self) -> None:
        self.Canvas.setViewContourLines(self.actionContour_lines_2.isChecked())     #Enable/disable drawing
        self.Canvas.update()                                                        #Update
    
    def viewSlopeClick(self) -> None:
        self.Canvas.setViewSlope(self.actionSlope.isChecked())                      #Enable/disable drawing
        self.Canvas.update()                                                        #Update

    def viewAspectClick(self) -> None:
        self.Canvas.setViewAspect(self.actionAspect.isChecked())                    #Enable/disable drawing
        self.Canvas.update()                                                        #Update
    
    def setParametersClick(self) -> None:
        self.settings.show()            # open pop-up parameter window                                                                    
    
    def closeClick(self) -> None:
        app.quit()  

    def retranslateUi(self, MainWindow: QtWidgets.QMainWindow) -> None:
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "DTM Analysis"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuAnalysis.setTitle(_translate("MainWindow", "Analysis"))
        self.menuView.setTitle(_translate("MainWindow", "View"))
        self.menuClear.setTitle(_translate("MainWindow", "Clear"))
        self.menuSettings.setTitle(_translate("MainWindow", "Settings"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionOpen.setToolTip(_translate("MainWindow", "Open file"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionExit.setToolTip(_translate("MainWindow", "Exit application"))
        self.actionExit.setShortcut(_translate("MainWindow", "Backspace"))
        self.actionCreate_DT.setText(_translate("MainWindow", "Create DT"))
        self.actionCreate_DT.setToolTip(_translate("MainWindow", "Create Delaunay triangulation"))
        self.actionCreateContouLines.setText(_translate("MainWindow", "Create contour lines"))
        self.actionAnalyzeSlope.setText(_translate("MainWindow", "Analyze slope"))
        self.actionAnalyzeSlope.setToolTip(_translate("MainWindow", "Analyze DTM slope"))
        self.actionAnalyzeAspect.setText(_translate("MainWindow", "Analyze aspect"))
        self.actionAnalyzeAspect.setToolTip(_translate("MainWindow", "Analyze DTM aspect"))
        self.actionDT.setText(_translate("MainWindow", "DT"))
        self.actionContour_lines_2.setText(_translate("MainWindow", "Contour lines"))
        self.actionSlope.setText(_translate("MainWindow", "Slope"))
        self.actionAspect.setText(_translate("MainWindow", "Aspect"))
        self.actionAspect.setToolTip(_translate("MainWindow", "Aspect"))
        self.actionClear_results.setText(_translate("MainWindow", "Clear results"))
        self.actionClear_all.setText(_translate("MainWindow", "Clear all"))
        self.actionParameters.setText(_translate("MainWindow", "Parameters"))
        self.actionParameters.setToolTip(_translate("MainWindow", "Parameter settings"))
        self.actionRescale.setText(_translate("MainWindow", "Rescale"))
        self.actionRescale.setToolTip(_translate("MainWindow", "Rescale data to current window size"))

try:
    if __name__ == "__main__":
        import sys
        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        ui = Ui_MainWindow()
        ui.setupUi(MainWindow)
        MainWindow.show()
        sys.exit(app.exec())
except Exception as e:
    try:                                # display error message in a message box
        ui.canvas.messageBox('User notification', 'Program ended by user or terminated due to unexpected error.')
    finally:                            # Print the message for a case the message window is unavailable
        print('>> Program ended by user or terminated due to unexpected error:', f'>> {e}', sep = '\n') 