from PyQt6 import QtCore, QtGui, QtWidgets
from coordDialog import UiDialog
from input_output import IO
from draw import Draw
from algorithms import *
import sys

class UiMainWindow():
    '''
    - Class for program´s main window and connecting operations in other classes.

    - Methods (Each method in any file without '->' returns None):
        - setupUi() - Main function called by the constructor
        - openClick() - Loads polygon data from file chosen via a file dialog
        - pointPolygonClick() - Switches between drawing the tested point and adding a point to the polygon
        - clearClick() - Clears data
        - exitClick() - Ends the program
        - rayClick() -  Checks if data is usable, prepares it, calls Ray Tracing algorithm, refreshes saved data
        - windingClick() - Checks if data is usable, prepares it, calls Winding Number algorithm, refreshes saved data
        - rescaleClick() - Rescales current polygon data to the size of thewindow
        - saveClick() - Saves polygon data to file chosen via a file dialog
        - retranslateUi() - Method created by Qt, necessary for running the program
    '''
    def setupUi(self, main_window):
        main_window.setObjectName("main_window")                                                                    
        main_window.resize(804, 608)
        main_window.setMinimumSize(QtCore.QSize(800, 600))
        main_window.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.DefaultContextMenu)
        self.central_widget = QtWidgets.QWidget(parent=main_window)
        self.central_widget.setObjectName("central_widget")
        self.horizontal_layout = QtWidgets.QHBoxLayout(self.central_widget)
        self.horizontal_layout.setObjectName("horizontal_layout")
        self.canvas = Draw(parent=self.central_widget)
        self.canvas.setObjectName("canvas")
        self.horizontal_layout.addWidget(self.canvas)
        main_window.setCentralWidget(self.central_widget)
        self.menu_bar = QtWidgets.QMenuBar(parent=main_window)
        self.menu_bar.setGeometry(QtCore.QRect(0, 0, 804, 22))
        self.menu_bar.setObjectName("menu_bar")
        self.menu_file = QtWidgets.QMenu(parent=self.menu_bar)
        self.menu_file.setObjectName("menu_file")
        self.menu_input = QtWidgets.QMenu(parent=self.menu_bar)
        self.menu_input.setObjectName("menu_input")
        self.menu_analyze = QtWidgets.QMenu(parent=self.menu_bar)
        self.menu_analyze.setObjectName("menu_analyze")
        main_window.setMenuBar(self.menu_bar)
        self.status_bar = QtWidgets.QStatusBar(parent=main_window)
        self.status_bar.setObjectName("status_bar")
        main_window.setStatusBar(self.status_bar)
        self.tool_bar = QtWidgets.QToolBar(parent=main_window)
        self.tool_bar.setObjectName("tool_bar")
        main_window.addToolBar(QtCore.Qt.ToolBarArea.TopToolBarArea, self.tool_bar)
        self.actionOpen = QtGui.QAction(parent=main_window)

        icon = QtGui.QIcon()                                                                                        # Icon creation
        icon.addPixmap(QtGui.QPixmap("icons/open_file.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionOpen.setIcon(icon)
        self.actionOpen.setObjectName("actionOpen")
        self.actionExit = QtGui.QAction(parent=main_window)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("icons/exit.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionExit.setIcon(icon1)
        self.actionExit.setObjectName("actionExit")
        self.actionPoint = QtGui.QAction(parent=main_window)
        self.actionPoint.setCheckable(True)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("icons/pointpol.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionPoint.setIcon(icon2)
        self.actionPoint.setObjectName("actionPoint")
        self.actionClear = QtGui.QAction(parent=main_window)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("icons/clear_all.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionClear.setIcon(icon3)
        self.actionClear.setObjectName("actionClear")
        self.actionRayCrossing = QtGui.QAction(parent=main_window)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("icons/ray.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionRayCrossing.setIcon(icon4)
        self.actionRayCrossing.setObjectName("actionRayCrossing")
        self.actionWindingNumber = QtGui.QAction(parent=main_window)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("icons/winding.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionWindingNumber.setIcon(icon5)
        self.actionWindingNumber.setObjectName("actionWindingNumber")
        self.actionSave = QtGui.QAction(parent=main_window)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("icons/save.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionSave.setIcon(icon6)
        self.actionSave.setObjectName("actionSave")
        self.actionPointLocation = QtGui.QAction(parent=main_window)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap("icons/pin.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionPointLocation.setIcon(icon7)
        self.actionPointLocation.setMenuRole(QtGui.QAction.MenuRole.NoRole)
        self.actionPointLocation.setObjectName("actionPointLocation")
        self.actionResizeData = QtGui.QAction(parent=main_window)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap("icons/resize.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionResizeData.setIcon(icon8)
        self.actionResizeData.setMenuRole(QtGui.QAction.MenuRole.NoRole)
        self.actionResizeData.setObjectName("actionResizeData")

        self.menu_file.addAction(self.actionOpen)
        self.menu_file.addAction(self.actionSave)
        self.menu_file.addSeparator()
        self.menu_file.addAction(self.actionExit)

        self.menu_input.addAction(self.actionPoint)
        self.menu_input.addAction(self.actionPointLocation)
        self.menu_input.addSeparator()
        self.menu_input.addAction(self.actionResizeData)
        self.menu_input.addAction(self.actionClear)

        self.menu_analyze.addAction(self.actionRayCrossing)
        self.menu_analyze.addAction(self.actionWindingNumber)

        self.menu_bar.addAction(self.menu_file.menuAction())
        self.menu_bar.addAction(self.menu_input.menuAction())
        self.menu_bar.addAction(self.menu_analyze.menuAction())

        self.tool_bar.addAction(self.actionOpen)
        self.tool_bar.addAction(self.actionSave)
        self.tool_bar.addSeparator()
        self.tool_bar.addAction(self.actionPoint)
        self.tool_bar.addAction(self.actionPointLocation)
        self.tool_bar.addSeparator()
        self.tool_bar.addAction(self.actionRayCrossing)
        self.tool_bar.addAction(self.actionWindingNumber)
        self.tool_bar.addSeparator()
        self.tool_bar.addAction(self.actionResizeData)
        self.tool_bar.addAction(self.actionClear)
        self.tool_bar.addSeparator()
        self.tool_bar.addAction(self.actionExit)
        self.tool_bar.addSeparator()

        self.retranslateUi(main_window)
        self.actionSave.triggered.connect(self.saveClick)                       # connection between icon actions and corresponding functions              
        self.actionOpen.triggered.connect(self.openClick)                            
        self.actionPoint.triggered.connect(self.pointPolygonClick) 
        self.actionClear.triggered.connect(self.clearClick) 
        self.actionExit.triggered.connect(self.exitClick) 
        self.actionPointLocation.triggered.connect(self.pntCoordClick) 
        self.actionRayCrossing.triggered.connect(self.rayClick) 
        self.actionWindingNumber.triggered.connect(self.windingClick) 
        self.actionResizeData.triggered.connect(self.rescaleClick)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def openClick(self):
        file = QFileDialog.getOpenFileName(caption = 'Open File', filter = 'JSON compatible (*.txt *.json *.geojson)')[0]
        io = IO()           # Input output framework
        if file != '':      # If a file name was chosen
            polygons = io.loadPolygons(file, self.canvas.getWidth(), self.canvas.getHeight())       # Load polygons and stretch them to current widget´s size
            if polygons:
                self.canvas.setHighlighted()                                                        # remove list of keys of polygons to highlight
                self.canvas.setPolygons(polygons)                                                   # update data
                self.canvas.messageBox('Success', 'Input data loaded succesfully.')
            else:
                self.canvas.messageBox('Error', 'Failed to load data.')

    def pointPolygonClick(self):
        self.canvas.switchDrawing()     

    def clearClick(self):
        self.canvas.clearData()

    def exitClick(self):
        app.quit()

    def rayClick(self):
        polygons = self.canvas.getPolygons()
        if (len(polygons) == 1) and (len(polygons[1][1]) == 0):                 # No polygons exist
            self.canvas.messageBox('Error', 'Empty input polygon.')
            return

        a = Algorithms()
        for pol in polygons.values():
            if len(pol[1]) < 3:                                                 # A polygon with less than # vertices ocured
                self.canvas.messageBox('Error', 'Not enough vertices in input polygon(s).')
                return

        q = self.canvas.getQ()                                                  # get tested point
        polygons = a.rayCrossingAll(q, polygons)                                # run analysis

        if len(polygons) > 0:                                                   # point inside
            self.canvas.setHighlighted([key for key in polygons.keys()])        # highlight positively tested polygons
            self.canvas.setPolygons(polygons)
            text = 'Point inside polygon.' 
        else:
            self.canvas.setHighlighted()
            text = 'Point outside polygon(s).'      
        self.canvas.messageBox('Ray Crossing´s result', text)

    def windingClick(self):
        polygons = self.canvas.getPolygons()
        if (len(polygons) == 1) and (len(polygons[1][1]) == 0):
            self.canvas.messageBox('Error', 'Empty input polygon.')
            return

        a = Algorithms()
        for pol in polygons.values():
            if len(pol[1]) < 3:
                self.canvas.messageBox('Error', 'Not enough vertices in input polygon(s).')
                return

        q = self.canvas.getQ()      
        polygons, pnt_pos = a.windingNumAll(q, polygons)     

        if len(polygons) > 0:
            text = 'Point '                                                     # Create a text string for message window
            relations = {0 : 'inside polygon(s): ', 1 : 'on edge of polygon(s): ', 2 : 'is a vertex of polygon(s): '}
            for key, val in pnt_pos.items():
                if val:
                    text = text + relations[key] + ', '.join(val) + ', \n'
            text = text[ : -3] + '.'
            
            self.canvas.setHighlighted([key for key in polygons.keys()])        # highlight positively tested polygons
            self.canvas.setPolygons(polygons)
        else:
            self.canvas.setHighlighted()
            text = 'Point outside polygon(s).'      
        self.canvas.messageBox('Winding Numbers´ result', text)

    def pntCoordClick(self):
        if self.canvas.getAddV():                                               # Switch to drawing the tested point if necessary
            self.canvas.switchDrawing()

        ui = UiDialog()                                                         # Create pop up window to input float coordinates
        ui.exec()
        new_coords = ui.getCoords()

        if new_coords != (None, None):
            try:                                                                # Check if convertible to float
                x = float(new_coords[0])
                y = float(new_coords[1])
            except ValueError:                                                  # input is not a number
                self.canvas.messageBox('Error', 'Input can´t be transformed to coordinates.')
                return
            else:
                if (x not in range (2000000000)) or (y not in range (2000000000)):      # input number too big
                    self.canvas.messageBox('Error', 'Coordinates not in accepted range.')
                    return
                
                self.canvas.q.setX(float(new_coords[0]))                        # Set point´s new coordinates
                self.canvas.q.setY(float(new_coords[1]))
                self.canvas.repaint()                                           # Refresh the widget

    def rescaleClick(self):
        if len(self.canvas.getPolygons()[1][1]) > 2:                            # Polygon has Less than 3 vertices                     
            a = Algorithms()
            polygons = a.rescale(self.canvas.getPolygons(), self.canvas.getWidth(), self.canvas.getHeight())
            self.canvas.setPolygons(polygons)
        else:
            self.canvas.messageBox('Error', 'No polygons to rescale.')               

    def saveClick(self):
        polygons = self.canvas.getPolygons()
        if (len(polygons) == 1) and (len(polygons[1][1]) == 0):                 # No data to save
            self.canvas.messageBox('Error', 'Empty polygon.')
            return

        poly_copy = {key : pol for key, pol in polygons.items()}                # Create a physical copy

        indexes = []
        for key, pol in poly_copy.items():
            if len(pol[1]) < 3:
                indexes.append(key)
        for key in indexes:                                                     # Remove polygons with not enough vertices
            poly_copy.pop(key)

        file = QFileDialog.getSaveFileName(caption = 'Open File', filter = 'JSON compatible (*.txt *.json *.geojson)')[0]
        if file != '':
            io = IO()
            saved = io.savePolygons(file, poly_copy)
            if saved:
                self.canvas.messageBox('Success', 'Data saved to file.')
            else:
                self.canvas.messageBox('Error', 'Failed to save data.')
            
    def retranslateUi(self, main_window):
        translate_func = QtCore.QCoreApplication.translate
        main_window.setWindowTitle(translate_func("main_window", "Point and polygon position"))
        self.menu_file.setTitle(translate_func("main_window", "File"))
        self.menu_input.setTitle(translate_func("main_window", "Input"))
        self.menu_analyze.setTitle(translate_func("main_window", "Analyze"))
        self.tool_bar.setWindowTitle(translate_func("main_window", "tool_bar"))
        self.actionOpen.setText(translate_func("main_window", "Open"))
        self.actionOpen.setToolTip(translate_func("main_window", "Open a file"))
        self.actionExit.setText(translate_func("main_window", "Exit"))
        self.actionExit.setToolTip(translate_func("main_window", "Exit the application"))
        self.actionPoint.setText(translate_func("main_window", "Point/Polygon"))
        self.actionPoint.setToolTip(translate_func("main_window", "Create a point/polygon"))
        self.actionClear.setText(translate_func("main_window", "Clear"))
        self.actionClear.setToolTip(translate_func("main_window", "Remove data"))
        self.actionRayCrossing.setText(translate_func("main_window", "Ray Crossing Algorithm"))
        self.actionRayCrossing.setToolTip(translate_func("main_window", "Use ray crossing algorithm"))
        self.actionWindingNumber.setText(translate_func("main_window", "Winding Number Algorithm"))
        self.actionWindingNumber.setToolTip(translate_func("main_window", "Use winding number algorithm"))
        self.actionSave.setText(translate_func("main_window", "Save"))
        self.actionSave.setToolTip(translate_func("main_window", "Save current polygons"))
        self.actionPointLocation.setText(translate_func("main_window", "Point Location"))
        self.actionPointLocation.setToolTip(translate_func("main_window", "Input float coordinates"))
        self.actionResizeData.setText(translate_func("main_window", "Resize Data"))
        self.actionResizeData.setToolTip(translate_func("main_window", "Stretch polygons to current screen size"))

try:                                                    # run the program and display occurring errors
    if __name__ == "__main__":
        app = QtWidgets.QApplication(sys.argv)
        main_window = QtWidgets.QMainWindow()
        ui = UiMainWindow()
        ui.setupUi(main_window)
        main_window.show()
        sys.exit(app.exec())
except Exception as e: 
    try:        # display the message in a message box
        ui.canvas.messageBox('User notification', 'Program ended by user or terminated due to unexpected error.')
    finally:            # Print the message for a case the message window is unavailable
        print('>> Program ended by user or terminated due to unexpected error:', f'>> {e}', sep = '\n')     
