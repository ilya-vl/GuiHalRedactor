from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QGraphicsSceneMouseEvent, QGraphicsEllipseItem, QGraphicsRectItem, QGraphicsSimpleTextItem
from PyQt5.QtGui import QColor, QPen, QTransform, QPainter
from PyQt5.QtCore import QPointF
from typing import List

class Scene(QtWidgets.QGraphicsScene):
    def __init__(self, parent=None):
        super().__init__(parent)
        # for i in range(10):
        #     item = NetСonnector()
        #     self.addItem(item)
        self.selectedItem = None


        # Добавление компонентов на сцену: В будущем будет функция автоматического определения пинов и их добавления по компоненту
        self.halItem = GraphicsHalComponent("and4")
        self.halItem.addInputPin("in0")
        self.halItem.addInputPin("in1")
        self.halItem.addInputPin("in3")
        self.halItem.addInputPin("in4")
        self.halItem.addOutputPin("out")
        self.addItem(self.halItem)
        self.halItem.setPos(100,100)
        
        self.halItem2 = GraphicsHalComponent("not")
        self.halItem2.addInputPin("in")
        self.halItem2.addOutputPin("out")
        self.addItem(self.halItem2)
        self.halItem2.setPos(200,100)
        
    # Обработка нажатия мыши по сцене. Определяем нажали ли на какой-то элемент, если да, то проверяем на какой, и обрабатываем
    def mousePressEvent(self, event):
        self.update() 
        # self.cross.shown = False
        item = self.itemAt(event.scenePos(), QTransform()) #Есть ли предмет на координатах курсора?
        print(item)
        if isinstance(item, Circle):
            self.selectedItem = item  # self.selectedItem - предмет, который будет шевелится при событии mouseMoveEvent
        if isinstance(item, GraphicsHalComponent):
            self.selectedItem = item  # self.selectedItem - предмет, который будет шевелится при событии mouseMoveEvent
        if isinstance(item, QGraphicsRectItem): 
            # если попали по прямоугольнику, проверяем, принадлежит ли этот прямоугольник какому либо GraphicsHalComponent
            if isinstance(item.group(), GraphicsHalComponent): 
                self.selectedItem = item.group() 

        if isinstance(item, QGraphicsSimpleTextItem):
            # если попали по тексу, проверяем, принадлежит ли этот прямоугольник какому либо GraphicsPin
            if isinstance(item.group(), GraphicsPin):
                pin:GraphicsPin = item.group()
                # Если нажали на пин, создаем графическое представление связи и привязываем один из кружков связи к пину 
                newItem = NetСonnector()
                self.addItem(newItem)
                pin.setCircle(newItem.circle1)
                
                # Выбираем второй кружок как предмет для перетаскивания. обновляем позицию кружка по курсору и перерисовывем полоски между кружками
                self.selectedItem = newItem.circle2
                newItem.circle2.setPos(event.scenePos())
                newItem.circle2.group().redraw()

    # Обработка нажатия движения мыши по сцене. Если есть какой-то выбранный элемент, то шевелим его по своему, в зависимости от типа
    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        x = event.scenePos().x()
        y = event.scenePos().y()

        if self.selectedItem != None:
            # deltaPos = QPointF( abs(self.selectedItem.pos().x() - x), abs(self.selectedItem.pos().y() - y) )
            self.selectedItem.setPos(x, y)
            if isinstance(self.selectedItem, Circle):
                self.selectedItem.group().redraw()
            elif isinstance(self.selectedItem, GraphicsHalComponent):
                halComponent: GraphicsHalComponent = self.selectedItem
                halComponent.redraw()

    # Когда отпустили кнопку мыши - сбрасываем последний выделенный элемент, что-бы он не шевелился, когджа кнопка не нажата
    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        self.selectedItem = None
        return super().mouseReleaseEvent(event)
                
    
    # Класс кружка, принимает позицию и диаметр. Ибо обычный QGraphicsEllipseItem это по факту прямоугольник
