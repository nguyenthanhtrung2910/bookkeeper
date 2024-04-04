import sys
import re
import sqlite3
from datetime import datetime

from dataclasses import dataclass
from inspect import get_annotations
from bookkeeper.models.expense import Expense
from bookkeeper.models.category import Category
from bookkeeper.repository.sqlite_repository import SQLiteRepository
from bookkeeper.repository.abstract_repository import AbstractRepository
from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QLabel, QTreeWidgetItem, QDialog
from PySide6.QtCore import Slot, Qt
from PySide6.QtGui import QIcon, QPixmap
from bookkeeper.view.ui_mainwindow import Ui_MainWindow
from bookkeeper.view.ui_errordialog import Ui_Dialog



@dataclass(slots=True)
class Change:
    """
    Object to save change in table
    """
    operator: str
    row: int|None = None
    col: str|None = None
    new_value: str|None = None
    old_value: str|None = None


class MainWindow(QMainWindow):
    def __init__(self, esp_repo:AbstractRepository[Expense], cate_repo:AbstractRepository[Category]) -> None:
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.tableWidget.setColumnWidth(0, 200) 
        self.ui.tableWidget.setColumnWidth(1, 80)  
        self.ui.tableWidget.setColumnWidth(2, 80)
        self.ui.tableWidget.setColumnWidth(3, 305)

        self.ui.tableWidget_2.setColumnWidth(0, 80) 
        self.ui.tableWidget_2.setColumnWidth(1, 290)  
        self.ui.tableWidget_2.setColumnWidth(2, 290)

        #in order to save changes
        self.changes: list[Change] = []

        self.old_text_cache: dict[QTreeWidgetItem, str] = {}
        self.tree_changes: list[Change] = []

        #write data to table
        data = esp_repo.get_all()
        self.ui.tableWidget.setRowCount(len(data))
        for i, espense in enumerate(data):
            for j in range(self.ui.tableWidget.columnCount()):
                attr_name = self.ui.tableWidget.horizontalHeaderItem(j).text().lower()
                item = getattr(espense, attr_name)
                if item is None:
                    item = ''
                else:
                    if attr_name == 'category':
                        item = cate_repo.get(getattr(espense, attr_name)).name 
                self.ui.tableWidget.setItem(i, j, QTableWidgetItem(str(item)))

        tree_widgets :list[QTreeWidgetItem]= []
        data = cate_repo.get_all()
        for _ in data :
            tree_widgets.append(QTreeWidgetItem())
        for i, row in enumerate(data):
            tree_widgets[i].addChildren([tree_widgets[cat.pk-1] for cat in row.get_all_children(cate_repo)])
            tree_widgets[i].setText(0, row.name)
            tree_widgets[i].setFlags(tree_widgets[i].flags() | Qt.ItemIsEditable)
            self.old_text_cache[tree_widgets[i]] = tree_widgets[i].text(0)

        self.ui.treeWidget.setColumnCount(1)
        self.ui.treeWidget.addTopLevelItems(tree_widgets)

        #set save button image
        pixmap = QPixmap("install.png")
        icon = QIcon(pixmap)
        self.ui.save_button.setIcon(icon)
        self.ui.save_button_tree.setIcon(icon)

        #set add button image
        pixmap = QPixmap("add.png")
        icon = QIcon(pixmap)
        self.ui.add_button.setIcon(icon)
        self.ui.add_button_tree.setIcon(icon)

        #set delete button image
        pixmap = QPixmap("delete.png")
        icon = QIcon(pixmap)
        self.ui.delete_button.setIcon(icon)
        self.ui.delete_button_tree.setIcon(icon)
                
        #set add child button image
        pixmap = QPixmap("folder.png")
        icon = QIcon(pixmap)
        self.ui.add_child_button.setIcon(icon)

        self.ui.tableWidget.itemChanged.connect(self.handle_item_change)
        self.ui.add_button.clicked.connect(self.handle_adding_row)
        self.ui.delete_button.clicked.connect(self.handle_deleting_row)

        self.ui.treeWidget.itemChanged.connect(self.handle_change_tree)
        self.ui.add_button_tree.clicked.connect(self.handle_add_item)
        self.ui.add_child_button.clicked.connect(self.handle_add_child)
        self.ui.delete_button_tree.clicked.connect(self.handle_delete_tree)


    @Slot(QTableWidgetItem)
    def handle_item_change(self, item:QTableWidgetItem) -> None:
        row = item.row() + 1
        col = item.column()
        value = item.text()
        column_name = self.ui.tableWidget.horizontalHeaderItem(col).text().lower()
        for change in self.changes:
            if change.operator == 'update' and change.row == row and change.col == column_name:
                self.changes.remove(change)
        self.changes.append(Change('update', row, column_name, value))

    @Slot()
    def handle_adding_row(self) -> None:
        current_row_count = self.ui.tableWidget.rowCount()
        self.ui.tableWidget.insertRow(current_row_count)
        self.ui.tableWidget.setItem(self.ui.tableWidget.rowCount() - 1, 0,  QTableWidgetItem(datetime.now().strftime('%Y-%m-%d')))
        self.changes.append(Change('add', col='date', new_value=datetime.now().strftime('%Y-%m-%d')))
    
    @Slot()
    def handle_deleting_row(self) -> None:
        selected_row = self.ui.tableWidget.currentRow()
        if selected_row >= 0:
            self.ui.tableWidget.removeRow(selected_row)
        self.changes.append(Change('delete', selected_row+1))

    @Slot(QTreeWidgetItem, int)
    def handle_change_tree(self, item: QTreeWidgetItem, column:int) -> None:
        if item is not None:
            old_text = self.old_text_cache.get(item, '')  # Get the old text from cache
            new_text = item.text(column)                  # Get the new text after the change
            self.old_text_cache[item] = new_text
        for change in self.tree_changes:
            if change.operator == 'update' and change.new_value == old_text:
                self.tree_changes.remove(change)
        self.tree_changes.append(Change('update', new_value=new_text, old_value=old_text ))

    def get_child_items(self, parent_item:QTreeWidgetItem) -> list[QTreeWidgetItem]:
        items = []
        child_count = parent_item.childCount()
        for i in range(child_count):
            child_item = parent_item.child(i)
            items.append(child_item)
            items.extend(self.get_child_items(child_item))
        return items
    
    def all_chilren_tree(self) -> list[QTreeWidgetItem]:
        items = []
        top_level_item_count = self.ui.treeWidget.topLevelItemCount()
        for i in range(top_level_item_count):
            top_level_item = self.ui.treeWidget.topLevelItem(i)
            items.append(top_level_item)
            items.extend(self.get_child_items(top_level_item))
        return items
    
    @Slot()
    def handle_add_item(self) -> None:
        selected_item = self.ui.treeWidget.currentItem()
        if selected_item is None:
            return
        parent = selected_item.parent()
        blank_item_numbers = [int(item.text(0)[8:]) for item in self.all_chilren_tree() 
                    if item.text(0)[0:8] == 'untitled']
        if len(blank_item_numbers) == 0:
            item_text = 'untitled1'
        else:
            item_text = 'untitled'+str(max(blank_item_numbers) + 1)
        new_item = QTreeWidgetItem([item_text])
        new_item.setFlags(new_item.flags() | Qt.ItemIsEditable)
        self.old_text_cache[new_item] = new_item.text(0)
        if parent is None:
            self.ui.treeWidget.addTopLevelItem(new_item)
            self.tree_changes.append(Change('add', new_value=new_item.text(0), old_value=None))
        else:
            parent.addChild(new_item)
            self.tree_changes.append(Change('add', new_value=new_item.text(0), old_value=parent.text(0)))
    
    @Slot()
    def handle_add_child(self) -> None:
        selected_item = self.ui.treeWidget.currentItem()
        if selected_item is None:
            return
        blank_item_numbers = [int(item.text(0)[8:]) for item in self.all_chilren_tree() 
                    if item.text(0)[0:8] == 'untitled']
        if len(blank_item_numbers) == 0:
            item_text = 'untitled1'
        else:
            item_text = 'untitled'+str(max(blank_item_numbers) + 1)
        new_item = QTreeWidgetItem([item_text])
        new_item.setFlags(new_item.flags() | Qt.ItemIsEditable)
        self.old_text_cache[new_item] = new_item.text(0)
        selected_item.addChild(new_item)
        self.tree_changes.append(Change('add', new_value=new_item.text(0), old_value=selected_item.text(0)))

    @Slot()
    def handle_delete_tree(self) -> None:
        selected_item = self.ui.treeWidget.currentItem()
        if selected_item is not None:
            parent = selected_item.parent()
            if parent is None:
                index = self.ui.treeWidget.indexOfTopLevelItem(selected_item)
                self.ui.treeWidget.takeTopLevelItem(index)
            else:
                parent.removeChild(selected_item)
        self.tree_changes.append(Change('delete', old_value=selected_item.text(0)))

