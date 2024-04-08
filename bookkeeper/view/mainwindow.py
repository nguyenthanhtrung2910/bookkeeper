import dataclasses
import datetime

from PySide6 import QtWidgets
from PySide6 import QtCore
from PySide6 import QtGui

from bookkeeper.models import expense
from bookkeeper.models import category
from bookkeeper.repository import abstract_repository
from bookkeeper.view import ui_mainwindow


@dataclasses.dataclass(slots=True)
class Change:
    """
    Object to save change in table
    """
    operator: str
    row: int | None = None
    col: str | None = None
    new_value: str | None = None
    old_value: str | None = None
    change_on_item: QtWidgets.QTreeWidgetItem | None = None


class MainWindow(QtWidgets.QMainWindow):

    def __init__(
        self,
        esp_repo: abstract_repository.AbstractRepository[expense.Expense],
        cate_repo: abstract_repository.AbstractRepository[category.Category]
    ) -> None:
        super(MainWindow, self).__init__()
        self.ui = ui_mainwindow.Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.table_widget_expense.setColumnWidth(0, 200)
        self.ui.table_widget_expense.setColumnWidth(1, 80)
        self.ui.table_widget_expense.setColumnWidth(2, 80)
        self.ui.table_widget_expense.setColumnWidth(3, 305)

        self.ui.table_widget_budget.setColumnWidth(0, 80)
        self.ui.table_widget_budget.setColumnWidth(1, 293)
        self.ui.table_widget_budget.setColumnWidth(2, 293)

        #cache to save expense table changes
        self.expense_table_changes: list[Change] = []
        #cache to save category changes
        self.category_tree_changes: list[Change] = []
        #cache to save pre-last category tree item text
        self.old_text_cache: dict[QtWidgets.QTreeWidgetItem, str] = {}

        #write data to table
        data = esp_repo.get_all()
        self.ui.table_widget_expense.setRowCount(len(data))
        for i, espense in enumerate(data):
            for j in range(self.ui.table_widget_expense.columnCount()):
                attr_name = self.ui.table_widget_expense.horizontalHeaderItem(
                    j).text().lower()
                item = getattr(espense, attr_name)
                if item is None:
                    item = ''
                else:
                    if attr_name == 'category':
                        item = cate_repo.get(getattr(espense, attr_name)).name
                self.ui.table_widget_expense.setItem(
                    i, j, QtWidgets.QTableWidgetItem(str(item)))

        #write data to tree
        tree_widgets: list[QtWidgets.QTreeWidgetItem] = []
        data_tree = cate_repo.get_all()
        for _ in data_tree:
            tree_widgets.append(QtWidgets.QTreeWidgetItem())
        for i, row in enumerate(data_tree):
            tree_widgets[i].addChildren([
                tree_widgets[cat.pk - 1]
                for cat in row.get_all_children(cate_repo)
            ])
            tree_widgets[i].setText(0, row.name)
            tree_widgets[i].setFlags(tree_widgets[i].flags()
                                     | QtCore.Qt.ItemIsEditable)
            self.old_text_cache[tree_widgets[i]] = tree_widgets[i].text(0)

        self.ui.tree_widget_category.setColumnCount(1)
        self.ui.tree_widget_category.addTopLevelItems(tree_widgets)

        self.ui.combo_box_chose_category.addItem('All')
        for tree_widget_item in self.all_chilren_tree():
            self.ui.combo_box_chose_category.addItem(tree_widget_item.text(0))

        #set save button image
        pixmap = QtGui.QPixmap("assets/install.png")
        icon = QtGui.QIcon(pixmap)
        self.ui.button_save_expense.setIcon(icon)
        self.ui.button_save_category.setIcon(icon)

        #set add button image
        pixmap = QtGui.QPixmap("assets/add.png")
        icon = QtGui.QIcon(pixmap)
        self.ui.button_add_expense.setIcon(icon)
        self.ui.button_add_category.setIcon(icon)

        #set delete button image
        pixmap = QtGui.QPixmap("assets/delete.png")
        icon = QtGui.QIcon(pixmap)
        self.ui.button_delete_expense.setIcon(icon)
        self.ui.button_delete_category.setIcon(icon)

        #set add child button image
        pixmap = QtGui.QPixmap("assets/folder.png")
        icon = QtGui.QIcon(pixmap)
        self.ui.button_add_child_category.setIcon(icon)

        self.ui.table_widget_expense.itemChanged.connect(
            self.handle_expense_table_updating)
        self.ui.button_add_expense.clicked.connect(
            self.handle_expense_table_adding_row)
        self.ui.button_delete_expense.clicked.connect(
            self.handle_expense_table_deleting_row)

        self.ui.tree_widget_category.itemChanged.connect(
            self.handle_category_tree_updating)
        self.ui.button_add_category.clicked.connect(
            self.handle_category_tree_adding)
        self.ui.button_add_child_category.clicked.connect(
            self.handle_category_tree_adding_child)
        self.ui.button_delete_category.clicked.connect(
            self.handle_category_tree_deleting)

    @QtCore.Slot(QtWidgets.QTableWidgetItem)
    def handle_expense_table_updating(
            self, item: QtWidgets.QTableWidgetItem) -> None:
        row = item.row() + 1
        col = item.column()
        value = item.text()
        column_name = self.ui.table_widget_expense.horizontalHeaderItem(
            col).text().lower()
        #we only save newest change for one item
        for c in self.expense_table_changes:
            if c.operator == 'update' and c.change_on_item is item:
                c.new_value = value
                return
        self.expense_table_changes.append(
            Change('update', row, column_name, value, change_on_item=item))

    @QtCore.Slot()
    def handle_expense_table_adding_row(self) -> None:
        current_row_count = self.ui.table_widget_expense.rowCount()
        self.ui.table_widget_expense.insertRow(current_row_count)
        #auto write for new row current date
        self.ui.table_widget_expense.setItem(
            self.ui.table_widget_expense.rowCount() - 1, 0,
            QtWidgets.QTableWidgetItem(
                datetime.datetime.now().strftime('%Y-%m-%d')))
        self.expense_table_changes.append(
            Change('add',
                   col='date',
                   new_value=datetime.datetime.now().strftime('%Y-%m-%d')))

    @QtCore.Slot()
    def handle_expense_table_deleting_row(self) -> None:
        selected_row = self.ui.table_widget_expense.currentRow()
        if selected_row >= 0:
            self.ui.table_widget_expense.removeRow(selected_row)
        self.expense_table_changes.append(Change('delete', selected_row + 1))

    @QtCore.Slot(QtWidgets.QTreeWidgetItem, int)
    def handle_category_tree_updating(self, item: QtWidgets.QTreeWidgetItem,
                                      column: int) -> None:
        if item is not None:
            old_text = self.old_text_cache.get(
                item, '')  # Get the old text from cache
            new_text = item.text(column)  # Get the new text after the change
            self.old_text_cache[item] = new_text
        #we only save newest change for one item
        for c in self.category_tree_changes:
            if c.operator == 'update' and c.change_on_item is item:
                c.new_value = new_text
                return
        self.category_tree_changes.append(
            Change('update', new_value=new_text, old_value=old_text, change_on_item=item))

    def get_child_items(
        self, parent_item: QtWidgets.QTreeWidgetItem
    ) -> list[QtWidgets.QTreeWidgetItem]:
        items = []
        child_count = parent_item.childCount()
        for i in range(child_count):
            child_item = parent_item.child(i)
            items.append(child_item)
            items.extend(self.get_child_items(child_item))
        return items

    def all_chilren_tree(self) -> list[QtWidgets.QTreeWidgetItem]:
        items = []
        top_level_item_count = self.ui.tree_widget_category.topLevelItemCount()
        for i in range(top_level_item_count):
            top_level_item = self.ui.tree_widget_category.topLevelItem(i)
            items.append(top_level_item)
            items.extend(self.get_child_items(top_level_item))
        return items

    @QtCore.Slot()
    def handle_category_tree_adding(self) -> None:
        selected_item = self.ui.tree_widget_category.currentItem()
        #new item by default have name untitled with different suffic
        blank_item_numbers = [
            int(item.text(0)[8:]) for item in self.all_chilren_tree()
            if item.text(0)[0:8] == 'untitled'
        ]
        if len(blank_item_numbers) == 0:
            item_text = 'untitled1'
        else:
            item_text = 'untitled' + str(max(blank_item_numbers) + 1)

        new_item = QtWidgets.QTreeWidgetItem([item_text])
        new_item.setFlags(new_item.flags() | QtCore.Qt.ItemIsEditable)
        self.old_text_cache[new_item] = new_item.text(0)
        if selected_item is None:
            self.ui.tree_widget_category.addTopLevelItem(new_item)
            self.category_tree_changes.append(
                Change('add', new_value=new_item.text(0), old_value=None))
        else:
            parent = selected_item.parent()
            if parent is None:
                self.ui.tree_widget_category.addTopLevelItem(new_item)
                self.category_tree_changes.append(
                    Change('add', new_value=new_item.text(0), old_value=None))
            else:
                parent.addChild(new_item)
                self.category_tree_changes.append(
                    Change('add',
                            new_value=new_item.text(0),
                            old_value=parent.text(0)))

    @QtCore.Slot()
    def handle_category_tree_adding_child(self) -> None:
        selected_item = self.ui.tree_widget_category.currentItem()
        if selected_item is None:
            return

        #new item by default have name untitled with different suffic
        blank_item_numbers = [
            int(item.text(0)[8:]) for item in self.all_chilren_tree()
            if item.text(0)[0:8] == 'untitled'
        ]
        if len(blank_item_numbers) == 0:
            item_text = 'untitled1'
        else:
            item_text = 'untitled' + str(max(blank_item_numbers) + 1)

        new_item = QtWidgets.QTreeWidgetItem([item_text])
        new_item.setFlags(new_item.flags() | QtCore.Qt.ItemIsEditable)
        self.old_text_cache[new_item] = new_item.text(0)
        selected_item.addChild(new_item)
        self.category_tree_changes.append(
            Change('add',
                   new_value=new_item.text(0),
                   old_value=selected_item.text(0)))

    @QtCore.Slot()
    def handle_category_tree_deleting(self) -> None:
        selected_item = self.ui.tree_widget_category.currentItem()
        if selected_item is not None:
            parent = selected_item.parent()
            if parent is None:
                index = self.ui.tree_widget_category.indexOfTopLevelItem(
                    selected_item)
                self.ui.tree_widget_category.takeTopLevelItem(index)
            else:
                parent.removeChild(selected_item)
        self.category_tree_changes.append(
            Change('delete', old_value=selected_item.text(0)))
