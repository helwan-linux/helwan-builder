# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PyQt5.QtCore import Qt

class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("About hel-pkg")
        self.setMinimumSize(400, 200) # تحديد حجم افتراضي مناسب

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        # معلومات التطبيق
        title_label = QLabel("<h1><b>hel-pkg: PKGBUILD Generator</b></h1>")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        version_label = QLabel("Version: 1.0.0")
        version_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(version_label)

        dev_label = QLabel("Developed by: Saeed badrelden")
        dev_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(dev_label)

        desc_label = QLabel("This application helps you generate PKGBUILD files for Arch Linux packages.")
        desc_label.setAlignment(Qt.AlignCenter)
        desc_label.setWordWrap(True) # لضمان التفاف النص لو طويل
        layout.addWidget(desc_label)

        tech_label = QLabel("<i>Built with PyQt5.</i>")
        tech_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(tech_label)

        layout.addStretch(1) # لدفع الأزرار للأسفل

        # زر الإغلاق
        close_button_layout = QHBoxLayout()
        close_button_layout.addStretch(1)
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.accept)
        close_button_layout.addWidget(close_button)
        close_button_layout.addStretch(1)
        
        layout.addLayout(close_button_layout)

        self.setLayout(layout)
