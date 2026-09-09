import random
from krita import Krita
from PyQt5.QtCore import Qt, QObject, QEvent
from PyQt5.QtGui import QImage, QCursor, QTransform
from PyQt5.QtWidgets import QOpenGLWidget, QToolButton
from .patterns import PatternGenerator


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

        self.pattern ="Brush"
        self.random_offset = 400 #increase to increase area of splash in random pattern
        self.random_count = 10

        self.circle_radius = 300 # increase or decrease radius of circle [in pixels] in circle pattern

        self.spiral_turns = 5 #adjust no. of turns for spiral pattern
        self.spiral_spacing = 250 #adjust distance between turns in spiral pattern

        self.border_spacing = 150 # distance between each stamp
        self.border_margin = 60 # distance from the canvas border

        self.stamp_counter = 0
        

    def eventFilter(self, obj, event):
        if not self.stamping_active:
            self.mouse_down = False
            return False

        if event.type() == QEvent.KeyPress:
            if event.key() == Qt.Key_Escape:
                self.stamping_active = False
                self.mouse_down = False
                self.last_stamp_x = None
                self.last_stamp_y = None
                self.stamp_counter = 0
                return False

        if event.type() == QEvent.MouseButtonPress:

            if self.is_tool_button_event(obj):
                self.stamping_active = False
                self.mouse_down = False
                self.last_stamp_x = None
                self.last_stamp_y = None
                self.stamp_counter = 0
                return False
            
            if event.button() == Qt.LeftButton:

                if not self.is_canvas_event(obj):
                    return False
                
                position = self.get_document_position(obj)

                if position is None:
                    return False

                #pattern : random, circle and spiral
                if self.pattern in ("Random","Circle","Spiral","Border"):
                    canvas_width,canvas_height = self.get_canvas_dimensions()

                    positions = PatternGenerator.generate_positions(
                        self.pattern,
                        position.x(),
                        position.y(),
                        self.stamp_spacing,
                        self.random_offset,
                        canvas_width,
                        canvas_height,
                        stamp_count = self.random_count,
                        circle_radius=self.circle_radius,
                        spiral_turns=self.spiral_turns,
                        spiral_spacing=self.spiral_spacing,
                        border_spacing = self.border_spacing,
                        border_margin = self.border_margin
                    )

                    for stamp_x, stamp_y in positions:
                        self.place_stamp(stamp_x,stamp_y)
                        self.next_stamp()

                    return True

                # default brush pattern        
                self.last_stamp_x = position.x()
                self.last_stamp_y = position.y()
                self.mouse_down = True
                self.stamp_counter = 0

                canvas_width, canvas_height = self.get_canvas_dimensions()

                positions = PatternGenerator.generate_positions(
                    self.pattern,
                    position.x(),
                    position.y(),
                    self.stamp_spacing,
                    self.random_offset,
                    canvas_width,
                    canvas_height
                )

                for stamp_x,stamp_y in positions:
                    self.place_stamp(stamp_x,stamp_y)
                    self.next_stamp()

                return True

        if event.type() == QEvent.MouseMove:
            if not self.mouse_down:
                return False

            if not self.is_canvas_event(obj):
                return False

            if self.last_stamp_x is None or self.last_stamp_y is None:
                self.mouse_down =  False
                return False
                
            position = self.get_document_position(obj)

            if position is None:
                return False

            if self.pattern.lower() == "circle":
                return True

            x = position.x()
            y = position.y()

            dx = x-self.last_stamp_x
            dy = y-self.last_stamp_y
            distance = (dx*dx+dy*dy) ** 0.5

            if distance >= self.stamp_spacing:
                canvas_width, canvas_height = self.get_canvas_dimensions()

                positions = PatternGenerator.generate_positions(
                    self.pattern,
                    x,
                    y,
                    self.stamp_spacing,
                    self.random_offset,
                    canvas_width,
                    canvas_height
                )
                for stamp_x, stamp_y in positions:
                    self.place_stamp(stamp_x,stamp_y)
                    self.next_stamp()

                self.last_stamp_x = x
                self.last_stamp_y = y
                self.stamp_counter+=1
            return True

        if event.type() == QEvent.MouseButtonRelease:
            if event.button() == Qt.LeftButton:

                was_down = self.mouse_down

                self.mouse_down = False
                self.last_stamp_x = None
                self.last_stamp_y = None
                self.stamp_counter = 0

                if was_down and self.is_canvas_event(obj):
                    return True
                
                return False

        return False

    def get_canvas_dimensions(self):
        doc=Krita.instance().activeDocument()
        if doc:
            return doc.width(), doc.height()
        return None, None

    def next_stamp(self):
        if not self.selected_stamps:
            return

        self.current_stamp_index += 1

        if self.current_stamp_index >= len(self.selected_stamps):
            self.current_stamp_index = 0

    def is_canvas_event(self, obj):
        current = obj

        while current is not None:
            if isinstance(current, QOpenGLWidget):
                return True

            current = current.parent()
        return False

    def is_tool_button_event(self, obj):
        current = obj

        while current is not None:
            if isinstance(current, QToolButton):
                return True

            current = current.parent()

            return False

    def get_document_position(self, obj=None):
        window = Krita.instance().activeWindow()

        if window is None:
            return None

        view = window.activeView()

        if view is None:
            return None

        canvas_widget = self.get_canvas_from_object(obj)

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

    def get_canvas_from_object(self,obj):
        current = obj

        while current is not None:
            if isinstance(current,QOpenGLWidget):
                return current
            current = current.parent()
        return None
