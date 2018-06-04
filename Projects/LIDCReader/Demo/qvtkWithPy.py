from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import sys
import vtk


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(603, 553)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.gridlayout = QtWidgets.QGridLayout(self.centralWidget)
        self.vtkWidget = QVTKRenderWindowInteractor(self.centralWidget)
        self.gridlayout.addWidget(self.vtkWidget, 0, 0, 100, 100)

        MainWindow.setCentralWidget(self.centralWidget)

class MyInteractorStyle(vtk.vtkInteractorStyleTrackballCamera):

    def __init__(self, parent=None):
        self.AddObserver("MiddleButtonPressEvent", self.middleButtonPressEvent)
        self.AddObserver("MiddleButtonReleaseEvent", self.middleButtonReleaseEvent)

    def middleButtonPressEvent(self, obj, event):
        print("Middle Button pressed")
        self.OnMiddleButtonDown()
        return

    def middleButtonReleaseEvent(self, obj, event):
        print("Middle Button released")
        self.OnMiddleButtonUp()
        return

class SimpleView(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ren = vtk.vtkRenderer()
        self.ui.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        self.iren = self.ui.vtkWidget.GetRenderWindow().GetInteractor()


        reader =  vtk.vtkDICOMImageReader()
        reader.SetFileName("F:/Dicom/100098.dcm")
        reader.Update()

        viewer = vtk.vtkImageViewer2()
        viewer.SetInputConnection(reader.GetOutputPort())

        self.ui.vtkWidget.SetInteractorStyle(vtk.vtkInteractorStyleImage())


        viewer.SetRenderWindow(self.ui.vtkWidget.GetRenderWindow())
        viewer.Render()
        viewer.GetRenderer().ResetCamera()
        self.ui.vtkWidget.GetRenderWindow().Render()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SimpleView()
    window.show()
    window.setWindowTitle("QVTK+pyQt 测试")
    window.iren.Initialize()  # Need this line to actually show the render inside Qt
    sys.exit(app.exec_())