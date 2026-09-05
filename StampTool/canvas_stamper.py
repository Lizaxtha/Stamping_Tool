from krita import Krita
from PyQt5.QtCore import Qt, QObject, QEvent
from PyQt5.QtGui import QImage, QCursor, QTransform
from PyQt5.QtWidgets import QWidget, QOpenGLWidget


class CanvasClickFilter(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.stamping_active = False
        self.selected_stamps = []
        self.current_stamp_index = 0
        self.mouse_down = False

        self.last_stamp_x = None
        self.last_stamp_y = None
        self.stamp_spacing = 30

        self.stamp_size = 100
        self.stamp_rotation = 0
        

    def eventFilter(self, obj, event):
        if not self.stamping_active:
            return False

        if event.type() == QEvent.MouseButtonPress:
            if event.button() == Qt.LeftButton:
                position = self.get_document_position()

                if position is not None:
                    self.mouse_down = True

                    self.last_stamp_x=position.x()
                    self.last_stamp_y=position.y()

                    self.place_stamp(
                        position.x(),
                        position.y())
                    self.next_stamp()
                    return True

        if event.type() == QEvent.MouseMove:
            if self.mouse_down:
                position = self.get_document_position()

                if position is not None:

                    x = position.x()
                    y=position.y()

                    dx = x-self.last_stamp_x
                    dy=y-self.last_stamp_y

                    distance = (dx*dx+dy*dy)**0.5

                    if distance >= self.stamp_spacing:

                        self.place_stamp(x,y)
                        self.next_stamp()
                        self.last_stamp_x = x
                        self.last_stamp_y = y
                    return True

        if event.type() == QEvent.MouseButtonRelease:
            if event.button() == Qt.LeftButton:
                self.mouse_down = False
                self.last_stamp_x = None
                self.last_stamp_y = None
                return True

        return False

    def next_stamp(self):
        if not self.selected_stamps:
            return

        self.current_stamp_index += 1

        if self.current_stamp_index >= len(self.selected_stamps):
            self.current_stamp_index = 0

    def get_document_position(self):
        window = Krita.instance().activeWindow()

        if window is None:
            return None

        view = window.activeView()

        if view is None:
            return None

        canvas_widget = self.get_canvas_widget()

        if canvas_widget is None:
            return None

        global_pos = QCursor.pos()
        canvas_pos = canvas_widget.mapFromGlobal(global_pos)

        if not canvas_widget.rect().contains(canvas_pos):
            return None

        flake_to_image = view.flakeToImageTransform()
        canvas_to_flake = view.flakeToCanvasTransform().inverted()[0]
        canvas_to_image = canvas_to_flake * flake_to_image

        image_pos = canvas_to_image.map(canvas_pos)
        return image_pos

    def place_stamp(self, x, y):
        if not self.selected_stamps:
            return

        stamp_path = self.selected_stamps[self.current_stamp_index]
        image = QImage(stamp_path)

        if image.isNull():
            return

        image = image.convertToFormat(QImage.Format_ARGB32)

        image = image.scaled(
            self.stamp_size,
            self.stamp_size,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation,
        )

        if self.stamp_rotation !=0:
            transform = QTransform()
            transform.rotate(self.stamp_rotation)
            image=image.transformed(
                transform,
                Qt.SmoothTransformation
            )

        width = image.width()
        height = image.height()

        document = Krita.instance().activeDocument()

        if document is None:
            return

        layer = document.activeNode()

        if layer is None:
            return

        bits = image.bits()
        bits.setsize(image.byteCount())
        data = bytes(bits)

        draw_x = int(x - width / 2)
        draw_y = int(y - height / 2)

        layer.setPixelData(
            data,
            draw_x,
            draw_y,
            width,
            height,
        )
        document.refreshProjection()

    def get_canvas_widget(self):
        window = Krita.instance().activeWindow()

        if window is None:
            return None

        qwindow = window.qwindow()

        if qwindow is None:
            return None

        view = window.activeView()

        if view is None:
            return None

        view_widget = qwindow.findChild(QWidget, "view_0")

        if view_widget is None:
            return None

        canvas_widget = view_widget.findChild(QOpenGLWidget)
        return canvas_widget
