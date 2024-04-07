# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindowRIvUzl.ui'
##
## Created by: Qt User Interface Compiler version 6.6.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
                            QMetaObject, QObject, QPoint, QRect, QSize, QTime,
                            QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
                           QFontDatabase, QGradient, QIcon, QImage,
                           QKeySequence, QLinearGradient, QPainter, QPalette,
                           QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QHeaderView, QLabel,
                               QLineEdit, QMainWindow, QMenuBar, QPushButton,
                               QSizePolicy, QStatusBar, QTableWidget,
                               QTableWidgetItem, QTreeWidget, QTreeWidgetItem,
                               QVBoxLayout, QWidget)


class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(980, 813)
        self.central_widget = QWidget(MainWindow)
        self.central_widget.setObjectName(u"central_widget")
        self.verticalLayoutWidget = QWidget(self.central_widget)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(0, 50, 681, 391))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.table_widget_expense = QTableWidget(self.verticalLayoutWidget)
        if (self.table_widget_expense.columnCount() < 4):
            self.table_widget_expense.setColumnCount(4)
        __qtablewidgetitem = QTableWidgetItem()
        self.table_widget_expense.setHorizontalHeaderItem(
            0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.table_widget_expense.setHorizontalHeaderItem(
            1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.table_widget_expense.setHorizontalHeaderItem(
            2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.table_widget_expense.setHorizontalHeaderItem(
            3, __qtablewidgetitem3)
        self.table_widget_expense.setObjectName(u"table_widget_expense")

        self.verticalLayout.addWidget(self.table_widget_expense)

        self.verticalLayoutWidget_2 = QWidget(self.central_widget)
        self.verticalLayoutWidget_2.setObjectName(u"verticalLayoutWidget_2")
        self.verticalLayoutWidget_2.setGeometry(QRect(0, 480, 681, 121))
        self.verticalLayout_2 = QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.table_widget_budget = QTableWidget(self.verticalLayoutWidget_2)
        if (self.table_widget_budget.columnCount() < 3):
            self.table_widget_budget.setColumnCount(3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.table_widget_budget.setHorizontalHeaderItem(
            0, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.table_widget_budget.setHorizontalHeaderItem(
            1, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.table_widget_budget.setHorizontalHeaderItem(
            2, __qtablewidgetitem6)
        if (self.table_widget_budget.rowCount() < 3):
            self.table_widget_budget.setRowCount(3)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.table_widget_budget.setItem(0, 0, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.table_widget_budget.setItem(0, 2, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        self.table_widget_budget.setItem(1, 0, __qtablewidgetitem9)
        __qtablewidgetitem10 = QTableWidgetItem()
        self.table_widget_budget.setItem(1, 2, __qtablewidgetitem10)
        __qtablewidgetitem11 = QTableWidgetItem()
        self.table_widget_budget.setItem(2, 0, __qtablewidgetitem11)
        __qtablewidgetitem12 = QTableWidgetItem()
        self.table_widget_budget.setItem(2, 2, __qtablewidgetitem12)
        self.table_widget_budget.setObjectName(u"table_widget_budget")

        self.verticalLayout_2.addWidget(self.table_widget_budget)

        self.button_save_expense = QPushButton(self.central_widget)
        self.button_save_expense.setObjectName(u"button_save_expense")
        self.button_save_expense.setGeometry(QRect(0, 0, 31, 31))
        self.button_add_expense = QPushButton(self.central_widget)
        self.button_add_expense.setObjectName(u"button_add_expense")
        self.button_add_expense.setGeometry(QRect(30, 0, 31, 31))
        self.button_delete_expense = QPushButton(self.central_widget)
        self.button_delete_expense.setObjectName(u"button_delete_expense")
        self.button_delete_expense.setGeometry(QRect(60, 0, 31, 31))
        self.verticalLayoutWidget_3 = QWidget(self.central_widget)
        self.verticalLayoutWidget_3.setObjectName(u"verticalLayoutWidget_3")
        self.verticalLayoutWidget_3.setGeometry(QRect(680, 50, 301, 391))
        self.verticalLayout_3 = QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.tree_widget_category = QTreeWidget(self.verticalLayoutWidget_3)
        self.tree_widget_category.setObjectName(u"tree_widget_category")

        self.verticalLayout_3.addWidget(self.tree_widget_category)

        self.button_add_category = QPushButton(self.central_widget)
        self.button_add_category.setObjectName(u"button_add_category")
        self.button_add_category.setGeometry(QRect(710, 0, 31, 31))
        self.button_save_category = QPushButton(self.central_widget)
        self.button_save_category.setObjectName(u"button_save_category")
        self.button_save_category.setGeometry(QRect(680, 0, 31, 31))
        self.button_delete_category = QPushButton(self.central_widget)
        self.button_delete_category.setObjectName(u"button_delete_category")
        self.button_delete_category.setGeometry(QRect(770, 0, 31, 31))
        self.button_add_child_category = QPushButton(self.central_widget)
        self.button_add_child_category.setObjectName(
            u"button_add_child_category")
        self.button_add_child_category.setGeometry(QRect(740, 0, 31, 31))
        self.lineEdit = QLineEdit(self.central_widget)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(760, 490, 221, 25))
        self.combo_box_chose_category = QComboBox(self.central_widget)
        self.combo_box_chose_category.setObjectName(
            u"combo_box_chose_category")
        self.combo_box_chose_category.setGeometry(QRect(760, 530, 221, 25))
        self.label_4 = QLabel(self.central_widget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(710, 490, 31, 17))
        self.label_1 = QLabel(self.central_widget)
        self.label_1.setObjectName(u"label_1")
        self.label_1.setGeometry(QRect(690, 530, 67, 17))
        self.label = QLabel(self.central_widget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(0, 30, 67, 17))
        self.label_2 = QLabel(self.central_widget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(680, 30, 67, 17))
        self.label_3 = QLabel(self.central_widget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(0, 460, 67, 17))
        MainWindow.setCentralWidget(self.central_widget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 980, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(
            QCoreApplication.translate("MainWindow", u"Bookkeeper", None))
        ___qtablewidgetitem = self.table_widget_expense.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(
            QCoreApplication.translate("MainWindow", u"Date", None))
        ___qtablewidgetitem1 = self.table_widget_expense.horizontalHeaderItem(
            1)
        ___qtablewidgetitem1.setText(
            QCoreApplication.translate("MainWindow", u"Amount", None))
        ___qtablewidgetitem2 = self.table_widget_expense.horizontalHeaderItem(
            2)
        ___qtablewidgetitem2.setText(
            QCoreApplication.translate("MainWindow", u"Category", None))
        ___qtablewidgetitem3 = self.table_widget_expense.horizontalHeaderItem(
            3)
        ___qtablewidgetitem3.setText(
            QCoreApplication.translate("MainWindow", u"Comment", None))
        ___qtablewidgetitem4 = self.table_widget_budget.horizontalHeaderItem(0)
        ___qtablewidgetitem4.setText(
            QCoreApplication.translate("MainWindow", u"Tern", None))
        ___qtablewidgetitem5 = self.table_widget_budget.horizontalHeaderItem(1)
        ___qtablewidgetitem5.setText(
            QCoreApplication.translate("MainWindow", u"Sum", None))
        ___qtablewidgetitem6 = self.table_widget_budget.horizontalHeaderItem(2)
        ___qtablewidgetitem6.setText(
            QCoreApplication.translate("MainWindow", u"Budget", None))

        __sortingEnabled = self.table_widget_budget.isSortingEnabled()
        self.table_widget_budget.setSortingEnabled(False)
        ___qtablewidgetitem7 = self.table_widget_budget.item(0, 0)
        ___qtablewidgetitem7.setText(
            QCoreApplication.translate("MainWindow", u"Day", None))
        ___qtablewidgetitem8 = self.table_widget_budget.item(0, 2)
        ___qtablewidgetitem8.setText(
            QCoreApplication.translate("MainWindow", u"1000", None))
        ___qtablewidgetitem9 = self.table_widget_budget.item(1, 0)
        ___qtablewidgetitem9.setText(
            QCoreApplication.translate("MainWindow", u"Month", None))
        ___qtablewidgetitem10 = self.table_widget_budget.item(1, 2)
        ___qtablewidgetitem10.setText(
            QCoreApplication.translate("MainWindow", u"30000", None))
        ___qtablewidgetitem11 = self.table_widget_budget.item(2, 0)
        ___qtablewidgetitem11.setText(
            QCoreApplication.translate("MainWindow", u"Year", None))
        ___qtablewidgetitem12 = self.table_widget_budget.item(2, 2)
        ___qtablewidgetitem12.setText(
            QCoreApplication.translate("MainWindow", u"360000", None))
        self.table_widget_budget.setSortingEnabled(__sortingEnabled)

        self.button_save_expense.setText("")
        self.button_add_expense.setText("")
        self.button_delete_expense.setText("")
        ___qtreewidgetitem = self.tree_widget_category.headerItem()
        ___qtreewidgetitem.setText(
            0, QCoreApplication.translate("MainWindow", u"Category", None))
        self.button_add_category.setText("")
        self.button_save_category.setText("")
        self.button_delete_category.setText("")
        self.button_add_child_category.setText("")
        self.label_4.setText(
            QCoreApplication.translate("MainWindow", u"Sum", None))
        self.label_1.setText(
            QCoreApplication.translate("MainWindow", u"Category", None))
        self.label.setText(
            QCoreApplication.translate("MainWindow", u"Expense", None))
        self.label_2.setText(
            QCoreApplication.translate("MainWindow", u"Category", None))
        self.label_3.setText(
            QCoreApplication.translate("MainWindow", u"Budget", None))

    # retranslateUi
