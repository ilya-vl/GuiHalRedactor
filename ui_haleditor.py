# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'haleditor.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_HalEditor(object):
    def setupUi(self, HalEditor):
        HalEditor.setObjectName("HalEditor")
        HalEditor.resize(1253, 799)
        HalEditor.setMaximumSize(QtCore.QSize(16777215, 16777215))
        HalEditor.setStyleSheet("QTreeView {\n"
"    border-radius: 10px;\n"
"    background:white;\n"
"    color: #333333;\n"
"}\n"
"QTreeView::item {\n"
"    height: 30px;\n"
"    border-radius: 5px;\n"
"}\n"
"QTreeView::item:selected {\n"
"    color:black;\n"
"}")
        self.centralwidget = QtWidgets.QWidget(HalEditor)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setHorizontalSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.graph = QtWidgets.QGraphicsView(self.centralwidget)
        self.graph.setMinimumSize(QtCore.QSize(500, 0))
        self.graph.setMouseTracking(True)
        self.graph.setStyleSheet("border-radius: 10px;\n"
"background: white;\n"
"border: 1px solid lightgrey;")
        self.graph.setDragMode(QtWidgets.QGraphicsView.NoDrag)
        self.graph.setObjectName("graph")
        self.gridLayout.addWidget(self.graph, 0, 2, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(5, 20, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 1, 1, 1)
        self.hierarchy = QtWidgets.QTreeView(self.centralwidget)
        self.hierarchy.setMaximumSize(QtCore.QSize(200, 16777215))
        self.hierarchy.setStyleSheet("border: 1px solid lightgrey;")
        self.hierarchy.setAutoScroll(True)
        self.hierarchy.setDragEnabled(True)
        self.hierarchy.setRootIsDecorated(True)
        self.hierarchy.setSortingEnabled(False)
        self.hierarchy.setAnimated(True)
        self.hierarchy.setObjectName("hierarchy")
        self.hierarchy.header().setVisible(True)
        self.gridLayout.addWidget(self.hierarchy, 0, 0, 1, 1)
        HalEditor.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(HalEditor)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1253, 20))
        self.menubar.setObjectName("menubar")
        self.filemenu = QtWidgets.QMenu(self.menubar)
        self.filemenu.setObjectName("filemenu")
        self.aboutmenu = QtWidgets.QMenu(self.menubar)
        self.aboutmenu.setObjectName("aboutmenu")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.menu_2 = QtWidgets.QMenu(self.menubar)
        self.menu_2.setObjectName("menu_2")
        HalEditor.setMenuBar(self.menubar)
        self.newAction = QtWidgets.QAction(HalEditor)
        self.newAction.setObjectName("newAction")
        self.openAction = QtWidgets.QAction(HalEditor)
        self.openAction.setObjectName("openAction")
        self.lastAction = QtWidgets.QAction(HalEditor)
        self.lastAction.setObjectName("lastAction")
        self.saveAction = QtWidgets.QAction(HalEditor)
        self.saveAction.setObjectName("saveAction")
        self.saveasAction = QtWidgets.QAction(HalEditor)
        self.saveasAction.setObjectName("saveasAction")
        self.exitAction = QtWidgets.QAction(HalEditor)
        self.exitAction.setObjectName("exitAction")
        self.halComponentsAction = QtWidgets.QAction(HalEditor)
        self.halComponentsAction.setCheckable(True)
        self.halComponentsAction.setChecked(True)
        self.halComponentsAction.setObjectName("halComponentsAction")
        self.settingsAction = QtWidgets.QAction(HalEditor)
        self.settingsAction.setObjectName("settingsAction")
        self.action_2 = QtWidgets.QAction(HalEditor)
        self.action_2.setObjectName("action_2")
        self.filemenu.addSeparator()
        self.filemenu.addAction(self.newAction)
        self.filemenu.addAction(self.openAction)
        self.filemenu.addAction(self.lastAction)
        self.filemenu.addSeparator()
        self.filemenu.addAction(self.action_2)
        self.filemenu.addSeparator()
        self.filemenu.addAction(self.saveAction)
        self.filemenu.addAction(self.saveasAction)
        self.filemenu.addSeparator()
        self.filemenu.addAction(self.exitAction)
        self.menu.addAction(self.settingsAction)
        self.menu_2.addAction(self.halComponentsAction)
        self.menubar.addAction(self.filemenu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.aboutmenu.menuAction())

        self.retranslateUi(HalEditor)
        QtCore.QMetaObject.connectSlotsByName(HalEditor)

    def retranslateUi(self, HalEditor):
        _translate = QtCore.QCoreApplication.translate
        HalEditor.setWindowTitle(_translate("HalEditor", "Hal Editor"))
        self.filemenu.setTitle(_translate("HalEditor", "Файл"))
        self.aboutmenu.setTitle(_translate("HalEditor", "О программе"))
        self.menu.setTitle(_translate("HalEditor", "Настройки"))
        self.menu_2.setTitle(_translate("HalEditor", "Вид"))
        self.newAction.setText(_translate("HalEditor", "Новый"))
        self.openAction.setText(_translate("HalEditor", "Открыть"))
        self.lastAction.setText(_translate("HalEditor", "Последние"))
        self.saveAction.setText(_translate("HalEditor", "Сохранить"))
        self.saveasAction.setText(_translate("HalEditor", "Сохранить как"))
        self.exitAction.setText(_translate("HalEditor", "Выход"))
        self.halComponentsAction.setText(_translate("HalEditor", "Компоненты HAL"))
        self.settingsAction.setText(_translate("HalEditor", "Настройки"))
        self.action_2.setText(_translate("HalEditor", "Перезагрузить файл"))
