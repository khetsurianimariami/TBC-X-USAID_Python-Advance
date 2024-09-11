def OpenSlice1(self, state):
    pixmap = QPixmap("E:\BEATSON_PROJECT\python\GUI\home.png")
    self.lbl = QLabel(self)  # Qlabel used to display QPixmap
    self.lbl.setPixmap(pixmap)
    if state == Qt.Checked:
        self.lbl.show()
    else:
        self.lbl.hide()