from krita import Krita, Extension
from PyQt5.QtWidgets import QApplication
from .stamp_dialog import StampDialog
from .canvas_stamper import CanvasClickFilter
class StampTool(Extension):
    def __init__(self, parent):
        super().__init__(parent)
        self.canvas_filter = CanvasClickFilter()
        self.dialog = None
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
        self.canvas_filter.stamping_active = False
        self.canvas_filter.mouse_down = False
        self.canvas_filter.last_stamp_x = None
        self.canvas_filter.last_stamp_y = None
        self.canvas_filter.stamp_counter = 0

        if self.dialog is None:
            self.dialog = StampDialog(self.canvas_filter)
            self.dialog.rejected.connect(self.stop_stamping)

        self.dialog.show()
        self.dialog.raise_()
        self.dialog.activateWindow()

    def stop_stamping(self):
        self.canvas_filter.stamping_active = False
        self.canvas_filter.mouse_down = False
        self.canvas_filter.last_stamp_x = None
        self.canvas_filter.last_stamp_y = None
        self.canvas_filter.stamp_counter = 0

Krita.instance().addExtension(
    StampTool(Krita.instance())
)
