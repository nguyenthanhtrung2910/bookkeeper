import re
import sqlite3
import inspect
import datetime

from PySide6 import QtWidgets
from PySide6 import QtCore

from bookkeeper.models import expense
from bookkeeper.models import category
from bookkeeper.repository import sqlite_repository
from bookkeeper.view import mainwindow
from bookkeeper.view import errordialog


class Presenter:
    """
    presenter
    """
    def __init__(self, db_file: str) -> None:
        self.expense_repo = sqlite_repository.SQLiteRepository[
            expense.Expense](db_file, expense.Expense)
        self.category_repo = sqlite_repository.SQLiteRepository[
            category.Category](db_file, category.Category)
        self.main_window = mainwindow.MainWindow(self.expense_repo,
                                                 self.category_repo)
        self.dialog = errordialog.Dialog()
        self.main_window.ui.button_save_expense.clicked.connect(
            self.handle_expense_table_saving)
        self.main_window.ui.button_save_category.clicked.connect(
            self.handle_category_tree_saving)
        self.main_window.ui.combo_box_chose_category.currentIndexChanged.connect(
            self.display_sum_amount)
        #diplay right away sum all amount by row in expense table
        self.display_sum_amount(0)
        #set sum amout for now
        self.main_window.ui.table_widget_budget.setItem(
            0, 1,
            QtWidgets.QTableWidgetItem(str(self.get_sum_amount_by('day'))))
        self.main_window.ui.table_widget_budget.setItem(
            1, 1,
            QtWidgets.QTableWidgetItem(str(self.get_sum_amount_by('month'))))
        self.main_window.ui.table_widget_budget.setItem(
            2, 1,
            QtWidgets.QTableWidgetItem(str(self.get_sum_amount_by('year'))))

        self.main_window.show()

    def get_sum_amount_by(self, time: str) -> int:
        conn = sqlite3.connect(self.expense_repo.db_file)
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()
        if time == 'day':
            cursor.execute(
                "SELECT SUM(amount) FROM expense WHERE date LIKE '%' || ? || '%'",
                (datetime.datetime.now().strftime('%Y-%m-%d'), ))
        if time == 'month':
            cursor.execute(
                "SELECT SUM(amount) FROM expense WHERE date LIKE '%' || ? || '%'",
                (datetime.datetime.now().strftime('%Y-%m-__'), ))
        if time == 'year':
            cursor.execute(
                "SELECT SUM(amount) FROM expense WHERE date LIKE '%' || ? || '%'",
                (datetime.datetime.now().strftime('%Y-__-__'), ))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return row[0] if row[0] is not None else 0

    def display_sum_amount(self, index: int) -> None:
        category = self.main_window.ui.combo_box_chose_category.currentText()
        if not category:
            return
        conn = sqlite3.connect(self.expense_repo.db_file)
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()
        if category == 'All':
            cursor.execute("SELECT SUM(amount) FROM expense")
        else:
            category_id = self.category_repo.get_all({'name': category})[0].pk
            cursor.execute(
                "SELECT SUM(amount) FROM expense WHERE category = ?",
                (category_id, ))
        row = cursor.fetchone()
        sum_result = row[0] if row[0] is not None else 0
        self.main_window.ui.lineEdit.setText(str(sum_result))
        cursor.close()
        conn.close()

    @QtCore.Slot()
    def handle_expense_table_saving(self) -> None:
        #check if all change illegal
        try:
            for change in self.main_window.expense_table_changes:
                if change.operator == 'update':
                    if change.new_value == '':
                        continue
                    if change.col == 'category':
                        value = self.category_repo.get_all(
                            {'name': change.new_value})[0].pk
                    elif change.col == 'date':
                        if not re.match(r'^[0-9]{4}-[0-9]{2}-[0-9]{2}$',
                                        change.new_value):
                            self.dialog.label.setText("")
                            self.dialog.label.setText(
                                'Date format illegal')
                            self.dialog.exec()
                            return
                    else:
                        value = inspect.get_annotations(
                            expense.Expense)[change.col](change.new_value)
                    continue

        except ValueError:
            self.dialog.label.setText("")
            self.dialog.label.setText(
                f'Illegal value in ROW {change.row} and COLUMN {change.col}')
            self.dialog.exec()
            return
        except IndexError:
            self.dialog.label.setText("")
            self.dialog.label.setText(f'Category {change.new_value} not found')
            self.dialog.exec()
            return

        #perform changes in database
        for change in self.main_window.expense_table_changes:
            if change.operator == 'update':
                if change.new_value == '':
                    self.expense_repo.update_item(change.row, change.col, None)
                else:
                    if change.col == 'category':
                        value = self.category_repo.get_all(
                            {'name': change.new_value})[0].pk
                    else:
                        value = inspect.get_annotations(
                            expense.Expense)[change.col](change.new_value)
                    self.expense_repo.update_item(change.row, change.col,
                                                  value)
            if change.operator == 'add':
                last_row_id = self.expense_repo.add_empty()
                self.expense_repo.update_item(last_row_id, change.col,
                                              change.new_value)
            if change.operator == 'delete':
                self.expense_repo.delete(change.row)

        #diplay sum all amount by row in expense table
        self.main_window.ui.table_widget_budget.setItem(
            0, 1,
            QtWidgets.QTableWidgetItem(str(self.get_sum_amount_by('day'))))
        self.main_window.ui.table_widget_budget.setItem(
            1, 1,
            QtWidgets.QTableWidgetItem(str(self.get_sum_amount_by('month'))))
        self.main_window.ui.table_widget_budget.setItem(
            2, 1,
            QtWidgets.QTableWidgetItem(str(self.get_sum_amount_by('year'))))

        #clear cache
        self.main_window.expense_table_changes = []

    @QtCore.Slot()
    def handle_category_tree_saving(self) -> None:
        #check if all change illegal
        for change in self.main_window.category_tree_changes:
            if change.operator == 'update':
                all_tree_item_text = [
                    item.text(0)
                    for item in self.main_window.all_chilren_tree()
                ]
                try:
                    all_tree_item_text.remove(change.new_value)
                except ValueError:
                    continue
                if change.new_value in all_tree_item_text:
                    self.dialog.label.setText("")
                    self.dialog.label.setText('Category already exists')
                    self.dialog.exec()
                    return

        #perform changes in database
        for change in self.main_window.category_tree_changes:
            if change.operator == 'update':
                rowid = self.category_repo.get_all({'name':
                                                    change.old_value})[0].pk
                self.category_repo.update_item(rowid, 'name', change.new_value)
                #update right away category in expense table
                for i in range(
                        self.main_window.ui.table_widget_expense.rowCount()):
                    item = self.main_window.ui.table_widget_expense.item(i, 2)
                    if item and item.text() == change.old_value:
                        item.setText(change.new_value)
            if change.operator == 'add':
                last_row_id = self.category_repo.add_empty()
                if change.old_value is not None:
                    parent_id = self.category_repo.get_all(
                        {'name': change.old_value})[0].pk
                else:
                    parent_id = None
                self.category_repo.update_item(last_row_id, 'parent',
                                               parent_id)
                self.category_repo.update_item(last_row_id, 'name',
                                               change.new_value)
            if change.operator == 'delete':
                rowid = self.category_repo.get_all({'name':
                                                    change.old_value})[0].pk
                self.category_repo.delete(rowid)

        #change also categories in combo box
        self.main_window.ui.combo_box_chose_category.clear()
        self.main_window.ui.combo_box_chose_category.addItem('All')
        for tree_widget_item in self.main_window.all_chilren_tree():
            self.main_window.ui.combo_box_chose_category.addItem(
                tree_widget_item.text(0))

        #clear cache
        self.main_window.category_tree_changes = []
