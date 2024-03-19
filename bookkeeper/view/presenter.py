import sys
import sqlite3
from bookkeeper.models.expense import Expense
from bookkeeper.models.category import Category
from bookkeeper.repository.sqlite_repository import SQLiteRepository
from bookkeeper.repository.abstract_repository import AbstractRepository
from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QWidget, QTreeWidgetItem
from bookkeeper.view.ui_mainwindow import Ui_MainWindow
from bookkeeper.view.ui_category import Ui_Form

class MainWindow(QMainWindow):
    def __init__(self, esp_repo:AbstractRepository[Expense], cate_repo:AbstractRepository[Category]):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.tableWidget.setColumnWidth(0, 200) 
        self.ui.tableWidget.setColumnWidth(1, 80)  
        self.ui.tableWidget.setColumnWidth(2, 80)
        self.ui.tableWidget.setColumnWidth(3, 305)

        self.ui.tableWidget_2.setColumnWidth(0, 80) 
        self.ui.tableWidget_2.setColumnWidth(1, 298)  
        self.ui.tableWidget_2.setColumnWidth(2, 298)

        self.ui.tableWidget.setRowCount(len(esp_repo.get_all()))
        for i, espense in enumerate(esp_repo.get_all()):
            for j in range(self.ui.tableWidget.columnCount()):
                attr_name = self.ui.tableWidget.horizontalHeaderItem(j).text().lower()
                if attr_name == 'category':
                    item = cate_repo.get(getattr(espense, attr_name)).name 
                else:
                    item = getattr(espense, attr_name)
                self.ui.tableWidget.setItem(i, j, QTableWidgetItem(str(item)))
                
    #     self.category_inspector = CategoryInspector(repo_2)
    #     self.ui.pushButton.clicked.connect(self.open_category_inspector)

    # def open_category_inspector(self):
    #     self.category_inspector.show()
 
class CategoryInspector(QWidget):
    def __init__(self, repo:AbstractRepository[Category]):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        tree_widgets :list[QTreeWidgetItem]= []
        for row in repo.get_all() :
            tree_widgets.append(QTreeWidgetItem())
        for i, row in enumerate(repo.get_all()):
            tree_widgets[i].addChildren([tree_widgets[cat.pk-1] for cat in row.get_subcategories(repo)])
            tree_widgets[i].setText(0, row.name)

        self.ui.treeWidget.setColumnCount(1)
        self.ui.treeWidget.addTopLevelItems(tree_widgets)

class Presenter:
    def __init__(self, db_file:str):
        self.expense_repo = SQLiteRepository[Expense](db_file, Expense)
        self.category_repo = SQLiteRepository[Category](db_file, Category)
        self.main_window = MainWindow(self.expense_repo, self.category_repo)
        self.category_inspector = CategoryInspector(self.category_repo)

        self.main_window.ui.pushButton.clicked.connect(self.open_category_inspector)

        self.main_window.show()

    def open_category_inspector(self):
        self.category_inspector.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    presenter = Presenter('tutorial.db')
   
    sys.exit(app.exec())
    # window.show()
