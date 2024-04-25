from PyQt6 import QtCore, QtGui, QtWidgets
from algorithms import *
from draw import Draw
from i_o import IO
from prettytable import PrettyTable
from typing import Callable

class Ui_MainWindow(object):
    '''
    - Class for program´s main window and connecting operations in other classes.

    - Methods:
        - setupUi() - Main function called by the constructor
        - openClick() - Loads polygon data from file chosen via a file dialog
        - generalizationProcess(algo: Callable, algo_name: str) - Checks if data is usable, prepares it, calls given MBR algorithm, refreshes saved data, used by next 5 functions:
            - maerClick() - Calls minimum area enclosing rectangle algorithm´s workflow
            - pcaClick() - Calls principal component analysis algorithm´s workflow
            - longestEdgeClick() - Calls Longest edge algorithm´s workflow
            - wallAvgClick() - Calls Wall average algorithm´s workflow
            - weightedClick() - Calls weighted bisector algorithm´s workflow
        - ratingClick() - Computers main direction detection efficiency, shows its statistics and saves statistics table to a file chosen via a file dialog
        - rescaleClick() - Rescales current polygon data to the size of the window
        - clearAllClick() - Clears all data from the canvas and the program´s memory
        - clearResClick() - clears only the results
        - exitClick() - Ends the program
        - retranslateUi() - Method created by Qt, necessary for running the program
    '''
    def setupUi(self, main_window) -> None:
        main_window.setObjectName("main_window")
        main_window.resize(1920, 1080)
        self.central_widget = QtWidgets.QWidget(parent=main_window)
        self.central_widget.setObjectName("central_widget")
        self.horizontal_layout = QtWidgets.QHBoxLayout(self.central_widget)
        self.horizontal_layout.setObjectName("horizontal_layout")
        self.canvas = Draw(parent=self.central_widget)
        self.canvas.setEnabled(True)
        self.canvas.setMinimumSize(QtCore.QSize(800, 600))
        self.canvas.setMaximumSize(QtCore.QSize(10000, 10000))
        self.canvas.setBaseSize(QtCore.QSize(1920, 1080))
        self.canvas.setObjectName("canvas")
        self.horizontal_layout.addWidget(self.canvas)
        main_window.setCentralWidget(self.central_widget)
        self.menu_bar = QtWidgets.QMenuBar(parent=main_window)
        self.menu_bar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menu_bar.setObjectName("menu_bar")
        self.menu_file = QtWidgets.QMenu(parent=self.menu_bar)
        self.menu_file.setObjectName("menu_file")
        self.menu_simplify = QtWidgets.QMenu(parent=self.menu_bar)
        self.menu_simplify.setObjectName("menu_simplify")
        self.menu_view = QtWidgets.QMenu(parent=self.menu_bar)
        self.menu_view.setObjectName("menu_view")
        main_window.setMenuBar(self.menu_bar)
        self.status_bar = QtWidgets.QStatusBar(parent=main_window)
        self.status_bar.setObjectName("status_bar")
        main_window.setStatusBar(self.status_bar)
        self.tool_bar = QtWidgets.QToolBar(parent=main_window)
        self.tool_bar.setObjectName("tool_bar")
        main_window.addToolBar(QtCore.Qt.ToolBarArea.TopToolBarArea, self.tool_bar)
        self.action_open = QtGui.QAction(parent=main_window)

        icon = QtGui.QIcon()                                                           # Icon creation
        icon.addPixmap(QtGui.QPixmap("icons/open_file.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.action_open.setIcon(icon)
        self.action_open.setObjectName("action_open")
        self.action_exit = QtGui.QAction(parent=main_window)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("icons/exit.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.action_exit.setIcon(icon1)
        self.action_exit.setObjectName("action_exit")
        self.actionMinBoundingRectangle = QtGui.QAction(parent=main_window)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("icons/maer.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionMinBoundingRectangle.setIcon(icon2)
        self.actionMinBoundingRectangle.setObjectName("actionMinBoundingRectangle")
        self.actionPCA = QtGui.QAction(parent=main_window)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("icons/pca.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionPCA.setIcon(icon3)
        self.actionPCA.setObjectName("actionPCA")
        self.actionClearResults = QtGui.QAction(parent=main_window)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("icons/clear_ch.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionClearResults.setIcon(icon4)
        self.actionClearResults.setObjectName("actionClearResults")
        self.actionClear_all = QtGui.QAction(parent=main_window)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("icons/clear_er.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionClear_all.setIcon(icon5)
        self.actionClear_all.setObjectName("actionClear_all")
        self.actionRescale = QtGui.QAction(parent=main_window)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("icons/resize.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionRescale.setIcon(icon6)
        self.actionRescale.setMenuRole(QtGui.QAction.MenuRole.NoRole)
        self.actionRescale.setObjectName("actionRescale")
        self.actionLongestEdge = QtGui.QAction(parent=main_window)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap("icons/longestedge.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionLongestEdge.setIcon(icon7)
        self.actionLongestEdge.setMenuRole(QtGui.QAction.MenuRole.NoRole)
        self.actionLongestEdge.setObjectName("actionLongestEdge")
        self.actionWallAverage = QtGui.QAction(parent=main_window)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap("icons/wa.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionWallAverage.setIcon(icon8)
        self.actionWallAverage.setMenuRole(QtGui.QAction.MenuRole.NoRole)
        self.actionWallAverage.setObjectName("actionWallAverage")
        self.actionWeightedBisector = QtGui.QAction(parent=main_window)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap("icons/weightedbisector.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionWeightedBisector.setIcon(icon9)
        self.actionWeightedBisector.setMenuRole(QtGui.QAction.MenuRole.NoRole)
        self.actionWeightedBisector.setObjectName("actionWeightedBisector")
        self.actionRating = QtGui.QAction(parent=main_window)
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap("icons/rating.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionRating.setIcon(icon10)
        self.actionRating.setMenuRole(QtGui.QAction.MenuRole.NoRole)
        self.actionRating.setObjectName("actionRating")

        self.menu_file.addAction(self.action_open)
        self.menu_file.addSeparator()
        self.menu_file.addAction(self.action_exit)
        self.menu_simplify.addAction(self.actionMinBoundingRectangle)
        self.menu_simplify.addAction(self.actionPCA)
        self.menu_simplify.addAction(self.actionLongestEdge)
        self.menu_simplify.addAction(self.actionWallAverage)
        self.menu_simplify.addAction(self.actionWeightedBisector)
        self.menu_view.addAction(self.actionRating)
        self.menu_view.addSeparator()
        self.menu_view.addAction(self.actionRescale)
        self.menu_view.addAction(self.actionClearResults)
        self.menu_view.addSeparator()
        self.menu_view.addAction(self.actionClear_all)
        self.menu_bar.addAction(self.menu_file.menuAction())
        self.menu_bar.addAction(self.menu_simplify.menuAction())
        self.menu_bar.addAction(self.menu_view.menuAction())
        self.tool_bar.addAction(self.action_open)
        self.tool_bar.addSeparator()
        self.tool_bar.addAction(self.actionMinBoundingRectangle)
        self.tool_bar.addAction(self.actionPCA)
        self.tool_bar.addAction(self.actionLongestEdge)
        self.tool_bar.addAction(self.actionWallAverage)
        self.tool_bar.addAction(self.actionWeightedBisector)
        self.tool_bar.addSeparator()
        self.tool_bar.addAction(self.actionRating)
        self.tool_bar.addSeparator()
        self.tool_bar.addAction(self.actionRescale)
        self.tool_bar.addAction(self.actionClearResults)
        self.tool_bar.addSeparator()
        self.tool_bar.addAction(self.actionClear_all)
        self.tool_bar.addSeparator()
        self.tool_bar.addAction(self.action_exit)
        self.retranslateUi(main_window)

        self.action_open.triggered.connect(self.openClick)                              # define actions-slots relations                                 
        self.actionMinBoundingRectangle.triggered.connect(self.maerClick)        
        self.actionPCA.triggered.connect(self.pcaClick)         
        self.actionLongestEdge.triggered.connect(self.longestEdgeClick)
        self.actionWallAverage.triggered.connect(self.wallAvgClick)  
        self.actionWeightedBisector.triggered.connect(self.weightedClick)                        
        self.actionRating.triggered.connect(self.ratingClick)         
        self.actionRescale.triggered.connect(self.rescaleClick) 
        self.actionClearResults.triggered.connect(self.clearResClick) 
        self.actionClear_all.triggered.connect(self.clearAllClick) 
        self.action_exit.triggered.connect(self.exitClick) 
        QtCore.QMetaObject.connectSlotsByName(main_window)                              # connect actions to slots 

        self.a = Algorithms()                                                           # easier access to processing

    def generalizationProcess(self, algo : Callable, algo_name : str) -> None:
        blds = self.canvas.getBlds()                                                    # get buildings
        if (len(blds) == 1) and (len(blds[1]) == 0):                                    # No polygons exist
            self.canvas.messageBox('Error', 'Empty input polygon.')
            return

        FrameworkError.resetCount()                                                     # reset error counter
        try:
            mbrs = self.a.generalize(algo, blds)                                        # simplify buildings
        except InvalidBldError:
            self.canvas.messageBox('Error', 'Not enough vertices in input building(s).')
            return

        self.canvas.setMBRs(mbrs)                                                       # update MBRs
        self.canvas.repaint()                                                           # refresh the screen

        error_len = FrameworkError.getCount()                                           # Number of failed MBR calculations
        title = f'{algo_name} algorithm´s result'
        if (error_len > 0) and (error_len == len(blds)):                                # All MBR creations failed
            title = 'Error'
            text = f'Failed to compute any MBR due to framework issues.\n\nThe issues were caused by inaccuraccies \
of float numbers building up in the algorithm. Computing based on pixel coordinates worsened the effect. \
\n\nRemaining buildings were processed successfully.'

        elif error_len:                                                                 # not all MBR creations failed
            text = f'Failed to compute MBR of {error_len} buildings due to framework issues.\n\nThe issues were caused \
by inaccuraccies of float numbers building up in the algorithm. Computing based on pixel coordinates worsened the effect. \
\n\nRemaining buildings were processed successfully.'

        else:                                                                           # No fails occurred
            text = f'Successfully processed all buildings.' 

        self.canvas.messageBox(title, text)                                             # display a result message 

    def openClick(self) -> None:
        file = QFileDialog.getOpenFileName(caption = 'Open File', filter = 'JSON compatible (*.txt *.json *.geojson)')[0]
        io = IO()           # Input output framework
        if file != '':      # If a file name was chosen
            buildings = io.loadBlds(file, self.canvas.getWidth(), self.canvas.getHeight())       # Load polygons and stretch them to current widget´s size
            if buildings:
                self.canvas.setBlds(buildings)                                                   # update data
                self.canvas.clearMBRs()
                self.canvas.messageBox('Success', 'Input buildings loaded succesfully.')
            else:
                self.canvas.messageBox('Error', 'Failed to load buildings.')

    def maerClick(self) -> None:
        self.generalizationProcess(self.a.MAER, 'MAER')

    def pcaClick(self) -> None:
        self.generalizationProcess(self.a.PCA, 'PCA')
        
    def longestEdgeClick(self) -> None:
        self.generalizationProcess(self.a.LE, 'Longest Edge')

    def wallAvgClick(self) -> None:
        self.generalizationProcess(self.a.WA, 'Wall average')

    def weightedClick(self) -> None:
        self.generalizationProcess(self.a.WB, 'Weighted Bisector')

    def ratingClick(self) -> None:
        blds = self.canvas.getBlds()
        mbrs = self.canvas.getMBRs()
        if (not blds) or (not mbrs):
            self.canvas.messageBox('Error', 'No buildings or MBRs to rate.')
            return

        common_k = set([key for key in blds.keys()]) & set([key for key in mbrs.keys()])        # Keys present in both buildings and MBR's dictionaries
        if common_k:
            table, stats = self.a.rateAll(blds, mbrs, common_k)                                 # Compute the efficiency
            self.canvas.messageBox('Success', f'Successfully calculated statistics for {len(common_k)} building-MBR pairs:\n\n\
Mean Δ1 [°]: {stats[0]}\nMean Δ2 [°]: {stats[1]}\n\nPairs where |Δ1 < 10°| [%]: {stats[2]}\nPairs where |Δ2 < 10°| [%]: {stats[3]}\n\t\
Pairs where both |Δ1 < 10°| and |Δ2 < 10°| [%]: {stats[4]}\n\nSelect a file to save statistics table into after closing this window.')     # Display efficiency statistics

            file = QFileDialog.getSaveFileName(caption = 'Save to file', filter = 'Text file (*.txt)')[0]           # Save the table via file dialog
            if file:
                io = IO()
                saved = io.saveTable(file, table)
                if saved:
                    self.canvas.messageBox('Success', 'Data saved to file.')
                else:
                    self.canvas.messageBox('Error', 'Failed to save data.')
        else:
            self.canvas.messageBox('Error', 'No buildings with assigned MBR.')
            return

    def rescaleClick(self) -> None:
        if len(self.canvas.getBlds()[1]) > 2:           # Polygon has 3 or more unique vertices                     
            blds, mbrs = self.a.rescaleAll(self.canvas.getBlds(), self.canvas.getMBRs(), self.canvas.getWidth(), self.canvas.getHeight())
            self.canvas.setBlds(blds)                   # Update the widget
            self.canvas.setMBRs(mbrs)
        else:
            self.canvas.messageBox('Error', 'No polygons to rescale.')     

    def clearResClick(self) -> None:
        if len(self.canvas.getMBRs()) > 0:              # No data to clear
            self.canvas.clearMBRs()
        else:
            self.canvas.messageBox('Operation unavailable', 'No building generalizations to clear.')

    def clearAllClick(self) -> None:
        self.canvas.clearData()

    def exitClick(self) -> None:
        app.quit()

    def retranslateUi(self, main_window) -> None:
        _translate = QtCore.QCoreApplication.translate
        main_window.setWindowTitle(_translate("main_window", "Simplify Buildings"))
        self.menu_file.setTitle(_translate("main_window", "File"))
        self.menu_simplify.setTitle(_translate("main_window", "Simplify"))
        self.menu_view.setTitle(_translate("main_window", "View"))
        self.tool_bar.setWindowTitle(_translate("main_window", "tool_bar"))
        self.action_open.setText(_translate("main_window", "Open"))
        self.action_open.setToolTip(_translate("main_window", "Open File"))
        self.action_exit.setText(_translate("main_window", "Exit"))
        self.action_exit.setToolTip(_translate("main_window", "Close Application"))
        self.actionMinBoundingRectangle.setText(_translate("main_window", "Min. Bounding Rectangle"))
        self.actionMinBoundingRectangle.setToolTip(_translate("main_window", "Simplify building using Minimum Bounding Rectangle"))
        self.actionPCA.setText(_translate("main_window", "PCA"))
        self.actionPCA.setToolTip(_translate("main_window", "Simplify building using PCA"))
        self.actionClearResults.setText(_translate("main_window", "Clear results"))
        self.actionClear_all.setText(_translate("main_window", "Clear all"))
        self.actionRescale.setText(_translate("main_window", "Rescale"))
        self.actionRescale.setToolTip(_translate("main_window", "Stretch data to widgets current extent"))
        self.actionLongestEdge.setText(_translate("main_window", "LongestEdge"))
        self.actionLongestEdge.setToolTip(_translate("main_window", "Simplify building using Longest Edge algorithm"))
        self.actionWallAverage.setText(_translate("main_window", "Wall Average"))
        self.actionWallAverage.setToolTip(_translate("main_window", "Simplify building using Wall Average algorithm"))
        self.actionWeightedBisector.setText(_translate("main_window", "Weighted Bisector"))
        self.actionWeightedBisector.setToolTip(_translate("main_window", "Simplify building using Weighted Bisector algorithm"))
        self.actionRating.setText(_translate("main_window", "Rating"))
        self.actionRating.setToolTip(_translate("main_window", "Rate algorithm efficiency"))
try:
    if __name__ == "__main__":
        import sys
        app = QtWidgets.QApplication(sys.argv)
        main_window = QtWidgets.QMainWindow()
        ui = Ui_MainWindow()
        ui.setupUi(main_window)
        main_window.show()
        sys.exit(app.exec())
except Exception as e: 
    try:                                # display the message in a message box
        ui.canvas.messageBox('User notification', 'Program ended by user or terminated due to unexpected error.')
    finally:                            # Print the message for a case the message window is unavailable
        print('>> Program ended by user or terminated due to unexpected error:', f'>> {e}', sep = '\n')  