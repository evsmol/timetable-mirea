from datetime import datetime

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QMainWindow, QAbstractItemView
from PySide6.QtWidgets import QGridLayout, QLabel, QPushButton, \
    QListWidget, QListWidgetItem, QLineEdit
from PySide6.QtGui import QIcon

from data.filter_func import load_teacher, load_group, load_auditorium, \
    change_teacher, change_group, change_auditorium

from logging_func import logging


class FilterForm(QMainWindow):
    """Класс окна выбора избранных групп, преподавателей и аудиторий."""

    def __init__(self, MainForm):
        super().__init__()
        self.main_form = MainForm
        self.initUI()

    def initUI(self):
        logging(datetime.now(), 'WARNING', 'Открытие формы выбора избранных '
                                           'групп, преподавателей и аудиторий')

        self.setWindowTitle('Избранные группы и преподаватели')
        self.setWindowIcon(QIcon('image/filter.png'))

        # создание виджетов
        self.layout = QGridLayout()

        # добавление информационного текста
        self.label_info = QLabel('Выберите группы, преподавателей и аудитории '
                                 'для отображения в главном окне программы.')
        self.layout.addWidget(self.label_info, 0, 0, 1, 3)

        # добавление кнопки выделения групп
        self.group_btn = QPushButton('Выделить / снять выделение')
        self.group_btn.clicked.connect(self.button_click_selected_group)
        self.layout.addWidget(self.group_btn, 1, 0, 1, 1)
        self.group_flag = 1

        # добавление кнопки выделения преподавателей
        self.teacher_btn = QPushButton('Выделить / снять выделение')
        self.teacher_btn.clicked.connect(self.button_click_selected_teacher)
        self.layout.addWidget(self.teacher_btn, 1, 1, 1, 1)
        self.teacher_flag = 1

        # добавление кнопки выделения аудиторий
        self.auditorium_btn = QPushButton('Выделить / снять выделение')
        self.auditorium_btn.clicked.connect(
            self.button_click_selected_auditorium
        )
        self.layout.addWidget(self.auditorium_btn, 1, 2, 1, 1)
        self.auditorium_flag = 1

        # добавление поля поиска групп
        self.group_search = QLineEdit()
        self.group_search.setPlaceholderText('Поиск по группам')
        self.group_search.textChanged.connect(self.text_change_group)
        self.layout.addWidget(self.group_search, 2, 0, 1, 1)

        # добавление поля поиска преподавателей
        self.teacher_search = QLineEdit()
        self.teacher_search.setPlaceholderText('Поиск по преподавателям')
        self.teacher_search.textChanged.connect(self.text_change_teacher)
        self.layout.addWidget(self.teacher_search, 2, 1, 1, 1)

        # добавление поля поиска аудиторий
        self.auditorium_search = QLineEdit()
        self.auditorium_search.setPlaceholderText('Поиск по аудиториям')
        self.auditorium_search.textChanged.connect(self.text_change_auditorium)
        self.layout.addWidget(self.auditorium_search, 2, 2, 1, 1)

        # добавление списка групп
        self.group_lst = QListWidget()
        self.group_lst.setSelectionMode(
            QAbstractItemView.SelectionMode.NoSelection
        )
        self.layout.addWidget(self.group_lst, 3, 0, 1, 1)

        # добавление списка преподавателей
        self.teacher_lst = QListWidget()
        self.teacher_lst.setSelectionMode(
            QAbstractItemView.SelectionMode.NoSelection
        )
        self.layout.addWidget(self.teacher_lst, 3, 1, 1, 1)

        # добавление списка аудиторий
        self.auditorium_lst = QListWidget()
        self.auditorium_lst.setSelectionMode(
            QAbstractItemView.SelectionMode.NoSelection
        )
        self.layout.addWidget(self.auditorium_lst, 3, 2, 1, 1)

        # добавление подтверждающей кнопки
        self.accept_btn = QPushButton('Применить')
        self.accept_btn.clicked.connect(self.button_click_accept)
        self.layout.addWidget(self.accept_btn, 4, 0, 1, 3)

        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

        # загрузка списка групп
        groups = load_group()
        for group in groups:
            item = QListWidgetItem(group.group)
            if group.selected:
                item.setCheckState(Qt.CheckState.Checked)
            else:
                item.setCheckState(Qt.CheckState.Unchecked)
            self.group_lst.addItem(item)
        self.group_items = [
            {'text': self.group_lst.item(x).text(),
             'selected': self.group_lst.item(x).checkState()}
            for x in range(self.group_lst.count())
        ]

        # загрузка списка преподавателей
        teachers = load_teacher()
        for teacher in teachers:
            if teacher.teacher == '':
                continue
            item = QListWidgetItem(teacher.teacher)
            if teacher.selected:
                item.setCheckState(Qt.CheckState.Checked)
            else:
                item.setCheckState(Qt.CheckState.Unchecked)
            self.teacher_lst.addItem(item)
        self.teacher_items = [
            {'text': self.teacher_lst.item(x).text(),
             'selected': self.teacher_lst.item(x).checkState()}
            for x in range(self.teacher_lst.count())
        ]

        # загрузка списка аудиторий
        auditoriums = load_auditorium()
        for auditorium in auditoriums:
            if auditorium.auditorium == '':
                continue
            item = QListWidgetItem(auditorium.auditorium)
            if auditorium.selected:
                item.setCheckState(Qt.CheckState.Checked)
            else:
                item.setCheckState(Qt.CheckState.Unchecked)
            self.auditorium_lst.addItem(item)
        self.auditorium_items = [
            {'text': self.auditorium_lst.item(x).text(),
             'selected': self.auditorium_lst.item(x).checkState()}
            for x in range(self.auditorium_lst.count())
        ]

    def button_click_selected_group(self):
        # выделение / снятие выделения списка групп
        items = [self.group_lst.item(x) for x in range(self.group_lst.count())]
        if self.group_flag:
            self.group_flag = 0
            for item in items:
                item.setCheckState(Qt.CheckState.Unchecked)
        else:
            self.group_flag = 1
            for item in items:
                item.setCheckState(Qt.CheckState.Checked)

    def button_click_selected_teacher(self):
        # выделение / снятие выделения списка преподавателей
        items = [self.teacher_lst.item(x)
                 for x in range(self.teacher_lst.count())]
        if self.teacher_flag:
            self.teacher_flag = 0
            for item in items:
                item.setCheckState(Qt.CheckState.Unchecked)
        else:
            self.teacher_flag = 1
            for item in items:
                item.setCheckState(Qt.CheckState.Checked)

    def button_click_selected_auditorium(self):
        # выделение / снятие выделения списка аудиторий
        items = [self.auditorium_lst.item(x)
                 for x in range(self.auditorium_lst.count())]
        if self.auditorium_flag:
            self.auditorium_flag = 0
            for item in items:
                item.setCheckState(Qt.CheckState.Unchecked)
        else:
            self.auditorium_flag = 1
            for item in items:
                item.setCheckState(Qt.CheckState.Checked)

    def button_click_accept(self):
        # получение выбранных состояний групп
        g_items = [self.group_lst.item(x)
                   for x in range(self.group_lst.count())]
        for x in self.group_items:
            for y in g_items:
                if x['text'] == y.text():
                    x['selected'] = y.checkState()

        # получение выбранных состояний преподавателей
        t_items = [self.teacher_lst.item(x)
                   for x in range(self.teacher_lst.count())]
        for x in self.teacher_items:
            for y in t_items:
                if x['text'] == y.text():
                    x['selected'] = y.checkState()

        # получение выбранных состояний аудиторий
        a_items = [self.auditorium_lst.item(x)
                   for x in range(self.auditorium_lst.count())]
        for x in self.auditorium_items:
            for y in a_items:
                if x['text'] == y.text():
                    x['selected'] = y.checkState()

        # преобразование списка групп для внесения в базу данных
        groups = []
        g_logging = []
        for item in self.group_items:
            i = QListWidgetItem(item['text'])
            i.setCheckState(item['selected'])
            groups.append(i)
            if item['selected'] == Qt.CheckState.Checked:
                g_logging.append(item['text'])
        if len(g_logging) == len(groups):
            g_logging.clear()
            g_logging.append('Выбраны все группы')

        # преобразование списка преподавателей для внесения в базу данных
        teachers = []
        t_logging = []
        for item in self.teacher_items:
            i = QListWidgetItem(item['text'])
            i.setCheckState(item['selected'])
            teachers.append(i)
            if item['selected'] == Qt.CheckState.Checked:
                t_logging.append(item['text'])
        if len(t_logging) == len(teachers):
            t_logging.clear()
            t_logging.append('Выбраны все преподаватели')

        # преобразование списка аудиторий для внесения в базу данных
        auditoriums = []
        a_logging = []
        for item in self.auditorium_items:
            i = QListWidgetItem(item['text'])
            i.setCheckState(item['selected'])
            auditoriums.append(i)
            if item['selected'] == Qt.CheckState.Checked:
                a_logging.append(item['text'])
        if len(a_logging) == len(auditoriums):
            a_logging.clear()
            a_logging.append('Выбраны все аудитории')

        # изменение в базе данных
        change_group(groups)
        change_teacher(teachers)
        change_auditorium(auditoriums)

        # обновление списков в основном окне программы
        self.main_form.update_lists()

        logging(datetime.now(), 'INFO_F', f'Обновление избранных: '
                                          f'группы {g_logging}; '
                                          f'преподаватели {t_logging}; '
                                          f'аудитории {a_logging}')

        self.close()

    def text_change_group(self):
        # сохранение текущих состояний групп
        g_items = [self.group_lst.item(x)
                   for x in range(self.group_lst.count())]
        for x in self.group_items:
            for y in g_items:
                if x['text'] == y.text():
                    x['selected'] = y.checkState()

        # очистка списка групп
        self.group_lst.clear()

        # заполнение списка групп с учётом фильтра
        for item in self.group_items:
            if self.group_search.text().lower() in item['text'].lower():
                i = QListWidgetItem(item['text'])
                i.setCheckState(item['selected'])
                self.group_lst.addItem(i)

    def text_change_teacher(self):
        # сохранение текущих состояний преподавателй
        t_items = [self.teacher_lst.item(x)
                   for x in range(self.teacher_lst.count())]
        for x in self.teacher_items:
            for y in t_items:
                if x['text'] == y.text():
                    x['selected'] = y.checkState()

        # очистка списка преподавателей
        self.teacher_lst.clear()

        # заполнение списка преподавателей с учётом фильтра
        for item in self.teacher_items:
            if self.teacher_search.text().lower() in item['text'].lower():
                i = QListWidgetItem(item['text'])
                i.setCheckState(item['selected'])
                self.teacher_lst.addItem(i)

    def text_change_auditorium(self):
        # сохранение текущих состояний аудиторий
        a_items = [self.auditorium_lst.item(x)
                   for x in range(self.auditorium_lst.count())]
        for x in self.auditorium_items:
            for y in a_items:
                if x['text'] == y.text():
                    x['selected'] = y.checkState()

        # очистка списка аудиторий
        self.auditorium_lst.clear()

        # заполнение списка аудиторий с учётом фильтра
        for item in self.auditorium_items:
            if self.auditorium_search.text().lower() in item['text'].lower():
                i = QListWidgetItem(item['text'])
                i.setCheckState(item['selected'])
                self.auditorium_lst.addItem(i)

    def closeEvent(self, event):
        logging(datetime.now(), 'WARNING', 'Закрытие формы выбора избранных '
                                           'групп, преподавателей и аудиторий')
