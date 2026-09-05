from krita import Krita, Extension
from PyQt5.QtWidgets import QApplication

from .stamp_dialog import StampDialog
from .canvas_stamper import CanvasClickFilter


class StampTool(Extension):
    def __init__(self, parent):
        super().__init__(parent)
        self.canvas_filter = CanvasClickFilter()
        self.install_canvas_filter()

    def install_canvas_filter(self):
        app = QApplication.instance()

        if app:
            app.installEventFilter(self.canvas_filter)

    def setup(self):
        pass

    def createActions(self, window):
        action = window.createAction(
            "stamp_tool",
            "Stamp Tool",
            "tools/scripts",
        )

        action.triggered.connect(self.show_dialog)

    def show_dialog(self):
        dialog = StampDialog(self.canvas_filter)
        dialog.exec_()


Krita.instance().addExtension(
    StampTool(Krita.instance())
)
