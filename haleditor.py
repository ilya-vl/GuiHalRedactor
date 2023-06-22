import sys
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsView
from PyQt5.QtGui import QPainter, QPen, QColor, QStandardItem, QStandardItemModel
from PyQt5.QtCore import Qt
from ui_haleditor import Ui_HalEditor
import halparser
from scene import *

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
        self.setGeometry(300, 300, 1024, 768)

        self.scene = Scene(self)
        self.ui.graph.setRenderHint(QPainter.Antialiasing)
        self.ui.graph.setScene(self.scene)
        self.scene.addLastComponent.connect(self.addLastComponent)

        self.ui.hierarchy.pressed.connect(self.handleItemPressed)

        # Кнопка вид -> Компоненты HAL
        self.ui.halComponentsAction.changed.connect(lambda: self.ui.hierarchy.setVisible(self.ui.halComponentsAction.isChecked()))

        # self.elements = []
        # self.connections = []
        # self.current_element = None
        # self.current_line = None

        #* Индекс элемента в категории Последние
        self.lastind = 0

        pins = ({'dir': 'in', 'name': 'in_', 'type': 'float', 'description': '"Input value";'},
                {'dir': 'out', 'name': 'out', 'type': 'float', 'description': '"Output value";'},
                {'dir': 'in', 'name': 'enable', 'type': 'bit', 'description': '"When TRUE, copy in to out";'},
                {'dir': 'in', 'name': 'enable', 'type': 'bit', 'description': '"When TRUE, copy in to out";'})
        andsch = Object("TEST", pins)

        self.create_object(andsch, 0, 0, False)

        # Создание модели данных
        self.model = QStandardItemModel()
        categories = ["Последние", "Системные", "Логические", "Арифметические", "Приведение типов", "Драйверы", "Другие"]
        categories_raw = ["last", "system", "logic", "arithm", "types", "drivers", "other"]
        self.category_ = {"":QStandardItem}
        ind = 0
        for category in categories:
            self.category_[categories_raw[ind]] = QStandardItem(category)
            self.category_[categories_raw[ind]].setFont(QtGui.QFont("Arial", 12))
            self.category_[categories_raw[ind]].setDragEnabled(False)
            self.model.appendRow(self.category_[categories_raw[ind]])
            self.category_[categories_raw[ind]].setEditable(False)
            self.category_[categories_raw[ind]].setData("no", Qt.UserRole)
            ind = ind + 1

        components_list, noparsed = halparser.load_components(COMPONENTSFOLDER)
        self.complist = components_list

        print("Следующие компоненты не могут быть использованы: \n")
        for item in noparsed:
            print(item)
            
        # Добавляем все компоненты по категориям в дерево компонентов
        for key, value in components_list.items():
            ind = 0
            for component in value:
                if value == "": continue
                item_s = component.split(".")[0]
                self.addComponentToHierarchy(ind, key, item_s)
                ind = ind + 1

        self.ui.hierarchy.setModel(self.model)
        self.model.setHeaderData(0, Qt.Horizontal, "Компоненты HAL")

    def handleItemPressed(self, index:QtCore.QModelIndex):
        item = self.model.itemFromIndex(index)
        
        #* Если выбран рут(заголовок) элемент 
        if (item.data(Qt.UserRole) == "no"):
            # Раскрывать и закрывать рут элементы при нажатии
            if (self.ui.hierarchy.isExpanded(index)): self.ui.hierarchy.setExpanded(index, False)
            else: self.ui.hierarchy.setExpanded(index, True)
            return

        component = self.complist[item.data(260)][item.data(Qt.UserRole)]
        pins = halparser.component_parse(COMPONENTSFOLDER + component)

        obj = Object(component.split(".")[0], pins)
        self.create_object(obj, 200, 200)

    #TODO
    def addComponentToHierarchy(self, ind, key, name):
        pins = halparser.component_parse(COMPONENTSFOLDER + name + ".comp")
        if (pins == False): return

        item = QStandardItem(name)
        self.category_[key].appendRow(item)

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
            
            subitem.setEditable(False)
            subitem.setData("no", Qt.UserRole)
            subitem.setToolTip(str(pin["description"]))
            item.appendRow(subitem)

    def addLastComponent(self, item:GraphicsHalComponent):
        if (isinstance(item, Circle)): return
        if (item != None):
            if (item.name + ".comp" not in self.complist["last"]):
                self.complist["last"].append(item.name + ".comp")

            for i in range(10):
                if (self.model.itemFromIndex(self.model.index(0, 0)).child(i, 0) != None):
                    text = self.model.itemFromIndex(self.model.index(0, 0).child(i, 0)).text()
                    if (text == item.name): return
                    
        self.addComponentToHierarchy(0, "last", item.name)
    def create_object(self, sch:Object, objx, objy, tracking=True):
        newComponent = GraphicsHalComponent(sch.NAME)
        self.scene.clearHiddenItems()
        self.scene.addItem(newComponent)
        
        for pin in sch.PINS:
            if (pin["dir"] == "in"):
                newComponent.addInputPin(pin["name"])
            elif (pin["dir"] == "out" or pin["dir"] == "io"): #TODO IO
                newComponent.addOutputPin(pin["name"])    

        if (tracking == True):
            self.scene.selectedItem = newComponent
            newComponent.hide()

        #         text_item.setPos(objx + 12, objy + ins * pindist - 9)
        #         ins = ins + 1
        #     else:
        #         if (pin["dir"] == "out"): typ = 1
        #         else: typ = 2
        #         self.create_pin(objx, objy + outs * pindist, typ)

        #         text_item.setPos(objx + 82, objy + outs * pindist - 9)
        #         outs = outs + 1

        #     text_item.setDefaultTextColor(Qt.gray)
        #     self.scene.addItem(text_item)

        # if (ins > outs): length = ins
        # else: length = outs
        
        # rectx = objx + 27.5
        # recty = objy - 2.5
        # rectwidth = 50
        # rectheight = 10 + (pindist * (length-1))
        # element = Element(rectx, recty, rectwidth, rectheight)
        # self.elements.append(element)
        # self.scene.addRect(rectx, recty, rectwidth, rectheight, pen=QPen(Qt.black), brush=QColor("white"))

        # text_item = QtWidgets.QGraphicsTextItem(sch.NAME)
        # text_item.setScale(0.9)
        # text_item.setPos(objx + 35, objy - 22)
        # text_item.setDefaultTextColor(Qt.gray)
        # self.scene.addItem(text_item)

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

    def wheelEvent(self, event):
        zoom_in_factor = 1.25
        zoom_out_factor = 1 / zoom_in_factor

        if event.angleDelta().y() > 0:
            self.zoom(zoom_in_factor)
        else:
            self.zoom(zoom_out_factor)

    def zoom(self, zoom_factor):
        if (not self.ui.graph.hasFocus()): return

        # Set the transformation anchor to the center of the viewport
        self.ui.graph.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)

        # Apply the scaling transformation
        self.ui.graph.scale(zoom_factor, zoom_factor)

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