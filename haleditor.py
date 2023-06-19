import sys, os
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsView
from PyQt5.QtGui import QPainter, QPen, QColor, QStandardItem, QStandardItemModel
from PyQt5.QtCore import Qt, QPointF, pyqtSignal
from ui_haleditor import Ui_HalEditor
import halparser

COMPONENTSFOLDER = "/home/pi/dev/linuxcnc/src/hal/components/"

class Object:
    NAME = ""
    PINS = [{}]
    def __init__(self, name, pins):
        self.NAME = name
        self.PINS = pins

class Element():
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

class Connection:
    def __init__(self, start, end):
        self.start = start
        self.end = end

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_HalEditor()
        self.ui.setupUi(self)

        self.setWindowTitle("HAL Editor: <unknown>")
        self.setGeometry(100, 100, 1024, 768)

        self.scene = QGraphicsScene(self)
        self.ui.graphicsView.setRenderHint(QPainter.Antialiasing)
        self.ui.graphicsView.setScene(self.scene)

        self.elements = []
        self.connections = []
        self.current_element = None
        self.current_line = None

        pins = ({'dir': 'in', 'name': 'in_', 'type': 'float', 'description': '"Input value";'},
                {'dir': 'out', 'name': 'out', 'type': 'float', 'description': '"Output value";'},
                {'dir': 'in', 'name': 'enable', 'type': 'bit', 'description': '"When TRUE, copy in to out";'},
                {'dir': 'in', 'name': 'enable', 'type': 'bit', 'description': '"When TRUE, copy in to out";'})
        andsch = Object("TEST", pins)

        self.create_object(andsch, 0, 0)

        self.ui.treeView.clicked.connect(self.handleItemClicked)

        # Создание модели данных
        self.model = QStandardItemModel()

        last_comp = QStandardItem("Последние")
        last_comp.setDragEnabled(False)
        self.model.appendRow(last_comp)
        last_comp.setEditable(False)

        sys_comp = QStandardItem("Системные")
        sys_comp.setDragEnabled(False)
        self.model.appendRow(sys_comp)
        sys_comp.setEditable(False)

        logic_comp = QStandardItem("Логические")
        self.model.appendRow(logic_comp)
        logic_comp.setDragEnabled(False)
        logic_comp.setEditable(False)

        arithm_comp = QStandardItem("Арифметические")
        self.model.appendRow(arithm_comp)
        arithm_comp.setDragEnabled(False)
        arithm_comp.setEditable(False)

        types_comp = QStandardItem("Приведение типов")
        self.model.appendRow(types_comp)
        types_comp.setDragEnabled(False)
        types_comp.setEditable(False)

        drivers_comp = QStandardItem("Драйверы")
        self.model.appendRow(drivers_comp)
        drivers_comp.setDragEnabled(False)
        drivers_comp.setEditable(False)

        other_comp = QStandardItem("Другие")
        self.model.appendRow(other_comp)
        other_comp.setDragEnabled(False)
        other_comp.setEditable(False)

        components_list, noparsed = halparser.load_components(COMPONENTSFOLDER)
        self.complist = components_list

        print("Следующие компоненты не могут быть использованы: \n")
        for item in noparsed:
            print(item)
            
        for key, value in components_list.items():
            ind = 0
            for component in value:
                if value == "": continue
                item_s = component.split(".")[0]

                item = QStandardItem(item_s)
                if (key == "system"):
                    sys_comp.appendRow(item)
                elif (key == "logic"):
                    logic_comp.appendRow(item)
                elif (key == "arithm"):
                    arithm_comp.appendRow(item)
                elif (key == "types"):
                    types_comp.appendRow(item)
                elif (key == "other"):
                    other_comp.appendRow(item)
                
                pins, inputs, outputs = halparser.component_parse(COMPONENTSFOLDER + component)
                pinind = 0

                item.setData(ind, Qt.UserRole)
                item.setData(key, 260)
                item.setEditable(False)

                for pin in pins:
                    subitem = QStandardItem(pin["name"])
                    if (pin["dir"] == "in"):
                        subitem.setForeground(Qt.blue)
                    elif (pin["dir"] == "out"):
                        subitem.setForeground(Qt.red)
                    elif (pin["dir"] == "io"):
                        subitem.setForeground(Qt.green)
                    item.appendRow(subitem)
                    subitem.setEditable(False)
                    pinind = pinind + 1
                ind = ind + 1

        self.ui.treeView.setModel(self.model)
        self.model.setHeaderData(0, Qt.Horizontal, "Компоненты HAL")

    def handleItemClicked(self, index:QtCore.QModelIndex):
        item = self.model.itemFromIndex(index)
        component = self.complist[item.data(260)][item.data(Qt.UserRole)]
        pins, inputs, outputs = halparser.component_parse(COMPONENTSFOLDER + component)
        obj = Object(component.split(".")[0], pins)

        self.create_object(obj, 200, 200)

    def create_object(self, sch:Object, objx, objy):
        pindist = 15

        ins = 0
        outs = 0
        for pin in sch.PINS:
            text_item = QtWidgets.QGraphicsTextItem(pin["name"])
            text_item.setScale(0.5)
            if (pin["dir"] == "in"):
                self.create_pin(objx, objy + ins * pindist, 0)

                text_item.setPos(objx + 12, objy + ins * pindist - 9)
                ins = ins + 1
            else:
                if (pin["dir"] == "out"): typ = 1
                else: typ = 2
                self.create_pin(objx, objy + outs * pindist, typ)

                text_item.setPos(objx + 82, objy + outs * pindist - 9)
                outs = outs + 1

            text_item.setDefaultTextColor(Qt.gray)
            self.scene.addItem(text_item)

        if (ins > outs): length = ins
        else: length = outs
        
        rectx = objx + 27.5
        recty = objy - 2.5
        rectwidth = 50
        rectheight = 10 + (pindist * (length-1))
        element = Element(rectx, recty, rectwidth, rectheight)
        self.elements.append(element)
        self.scene.addRect(rectx, recty, rectwidth, rectheight, pen=QPen(Qt.black), brush=QColor("white"))

        text_item = QtWidgets.QGraphicsTextItem(sch.NAME)
        text_item.setScale(0.9)
        text_item.setPos(objx + 35, objy - 22)
        text_item.setDefaultTextColor(Qt.gray)
        self.scene.addItem(text_item)

    def create_pin(self, x, y, type):
        x1 = x
        y1 = y
        rad = 5
        if (type == 0):
            self.scene.addLine(x1 + rad,
                                y1 + rad / 2,
                                x1 + 25 + rad / 2,
                                y1 + rad / 2,
                                pen=QPen(Qt.blue))
        else:
            x1 = x1 + 100
            if (type == 1): pen1 = QPen(Qt.red)
            else:  pen1 = QPen(Qt.green)

            self.scene.addLine(x1 + rad,
                                y1 + rad / 2,
                                x1 - 25 + rad / 2,
                                y1 + rad / 2,
                                pen=pen1)
        circle_item = QtWidgets.QGraphicsEllipseItem(x1, y1, rad, rad)  # Параметры: x, y, width, height

        element = Element(x1, y1, 10, 10)
        self.elements.append(element)
        circle_item.setBrush(Qt.white)
        self.scene.addItem(circle_item)
        
    def create_element(self, x, y, width, height):
        element = Element(x, y, width, height)
        self.elements.append(element)
        circle_item = QtWidgets.QGraphicsEllipseItem(x, y, width, height)
        circle_item.setBrush(Qt.white)
        self.scene.addItem(circle_item)
        circle_item.clicked.connect(self.handleItemClick)

    def handleItemClick(self):
        print("Нажатие на элемент!")

    def create_connection(self, start_element, end_element):
        connection = Connection(start_element, end_element)
        # self.connections.append(connection)
        # self.scene.addLine(start_element.x + start_element.width / 2,
        #                      start_element.y + start_element.height / 2,
        #                      end_element.x + end_element.width / 2,
        #                      end_element.y + end_element.height / 2,
        #                      pen=QPen(Qt.black))


    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            pos = self.ui.graphicsView.mapToScene(event.pos())
            x = pos.x()
            y = pos.y()

            for element in self.elements:
                if (x >= element.x and x <= element.x + element.width and
                    y >= element.y and y <= element.y + element.height):
                    self.current_element = element
                    break
            else:
                # self.create_element(x, y, 20, 20)

                if len(self.elements) > 1:
                    start = self.elements[-2]
                    end = self.elements[-1]
                    self.create_connection(start, end)

    def mouseMoveEvent(self, event):
        if self.current_element is not None:
            delta = event.pos() - event.localPos()
            self.current_element.x += delta.x()
            self.current_element.y += delta.y()
            self.update()

        if self.current_line is not None:
            self.current_line.setLine(QtCore.QLineF(self.current_line.line().p1(), event.scenePos()))

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.current_element = None

    def wheelEvent(self, event):
        zoom_in_factor = 1.25
        zoom_out_factor = 1 / zoom_in_factor

        if event.angleDelta().y() > 0:
            self.zoom(zoom_in_factor)
        else:
            self.zoom(zoom_out_factor)

    def zoom(self, zoom_factor):
        if (not self.ui.graphicsView.hasFocus()): return

        current_scale = self.ui.graphicsView.transform().m11()

        # Set the transformation anchor to the center of the viewport
        self.ui.graphicsView.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)

        # Apply the scaling transformation
        self.ui.graphicsView.scale(zoom_factor, zoom_factor)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Plus:
            self.graphics_view.zoom(1.25)
        elif event.key() == Qt.Key_Minus:
            self.graphics_view.zoom(0.8)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

