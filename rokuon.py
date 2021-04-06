#!/usr/bin/env python3
import sys

from PyQt5 import QtCore
from PyQt5.QtWidgets import (
    QApplication,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QLabel,
)
import pulse_recorder as recorder


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("録音")
        self.resize(300, 200)
        self.setWindowFlags(
            QtCore.Qt.Window
            | QtCore.Qt.WindowStaysOnTopHint
            | QtCore.Qt.WindowCloseButtonHint
            | QtCore.Qt.WindowMinimizeButtonHint
        )

        main_layout = QVBoxLayout()

        # Top Layout -----------------------------
        top_layout = QVBoxLayout()

        self.label = QLabel("Choose an audio input channel")
        self.apps = QListWidget()

        # self.selection = None
        self.loadItems()

        # timer = QtCore.QTimer(self)
        # timer.timeout.connect(self.loadItems)
        # timer.start(5000)

        self.apps.itemClicked.connect(self.getItem)
        self.apps.itemDoubleClicked.connect(self.getItem)

        top_layout.addWidget(self.label)
        top_layout.addWidget(self.apps)

        # Bot Layout -----------------------------
        bot_layout = QHBoxLayout()

        self.recording = False
        self.data = None

        self.record_btn = QPushButton("Record", self)
        self.cancel_btn = QPushButton("Cancel", self)

        self.record_btn.setDisabled(True)
        self.cancel_btn.setDisabled(True)

        # Events
        self.record_btn.clicked.connect(self.toogleBtnClick)
        self.cancel_btn.clicked.connect(self.cancelBtnClick)

        # Add Widgets
        bot_layout.addWidget(self.record_btn)
        bot_layout.addWidget(self.cancel_btn)

        # Add Layouts
        main_layout.addLayout(top_layout)
        main_layout.addLayout(bot_layout)
        self.setLayout(main_layout)

    def loadItems(self):
        _, clients = recorder.load_sink_inputs()

        self.apps.clear()
        for index, app_name in clients.items():
            item = QListWidgetItem(app_name)
            item.setData(QtCore.Qt.UserRole, index)
            self.apps.addItem(item)

        # if (self.selection):
        #     self.apps.setCurrentIndex(self.selection)

    def getItem(self, listItem):
        # self.selection = self.apps.currentIndex()
        self.record_btn.setDisabled(False)

    def toogleBtnClick(self):
        self.recording = not self.recording
        if self.recording:
            index = self.apps.currentItem().data(QtCore.Qt.UserRole)
            self.data = recorder.record_start(index)
            self.record_btn.setText("Stop")
            self.cancel_btn.setDisabled(False)
        else:
            recorder.record_stop(self.data)
            self.record_btn.setText("Record")
            self.cancel_btn.setDisabled(True)

    def cancelBtnClick(self):
        self.recording = False
        self.record_btn.setText("Record")
        self.cancel_btn.setDisabled(True)

    def closeEvent(self, event):
        print("close")
        if self.data is not None:
            recorder.record_stop(self.data)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    main = MainWindow()
    main.show()

    sys.exit(app.exec_())
