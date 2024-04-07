from PySide6 import QtWidgets
from bookkeeper.view import ui_errordialog


class Dialog(QtWidgets.QDialog):

    def __init__(self) -> None:
        super(Dialog, self).__init__()
        self.dialog = ui_errordialog.Ui_Dialog()
        self.dialog.setupUi(self)
        self.label = QtWidgets.QLabel()
        self.dialog.verticalLayout.addWidget(self.label)
