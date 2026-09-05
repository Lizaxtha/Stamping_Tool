import os
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QMessageBox,
    QDialog,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QListWidget,
    QListWidgetItem,
    QFileDialog,
    QComboBox,
    QSlider,
)


class StampDialog(QDialog):

    def __init__(self, canvas_filter):
        super().__init__()

        self.canvas_filter = canvas_filter
        self.setWindowTitle("Stamps")
        self.setMinimumWidth(400)
        self.stamps = []

        layout = QVBoxLayout()

        title = QLabel("Choose one or more stamps")
        layout.addWidget(title)

        self.stamp_list = QListWidget()
        self.stamp_list.setSelectionMode(QListWidget.MultiSelection)
        self.stamp_list.setViewMode(QListWidget.IconMode)
        self.stamp_list.setIconSize(QSize(80, 80))
        self.stamp_list.setResizeMode(QListWidget.Adjust)

        self.load_builtin_stamps()
        layout.addWidget(self.stamp_list)

        custom_button = QPushButton("+ Custom Stamp")
        custom_button.clicked.connect(self.add_custom_stamp)
        layout.addWidget(custom_button)

        size_label = QLabel("Size")
        layout.addWidget(size_label)

        self.size_slider = QSlider(Qt.Horizontal)
        self.size_slider.setMinimum(10)
        self.size_slider.setMaximum(200)
        self.size_slider.setValue(100)
        layout.addWidget(self.size_slider)

        rotation_label = QLabel("Rotation")
        layout.addWidget(rotation_label)

        self.rotation_slider = QSlider(Qt.Horizontal)
        self.rotation_slider.setMinimum(0)
        self.rotation_slider.setMaximum(360)
        self.rotation_slider.setValue(0)
        layout.addWidget(self.rotation_slider)

        pattern_label = QLabel("Pattern")
        layout.addWidget(pattern_label)

        self.pattern_box = QComboBox()
        self.pattern_box.addItems([
            "Brush",
            "Random",
            "Circle",
            "Spiral",
            "Grid",
            "border",
            "Star",
        ])
        layout.addWidget(self.pattern_box)

        self.create_button = QPushButton("Start Stamping")
        self.create_button.clicked.connect(self.start_stamping)
        layout.addWidget(self.create_button)

        self.setLayout(layout)

    def add_custom_stamp(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Choose a stamp image",
            "",
            "Images (*.png *.jpg *.jpeg *.webp)",
        )

        if not file_path:
            return

        allowed_extensions = (".png", ".jpg", ".jpeg", ".webp")
        if not file_path.lower().endswith(allowed_extensions):
            return

        item = QListWidgetItem()
        item.setIcon(QIcon(file_path))
        item.setData(Qt.UserRole, file_path)
        self.stamp_list.addItem(item)
        self.stamps.append(file_path)

    def load_builtin_stamps(self):
        assets_folder = os.path.join(os.path.dirname(__file__), "assets")

        builtin_stamps = [
            "Heart.png",
            "C-moon.png",
            "Star.png",
            "Moon.png",
            "Leaf.png",
            "Autumn-Leaf.png",
            "Eifell-Tower.png",
            "Glittering-Star.png",
        ]

        for stamp in builtin_stamps:
            stamp_path = os.path.join(assets_folder, stamp)

            if os.path.exists(stamp_path):
                item = QListWidgetItem()
                item.setIcon(QIcon(stamp_path))
                item.setData(Qt.UserRole, stamp_path)
                self.stamp_list.addItem(item)
                self.stamps.append(stamp_path)

    def get_selected_stamps(self):
        selected_items = self.stamp_list.selectedItems()
        selected_stamps = []

        for item in selected_items:
            stamp_path = item.data(Qt.UserRole)
            if stamp_path:
                selected_stamps.append(stamp_path)

        return selected_stamps

    def start_stamping(self):
        selected_stamps = self.get_selected_stamps()

        if not selected_stamps:
            QMessageBox.warning(
                self,
                "No Stamp Selected",
                "Please select at least one stamp.",
            )
            return

        self.canvas_filter.selected_stamps = selected_stamps
        self.canvas_filter.current_stamp_index = 0

        self. canvas_filter.stamp_size = self.size_slider.value()
        self.canvas_filter.stamp_rotation = self.rotation_slider.value()
        
        self.canvas_filter.stamping_active = True
        self.accept()