class Circle(QGraphicsEllipseItem):
    def __init__(self, x, y, diameter, parent=None):
        super().__init__(x, y, diameter, diameter, parent)
        self.setFlag(QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.diameter = diameter

    
    def centerPos(self):
        pos = self.pos()
        pos.setX(pos.x() + self.diameter / 2)
        pos.setY(pos.y() + self.diameter / 2)
        return pos
    
# Класс графического отображения пина. К нему можно привязать кружок от связи
class GraphicsPin(QtWidgets.QGraphicsItemGroup ):
    def __init__(self, name, pinType = "input", parent=None):
        super().__init__(parent)
        self.name = name
        self.text = QtWidgets.QGraphicsSimpleTextItem(name)
        self.addToGroup(self.text)
        self.circle: Circle = None
        self.pinType = pinType

    # Привязываем кружок связи к пину
    def setCircle(self, circle: QGraphicsEllipseItem):
        self.circle = circle
        self.updateCirclePos()

    # Обновление позиции кружка, относительно позиции пина
    def updateCirclePos(self):
        if self.circle:
            # Получаем родительский объект GraphicsHalComponent, на котором лежит наш пин. А так-же находим координаты для кружка, относительно стенок этого компонента
            parentComponent: GraphicsHalComponent = self.group()
            # Если пин input  помещаем кружок на левой стенке компонента, если output, то на правой
            x = self.mapFromParent(parentComponent.boundingRect().width(),0).x() if self.pinType == "output" else self.mapFromParent(0,0).x()
            # Получаем координаты нашего пина в системе координат родительского компонента
            p = self.mapFromParent(self.pos())
            # находим точку, куда расположим кружок
            point = QPointF(x - self.circle.diameter / 2, p.y() + self.boundingRect().height() / 2 - self.circle.diameter / 2)
            # располагаем кружок на сцене
            self.circle.setPos( self.mapToScene(point) )
            # через метод group обращаемся к NetСonnector, которому принадлежит кружок и перерисовываем соеденительные линии
            self.circle.group().redraw()

# Класс компонента содержит имя и определенное количество GraphicsPin. 
class GraphicsHalComponent(QtWidgets.QGraphicsItemGroup ):
    def __init__(self, name, parent=None):
        super().__init__(parent)
        self.name = name
        self.inputPins: List[GraphicsPin] = [] 
        self.outputPins: List[GraphicsPin] = []
        self.rect = QtWidgets.QGraphicsRectItem(0,0,70,100) # Размер условный, в дальнейшем будет динамическим
        self.gName = QtWidgets.QGraphicsSimpleTextItem(self.name) 
        self.addToGroup(self.rect) 
        self.addToGroup(self.gName)
        

        # Располагаем имя компонета посередине прямоугольника. С небольшим отступом сверху
        nameRect = self.gName.boundingRect()
        rect = self.boundingRect()
        margin = 5
        self.gName.setPos( rect.width() / 2 - nameRect.width() / 2, margin) 


    # Функция, обновляет позиции всех, присоединенных к пинам, кружков, и перерисовывает их соединительные линии
    def redraw(self):
        for pin in self.inputPins:
            pin.updateCirclePos()
        for pin in self.outputPins:
            pin.updateCirclePos()

    # Функция добавления входного пина на прямоугольник, и размещает его равномерно по длинне, относительно других пинов
    def addInputPin(self, name):
        newPin = GraphicsPin(name, "input")
        self.inputPins.append(newPin)
        self.addToGroup(newPin)
        self.DistributePositionsByHeight(self.inputPins)

    # Тоже самое, как и для входных пинов, но для выходных
    def addOutputPin(self, name):
        newPin = GraphicsPin(name, "output")
        self.outputPins.append(newPin)
        self.addToGroup(newPin)
        self.DistributePositionsByHeight(self.outputPins, right=True)

    # Расставляем пины по высоте.
    def DistributePositionsByHeight(self, pins: List[QtWidgets.QGraphicsSimpleTextItem], right = False):
        rect = self.boundingRect() 
        denominator = (len(pins) + 1)
        distance = rect.height() /  denominator  # Дистанция, которая будет между пинами
        margin = 7 # отступ от внешней стенки по оси X

        i = 0
        for pin in pins:
            i += 1
            xPos = abs(self.boundingRect().width() - pin.boundingRect().width()) - margin if right else margin
            y =  distance * i
            pin.setPos(xPos, y)


# Графическое представление связи между пинами
class NetСonnector(QtWidgets.QGraphicsItemGroup ):
    def __init__(self, parent=None):
        super(NetСonnector, self).__init__(parent)
        self.circle1 = Circle(0,0,10)
        self.circle2 = Circle(0,0,10)
        self.line = QtWidgets.QGraphicsLineItem()
        self.line2 = QtWidgets.QGraphicsLineItem()
        self.line3 = QtWidgets.QGraphicsLineItem()

        for item in [self.circle1, self.circle2, self.line, self.line2, self.line3]:
            self.addToGroup(item)

        # Рисуем кружки выше линий, второй кружок, выше первого
        self.circle1.setZValue(10)
        self.circle2.setZValue(11)

    # Возвращаем невалидное значение boundingRect, что-бы сцена не реагировала на пустую область между точками, а только на линии или кружки
    def boundingRect(self):
        return QtCore.QRectF(-1,-1,0,0)


    # Перерисовываем соеденительные линии относительно позиции кружков. Нужно выхывать после перемещения кружков
    def redraw(self):
        pos1 = self.circle1.centerPos()
        pos2 = self.circle2.centerPos()

        # Меняем местами значения, так, что-юы pos1 был меньше чем pos2 по оси X
        if pos1.x() > pos2.x():
            pos1, pos2 = pos2, pos1

        # Находим координату середину между координатами точек по оси Х
        delta = (pos2.x() - pos1.x()) / 2

        # Рисуем линию от первого кружка до найденой середины, на высоте первого кружка
        self.line.setLine(QtCore.QLineF(pos1, QPointF(pos1.x() + delta, pos1.y())))
        # Рисуем горизонтальню линию, начинающуюся с конца первой линии, и идущей к высоте второго кружка
        self.line2.setLine(QtCore.QLineF(QPointF(pos1.x() + delta, pos1.y()), QPointF(pos1.x() + delta, pos2.y())))
        # Рисуем горизонтальную линию, идущей от середины до второго кружка
        self.line3.setLine(QtCore.QLineF(QPointF(pos1.x() + delta, pos2.y()), pos2))


# Окно для отображения всего этого добра
class Window(QtWidgets.QWidget):
    def __init__(self):
        super(Window, self).__init__()
        scene = Scene()
        scene.setSceneRect(0,0, 1000, 800)
        view = QtWidgets.QGraphicsView(scene)
        view.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(view)

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = Window()
    w.setGeometry(100,100,1100,900)
    w.show()
    sys.exit(app.exec_())