class Dialog(QDialog):
    def __init__(self) -> None:
        super(Dialog, self).__init__()
        self.dialog = Ui_Dialog()
        self.dialog.setupUi(self)
        self.label = QLabel()
        self.dialog.verticalLayout.addWidget(self.label)

class Presenter:
    def __init__(self, db_file:str) -> None:
        self.expense_repo = SQLiteRepository[Expense](db_file, Expense)
        self.category_repo = SQLiteRepository[Category](db_file, Category)
        self.main_window = MainWindow(self.expense_repo, self.category_repo)
        self.dialog = Dialog()
        self.main_window.ui.save_button.clicked.connect(self.handle_saving_table)
        self.main_window.ui.save_button_tree.clicked.connect(self.handle_saving_tree)
        self.main_window.ui.tableWidget_2.setItem(0, 1, QTableWidgetItem(str(self.get_sum_by('day'))))
        self.main_window.ui.tableWidget_2.setItem(1, 1, QTableWidgetItem(str(self.get_sum_by('month'))))
        self.main_window.ui.tableWidget_2.setItem(2, 1, QTableWidgetItem(str(self.get_sum_by('year'))))
        self.main_window.show()
    
    def get_sum_by(self, time) -> int:
        conn = sqlite3.connect(self.expense_repo.db_file)
        cursor = conn.cursor()
        if time == 'day':
            cursor.execute("SELECT SUM(amount) FROM expense WHERE date LIKE '%' || ? || '%'", (datetime.now().strftime('%Y-%m-%d'),))
        if time == 'month':
            cursor.execute("SELECT SUM(amount) FROM expense WHERE date LIKE '%' || ? || '%'", (datetime.now().strftime('%Y-%m-__'),)) 
        if time == 'year':
            cursor.execute("SELECT SUM(amount) FROM expense WHERE date LIKE '%' || ? || '%'", (datetime.now().strftime('%Y-__-__'),)) 
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return row[0] if row[0] is not None else 0

    @Slot()
    def handle_saving_table(self) -> None:
        try:
            for change in self.main_window.changes:
                if change.operator == 'update':
                    if change.new_value == '':
                        continue
                    else:
                        if change.col == 'category':
                            value = self.category_repo.get_all({'name':change.new_value})[0].pk
                        elif change.col == 'date':
                            if not re.match(r'^[0-9]{4}-[0-9]{2}-[0-9]{2}$', change.new_value):
                                self.dialog.label.setText("")
                                self.dialog.label.setText(f'Date format illegal')
                                self.dialog.exec()   
                                return
                        else:
                            value = get_annotations(Expense)[change.col](change.new_value)
                        continue
        except ValueError:
            self.dialog.label.setText("")
            self.dialog.label.setText(f'Illegal value in ROW {change.row} and COLUMN {change.col}')
            self.dialog.exec()   
            return
        except IndexError:
            self.dialog.label.setText("")
            self.dialog.label.setText(f'Category not found')
            self.dialog.exec()   
            return

        for change in self.main_window.changes:
            if change.operator == 'update':
                if change.new_value == '':
                    self.expense_repo.update_item(change.row, change.col, None)
                else:
                    if change.col == 'category':
                        value = self.category_repo.get_all({'name':change.new_value})[0].pk
                    else:
                        value = get_annotations(Expense)[change.col](change.new_value)
                    self.expense_repo.update_item(change.row, change.col, value)
            if change.operator == 'add':
                last_row_id=self.expense_repo.add_empty()
                self.expense_repo.update_item(last_row_id, change.col, change.new_value)
            if change.operator == 'delete':
                self.expense_repo.delete(change.row)
        self.main_window.ui.tableWidget_2.setItem(0, 1, QTableWidgetItem(str(self.get_sum_by('day'))))
        self.main_window.ui.tableWidget_2.setItem(1, 1, QTableWidgetItem(str(self.get_sum_by('month'))))
        self.main_window.ui.tableWidget_2.setItem(2, 1, QTableWidgetItem(str(self.get_sum_by('year'))))
        self.main_window.changes = []

    @Slot()
    def handle_saving_tree(self) -> None:
        for change in self.main_window.tree_changes:
            if change.operator == 'update':
                all_tree_item_text = [item.text(0) for item in self.main_window.all_chilren_tree()]
                all_tree_item_text.remove(change.new_value)
                if change.new_value in all_tree_item_text:
                    self.dialog.label.setText("")
                    self.dialog.label.setText(f'Category already exists')
                    self.dialog.exec()
                    return
                continue   
        for change in self.main_window.tree_changes:
            if change.operator == 'update':
                rowid = self.category_repo.get_all({'name':change.old_value})[0].pk
                self.category_repo.update_item(rowid, 'name', change.new_value)
                for i in range(self.main_window.ui.tableWidget.rowCount()):
                    item = self.main_window.ui.tableWidget.item(i, 2)
                    if item and item.text() == change.old_value:
                        item.setText(change.new_value)
            if change.operator == 'add':
                last_row_id = self.category_repo.add_empty()
                if change.old_value != None:
                    parent_id = self.category_repo.get_all({'name':change.old_value})[0].pk
                else:
                    parent_id = None
                self.category_repo.update_item(last_row_id,'parent',parent_id)
                self.category_repo.update_item(last_row_id,'name',change.new_value)
            if change.operator == 'delete':
                rowid = self.category_repo.get_all({'name':change.old_value})[0].pk
                self.category_repo.delete(rowid)
        self.main_window.tree_changes = []


if __name__ == "__main__":
    app = QApplication(sys.argv)

    presenter = Presenter('tutorial.db')
   
    sys.exit(app.exec())
