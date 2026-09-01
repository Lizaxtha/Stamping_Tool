from krita import *
import os
from PyQt5.QtCore import QSize,Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QListWidget,
    QListWidgetItem,
    QFileDialog,
    QComboBox,
    QSlider
)

class StampDialog(QDialog):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Stamps")
        self.setMinimumWidth(400)

        self.stamps=[]

        layout =QVBoxLayout()

        title = QLabel("Choose one or more stamps")
        layout.addWidget(title)

        self.stamp_list = QListWidget()

        self.stamp_list.setSelectionMode(
            QListWidget.MultiSelection
        )

        self.stamp_list.setViewMode(
            QListWidget.IconMode
        )

        self.stamp_list.setIconSize(
            QSize(80,80)
        )

        self.stamp_list.setResizeMode(
            QListWidget.Adjust
        )

        self.load_builtin_stamps()

        layout.addWidget(self.stamp_list)

        custom_button=QPushButton("+ Custom Stamp")
        custom_button.clicked.connect(self.add_custom_stamp)

        layout.addWidget(custom_button)

        self.setLayout(layout)

# for Size control
        size_label =QLabel("Size")
        layout.addWidget(size_label)

        self.size_slider=QSlider(Qt.Horizontal)

        self.size_slider.setMinimum(10)
        self.size_slider.setMaximum(200)
        self.size_slider.setValue(100)

        layout.addWidget(self.size_slider)

# For Rotation control
        rotation_label=QLabel("Rotation")
        layout.addWidget(rotation_label)

        self.rotation_slider=QSlider(Qt.Horizontal)
        
        self.rotation_slider.setMinimum(0)
        self.rotation_slider.setMaximum(360)
        self.rotation_slider.setValue(0)
        
        layout.addWidget(self.rotation_slider)

# for Pattern control
        pattern_label =QLabel("Pattern")
        layout.addWidget(pattern_label)

        self.pattern_box=QComboBox()

        self.pattern_box.addItems([
            "Brush",
            "Random",
            "Circle",
            "Spiral",
            "Grid",
            "border",
            "Star"
        ])

        layout.addWidget(self.pattern_box)

        create_button=QPushButton("Create")
        layout.addWidget(create_button)


    def add_custom_stamp(self):

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Choose a stamp image",
            "",
            "Images (*.png *.jpg *.jpeg *.webp)"
        )

        if not file_path:
            return

        allowed_extensions =(".png",".jpg",".jpeg",".webp")

        if not file_path.lower().endswith(allowed_extensions):
            return

        item =QListWidgetItem()
        item.setIcon(QIcon(file_path))

        self.stamp_list.addItem(item)
        self.stamps.append(file_path)


    def load_builtin_stamps(self):

        assets_folder =os.path.join(
            os.path.dirname(__file__),
            "assets"
        )

        builtin_stamps=[
        "Heart.png",
        "C-moon.png",
        "Star.png",
        "Moon.png",
        "Leaf.png",
        "Autumn-Leaf.png",
        "Eifell-Tower.png",
        "Glittering-Star.png"

        ]

        for stamp in builtin_stamps:

            stamp_path =os.path.join(
                assets_folder,
                stamp
            )

            if os.path.exists(stamp_path):

                item=QListWidgetItem()
                item.setIcon(QIcon(stamp_path))

                self.stamp_list.addItem(item)

                self.stamps.append(stamp_path)
class StampTool(Extension):

    def __init__(self, parent):
        super().__init__(parent)

    def setup(self):
        pass

    def createActions(self,window):
        action=window.createAction(
            "stamp_tool",
            "Stamp Tool",
            "tools/scripts"
        )

        action.triggered.connect(self.show_dialog)

    def show_dialog(self):
        dialog = StampDialog()
        dialog.exec_()


Krita.instance().addExtension(
    StampTool(Krita.instance())
)