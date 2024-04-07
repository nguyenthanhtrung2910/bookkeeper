import sys
from PySide6 import QtWidgets
from bookkeeper.presenter import presenter
from bookkeeper.repository import sqlite_repository
from bookkeeper.models import expense, category

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    presenter = presenter.Presenter('book.db')

    sys.exit(app.exec())
 