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
    QPushButton,
    QVBoxLayout,
    QWidget,
    QLineEdit,
    QTabWidget,
    QFormLayout,
    QRadioButton,
    QMessageBox)
from matplotlib import pyplot



class MainWindow(QTabWidget):
    def __init__(self,parent=None):
        super(MainWindow, self).__init__(parent)
        self.setStyleSheet("background-color: lightblue;")
        self.setWindowTitle('Информация с биржи')
#виджеты для первой вкладки
        self.box1 = QComboBox()
        self.box1.addItems(["____", "Yandex", "Sberbank", "Tatneft"])
        self.box1.currentTextChanged.connect( self.text_changed )
        self.date_edit = QDateEdit(self)
        self.date_edit.editingFinished.connect(self.update)
        self.button = QPushButton("Получить данные")
        self.button.setCheckable(True)
        self.button.toggled.connect(self.the_button_was_toggled)
        self.table = QTableWidget(self)
        QTableWidgetItem()

#виджеты для второй вкладки
        self.button2 = QPushButton("Поcтроить график")
        self.button2.setCheckable(True)
        self.button2.toggled.connect(self.the_button_was_toggled2)
        self.line_edit = QLineEdit()
        self.input = QLineEdit()
        self.date_edit_s = QDateEdit(self)
        self.date_edit_s.editingFinished.connect(self.update_s)
        self.date_edit_f = QDateEdit(self)
        self.date_edit_f.editingFinished.connect(self.update_f)
        self.rb1m = QRadioButton('Одна минута', self)
        self.rb1m.toggled.connect(self.rbupdate)
        self.rb1m.res="1"
        self.rb10m = QRadioButton('Десть минут', self)
        self.rb10m.toggled.connect(self.rbupdate)
        self.rb10m.res="10"
        self.rb60m = QRadioButton('Час', self)
        self.rb60m.toggled.connect(self.rbupdate)
        self.rb60m.res="60"
        self.rb1d = QRadioButton('День', self)
        self.rb1d.toggled.connect(self.rbupdate)
        self.rb1d.res="24"
        self.rb1w = QRadioButton('Неделя', self)
        self.rb1w.clicked.connect(self.rbupdate)
        self.rb1w.res="7"
        self.rb1mo = QRadioButton('Месяц', self)
        self.rb1mo.toggled.connect(self.rbupdate)
        self.rb1mo.res="31"

        #
        self.tab1=QWidget()
        self.tab2=QWidget()


        #Добавить вкладки к верхнему окну
        self.addTab(self.tab1, "Все акции компании")
        self.addTab(self.tab2, "Статистика по акции")
        #Некоторые глобальные переменные, чтобы избежать ошибок при формировании запроса


        #
        self.tab1f()
        self.tab2f()


    def tab1f(self):
        layout=QFormLayout()
        layout.addWidget(QLabel("Выберите компанию"))
        layout.addWidget(self.box1)
        layout.addWidget(QLabel("Выберите дату"))
        layout.addWidget(self.date_edit)
        layout.addWidget(self.button)
        layout.addWidget(self.table)
        self.tab1.setLayout(layout)

    def tab2f(self):
        layout=QVBoxLayout()
        layout.addWidget(QLabel("Введите название (shortname) акции"))
        layout.addWidget(self.line_edit)
        layout.addWidget(QLabel("Выберите начальную дату "))
        layout.addWidget(self.date_edit_s)
        layout.addWidget(QLabel("Выберите конечную дату "))
        layout.addWidget(self.date_edit_f)
        layout.addWidget(QLabel("Выберите интервал"))
        layout.addWidget(self.rb1m)
        layout.addWidget(self.rb10m)
        layout.addWidget(self.rb60m)
        layout.addWidget(self.rb1d)
        layout.addWidget(self.rb1w)
        layout.addWidget(self.rb1mo)
        layout.addWidget(self.button2)
        self.tab2.setLayout(layout)

    def text_changed(self, s):
        self.companyname = s
    def update(self):
        value = self.date_edit.date()
        self.date1 = (str(value.toPyDate()))

    def the_button_was_toggled(self, checked):
        if checked == True:
            zapros = requests.get('https://iss.moex.com/iss/securities.json?q='+ self.companyname + "&date="+ self.date1).json()
            data = [{k : r[i] for i, k in enumerate(zapros['securities']['columns'])} for r in zapros['securities']['data']]
            if len(data) ==0:
                self.messege1=QMessageBox.warning(self,'Ошибка',"Нет данных для выбранных значений")
                self.show()
            else:
                final_data = (pandas.DataFrame(data))
                zag = list(final_data.columns.values)#получаем заголовки столбцов
                self.table.setColumnCount(len(zag))
                self.table.setHorizontalHeaderLabels(zag)

                self.table.setRowCount(0)#чтобы можно было для других значений повторно таблицу заполнить

                for i in range(0,len(final_data)):
                    item_val = final_data.iloc[i].tolist()

                    current_row_count = self.table.rowCount()
                    row_position = self.table.rowCount()
                    self.table.insertRow(row_position)
                    for j in range(0,len(zag)):
                        #print(item_val[j])
                        self.table.setItem(current_row_count, j, QTableWidgetItem(str(item_val[j])))

    def update_s(self):
        value = self.date_edit_s.date()
        self.startdate = (str(value.toPyDate()))

    def update_f(self):
        value = self.date_edit_f.date()
        self.findate = (str(value.toPyDate()))
    def rbupdate(self):
        rb = self.sender()
        if rb.isChecked():
            self.interval = rb.res

    def the_button_was_toggled2(self, checked):
        if checked == True:
            print('http://iss.moex.com/iss/engines/stock/markets/shares/securities/' + self.line_edit.text() + '/candles.json?from='+ self.startdate +'&till=' + self.findate +'&interval=' + self.interval)
            zapros2 = requests.get('http://iss.moex.com/iss/engines/stock/markets/shares/securities/' + self.line_edit.text() + '/candles.json?from='+ self.startdate +'&till=' + self.findate +'&interval=' + self.interval).json()
            data = [{k : r[i] for i, k in enumerate(zapros2['candles']['columns'])} for r in zapros2['candles']['data']]
            if len(data) ==0:
                self.messege=QMessageBox.warning(self,'Ошибка',"Нет данных для выбранных значений")
                self.show()
            else:
                frame = pandas.DataFrame(data)
                pyplot.plot(list(frame['close']))
                pyplot.show()


if __name__ == '__main__':
    app=QApplication(sys.argv)
    w=MainWindow()
    w.show()
    sys.exit(app.exec())
