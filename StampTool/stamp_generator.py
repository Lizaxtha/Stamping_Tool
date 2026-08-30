from krita import *
from PyQt5.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QListWidget,
    QFileDIalog
)

class StampDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Stamps")
        self.setMinimumWidth(400)

        self.stamps=[]

        layout =QVBoxLayout()

        # title = QLabel("Stamp")
        # layout.addWidget(title)

        description = QLabel(
            "Choose one or more stamps"
        )
        layout.addWidget(description)

        custom_button = QPushButton("Custom Stamp")
        layout.addWidget(custom_button)

        self.setLayout(layout)
class StampTool(Extension):

    def __init__(self, parent):
        super().__init__(parent)

    def setup(self):
        pass

    def createActions(self,window):
        action=window.createAction(
            "stamp_tool_test",
            "Stamp Tool test",
            "tools/scripts"
        )

        action.triggered.connect(self.show_dialog)

    def show_dialog(self):
        dialog = StampDialog()
        dialog.exec_()


Krita.instance().addExtension(
    StampTool(Krita.instance())
)