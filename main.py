import sys
import pandas
import requests
from PyQt6.QtWidgets import (
    QTableWidgetItem,
    QApplication,
    QTableWidget,
    QComboBox,
    QDateEdit,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle('Информация с биржи')
        box1 = QComboBox()
        box1.addItems(["Yandex", "Sberbank", "Tatneft"])
        box1.currentTextChanged.connect( self.text_changed )
        self.date_edit = QDateEdit(self)
        self.date_edit.editingFinished.connect(self.update)
        button = QPushButton("Получить данные")
        button.setCheckable(True)
        button.clicked.connect(self.the_button_was_toggled)
        self.table = QTableWidget(self)
        QTableWidgetItem()

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Выберите компанию"))
        layout.addWidget(box1)
        layout.addWidget(QLabel("Выберите дату"))
        layout.addWidget(self.date_edit)
        layout.addWidget(button)
        layout.addWidget(self.table)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def text_changed(self, s):
        self.companyname = s

    def update(self):
        value = self.date_edit.date()
        self.date1 = (str(value.toPyDate()))

    def the_button_was_toggled(self, checked):
        if checked == True:
            print('https://iss.moex.com/iss/securities.json?q='+ self.companyname + "&date="+ self.date1)
            zapros = requests.get('https://iss.moex.com/iss/securities.json?q='+ self.companyname + "&date="+ self.date1).json()
            print(zapros)
            data = [{k : r[i] for i, k in enumerate(zapros['securities']['columns'])} for r in zapros['securities']['data']]
            final_data = (pandas.DataFrame(data))
            zag = list(final_data.columns.values)#получаем заголовки столбцов
            self.table.setColumnCount(len(zag))
            self.table.setHorizontalHeaderLabels(zag)

            for i in range(0,len(final_data)):
                item_val = final_data.iloc[i].tolist()
                current_row_count = self.table.rowCount()
                row_position = self.table.rowCount()
                self.table.insertRow(row_position)
                for j in range(0,len(zag)):
                    self.table.setItem(current_row_count, j, QTableWidgetItem(str(item_val[j])))

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
