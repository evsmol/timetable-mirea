import datetime

from PyQt6.QtCore import Qt, QSize, QUrl
from PyQt6.QtWidgets import QMainWindow, QWidget, QAbstractItemView
from PyQt6.QtWidgets import QGridLayout, QToolBar, \
    QLabel, QListWidget, QListWidgetItem
from PyQt6.QtGui import QAction, QIcon, QDesktopServices, QColor

from forms import DateForm, FilterForm
# from forms import CheckForm

from config import VERSION

from data.update_time_func import get_time
from data.filter_func import load_group, load_teacher, load_auditorium

from mainform_func import fill_dates, get_pairs, fill_pairs

from calendar_func import set_now_month, set_previous_month, set_next_month

from logging_func import logging


class MainForm(QMainWindow):
    """Класс основного окна программы."""

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        logging(datetime.datetime.now(), 'WARNING', 'Открытие формы '
                                                    'основного окна программы')

        self.setWindowTitle(f'Учебное расписание РТУ МИРЭА (v{VERSION})')
        self.setWindowIcon(QIcon('image/icon.png'))

        # создание панели инструментов
        self.toolbar = QToolBar()
        self.toolbar.setIconSize(QSize(24, 24))
        self.toolbar.setMovable(False)
        self.addToolBar(self.toolbar)

        # добавление кнопки информации
        self.button_action_info = QAction(QIcon('image/info.png'),
                                          'Информация', self)
        self.button_action_info.triggered.connect(
            self.toolbar_button_click_info
        )
        self.toolbar.addAction(self.button_action_info)

        self.toolbar.addSeparator()

        # добавление кнопки загрузки расписания
        self.button_action_download = QAction(QIcon('image/download.png'),
                                              'Загрузить расписание', self)
        self.button_action_download.triggered.connect(
            self.toolbar_button_click_download
        )
        self.toolbar.addAction(self.button_action_download)

        self.toolbar.addSeparator()

        # добавление кнопки проверки загруженного расписания
        # self.button_action_check = QAction(
        #     QIcon('image/check.png'),
        #     'Проверить загруженное расписание',
        #     self
        # )
        # self.button_action_check.triggered.connect(
        #     self.toolbar_button_click_check
        # )
        # self.toolbar.addAction(self.button_action_check)
        #
        # self.toolbar.addSeparator()

        # добавление кнопки фильтра
        self.button_action_filter = QAction(
            QIcon('image/filter.png'),
            'Избранные группы и преподаватели',
            self
        )
        self.button_action_filter.triggered.connect(
            self.toolbar_button_click_filter
        )
        self.toolbar.addAction(self.button_action_filter)

        self.toolbar.addSeparator()

        # добавление кнопки предыдущего месяца
        self.button_action_left = QAction(QIcon('image/left.png'),
                                          'Предыдущий месяц', self)
        self.button_action_left.triggered.connect(
            self.toolbar_button_click_left
        )
        self.toolbar.addAction(self.button_action_left)

        # добавление кнопки текущего месяца
        self.button_action_now = QAction(QIcon('image/now.png'),
                                         'Текущий месяц', self)
        self.button_action_now.triggered.connect(
            self.toolbar_button_click_now
        )
        self.toolbar.addAction(self.button_action_now)

        # добавление кнопки следующего месяца
        self.button_action_right = QAction(QIcon('image/right.png'),
                                           'Следующий месяц', self)
        self.button_action_right.triggered.connect(
            self.toolbar_button_click_right
        )
        self.toolbar.addAction(self.button_action_right)

        self.toolbar.addSeparator()

        # добавление кнопки сообщения об ошибке
        self.button_action_report = QAction(QIcon('image/report.png'),
                                            'Сообщить об ошибке', self)
        self.button_action_report.triggered.connect(
            self.toolbar_button_click_report
        )
        self.toolbar.addAction(self.button_action_report)

        self.toolbar.addSeparator()

        # получение текста о времени загрузки расписания
        time = get_time()
        if time is None:
            time = '<i>загрузите расписание</i>'
        else:
            time = time[0]

        # добавление текста о последней загрузке расписания
        self.label_update = QLabel(f'Последняя загрузка расписания: {time}')
        self.label_update.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.toolbar.addWidget(self.label_update)

        # создание виджетов
        self.layout = QGridLayout()

        # добавление списка групп
        self.groups_list = QListWidget()
        self.groups_list.setSelectionMode(
            QAbstractItemView.SelectionMode.NoSelection
        )
        self.groups_list.itemChanged.connect(self.click_update)
        self.groups_list.itemDoubleClicked.connect(self.double_click)
        self.layout.addWidget(self.groups_list, 0, 0, 2, 1)

        # загрузка списка групп
        groups = load_group()
        for group in groups:
            if group.selected:
                item = QListWidgetItem(group.group)
                item.setCheckState(Qt.CheckState.Unchecked)
                self.groups_list.addItem(item)

        # добавление списка преподавателей
        self.teachers_list = QListWidget()
        self.teachers_list.setSelectionMode(
            QAbstractItemView.SelectionMode.NoSelection
        )
        self.teachers_list.itemChanged.connect(self.click_update)
        self.teachers_list.itemDoubleClicked.connect(self.double_click)
        self.layout.addWidget(self.teachers_list, 2, 0, 2, 1)

        # загрузка списка преподавателей
        teachers = load_teacher()
        for teacher in teachers:
            if teacher.teacher == '':
                continue
            if teacher.selected:
                item = QListWidgetItem(teacher.teacher)
                item.setCheckState(Qt.CheckState.Unchecked)
                self.teachers_list.addItem(item)

        # добавление списка аудиторий
        self.auditoriums_list = QListWidget()
        self.auditoriums_list.setSelectionMode(
            QAbstractItemView.SelectionMode.NoSelection
        )
        self.auditoriums_list.itemChanged.connect(self.click_update)
        self.auditoriums_list.itemDoubleClicked.connect(self.double_click)
        self.layout.addWidget(self.auditoriums_list, 4, 0, 1, 1)

        # загрузка списка аудиторий
        auditoriums = load_auditorium()
        for auditorium in auditoriums:
            if auditorium.auditorium == '':
                continue
            if auditorium.selected:
                item = QListWidgetItem(auditorium.auditorium)
                item.setCheckState(Qt.CheckState.Unchecked)
                self.auditoriums_list.addItem(item)

        # добавление списка параметров
        self.parameters_list = QListWidget()
        self.parameters_list.setSelectionMode(
            QAbstractItemView.SelectionMode.NoSelection
        )
        self.parameters_list.itemChanged.connect(self.click_update)
        self.parameters_list.itemDoubleClicked.connect(self.double_click)
        self.layout.addWidget(self.parameters_list, 5, 0, 1, 1)

        parameters = [
            'ФИО преподавателя',
            'Номер группы',
            'Номер аудитории',
            'Тип занятия',
            'Название дисциплины',
            'Объединить потоки'
        ]
        item = QListWidgetItem('Параметры:')
        item.setBackground(QColor('#4f4f4f'))
        self.parameters_list.addItem(item)
        for parameter in parameters:
            item = QListWidgetItem(parameter)
            item.setCheckState(Qt.CheckState.Checked)
            self.parameters_list.addItem(item)

        # фильтр
        # item = QListWidgetItem('Фильтр (нажмите трижды)')
        #
        # item.setIcon(QIcon('image/filters.png'))
        # item.setFont(QFont('Arial', 12, italic=True))
        # item.setFlags(Qt.ItemFlag.ItemIsEnabled |
        #               Qt.ItemFlag.ItemIsSelectable |
        #               Qt.ItemFlag.ItemIsEditable)
        # self.parameters_list.addItem(item)

        # добавление списков дней
        self.day_list = [QListWidget() for _ in range(36)]
        counter = 0
        for i in range(6):
            for j in range(1, 7):
                self.day_list[counter].setSelectionMode(
                    QAbstractItemView.SelectionMode.NoSelection
                )
                self.layout.addWidget(self.day_list[counter], i, j)
                counter += 1

        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

        # заполнение дат
        dates = set_now_month()
        fill_dates(self.day_list, dates)

        self.groups, self.teachers, self.auditoriums = [], [], []

    def update_dates(self):
        # заполнение дат
        dates = set_now_month()
        fill_dates(self.day_list, dates)

    def update_lists(self):
        # обновление списков

        self.groups_list.clear()
        # загрузка списка групп
        groups = load_group()
        for group in groups:
            if group.selected:
                item = QListWidgetItem(group.group)
                item.setCheckState(Qt.CheckState.Unchecked)
                self.groups_list.addItem(item)

        self.teachers_list.clear()
        # загрузка списка преподавателей
        teachers = load_teacher()
        for teacher in teachers:
            if teacher.teacher == '':
                continue
            if teacher.selected:
                item = QListWidgetItem(teacher.teacher)
                item.setCheckState(Qt.CheckState.Unchecked)
                self.teachers_list.addItem(item)

        self.auditoriums_list.clear()
        # загрузка списка аудиторий
        auditoriums = load_auditorium()
        for auditorium in auditoriums:
            if auditorium.auditorium == '':
                continue
            if auditorium.selected:
                item = QListWidgetItem(auditorium.auditorium)
                item.setCheckState(Qt.CheckState.Unchecked)
                self.auditoriums_list.addItem(item)

    def update_time_download(self):
        # обновление даты загрузки расписания
        time = get_time()
        if time is None:
            time = '<i>расписание не загружалось</i>'
        else:
            time = time[0]
        self.label_update.setText(f'Последняя загрузка расписания: {time}')

    def toolbar_button_click_info(self):
        logging(datetime.datetime.now(), 'WARNING',
                'Переход на страницу релизов')

        # переход на страницу релизов программы
        url = 'https://github.com/evsmol/timetable/releases'
        QDesktopServices.openUrl(QUrl(url))

    def toolbar_button_click_download(self):
        # открытие формы загрузки расписания
        self.date_form = DateForm.DateForm(self)
        self.date_form.show()

    # def toolbar_button_click_check(self):
    # # открытие формы проверки расписания
    #     self.check_form = CheckForm.CheckForm(self)
    #     self.check_form.show()

    def toolbar_button_click_filter(self):
        # открытие формы выбора избранных
        self.filter_form = FilterForm.FilterForm(self)
        self.filter_form.show()

    def toolbar_button_click_left(self):
        logging(datetime.datetime.now(), 'INFO', 'Выбор предыдущего месяца')

        # получение даты текущего месяца
        date = self.day_list[6].item(0).text()

        # очистка дат
        for lst in self.day_list:
            lst.clear()

        # заполнение дат
        dates = set_previous_month(date)
        fill_dates(self.day_list, dates)
        fill_pairs(self.groups, self.teachers, self.auditoriums,
                   self.day_list, self.parameters_list)

    def toolbar_button_click_now(self):
        logging(datetime.datetime.now(), 'INFO', 'Выбор текущего месяца')

        # заполнение дат
        dates = set_now_month()
        fill_dates(self.day_list, dates)
        fill_pairs(self.groups, self.teachers, self.auditoriums,
                   self.day_list, self.parameters_list)

    def toolbar_button_click_right(self):
        logging(datetime.datetime.now(), 'INFO', 'Выбор следующего месяца')

        # получение даты текущего месяца
        date = self.day_list[6].item(0).text()

        # очистка дат
        for lst in self.day_list:
            lst.clear()

        # заполнение дат
        dates = set_next_month(date)
        fill_dates(self.day_list, dates)
        fill_pairs(self.groups, self.teachers, self.auditoriums,
                   self.day_list, self.parameters_list)

    def toolbar_button_click_report(self):
        logging(datetime.datetime.now(), 'WARNING',
                'Открытие письма сообщения об ошибке')

        # переход к стандартному почтовому клиенту, встраивание шаблона письма
        url = f'mailto:smolentsev@kb9-mirea.ru' \
              f'?subject=Ошибка в приложении Учебное расписание РТУ МИРЭА ' \
              f'(v{VERSION}) {datetime.datetime.now()}' \
              f'&body=Подробно опишите ошибку, приложите скриншоты:'
        QDesktopServices.openUrl(QUrl(url))

    def click_update(self):
        # обновление выбираемых данных

        # очистка дат
        for lst in self.day_list:
            lst.clear()

        # заполнение дат
        dates = set_now_month()
        fill_dates(self.day_list, dates)

        # получение выбранных групп
        group_items = [self.groups_list.item(x)
                       for x in range(self.groups_list.count())]
        group_lst = []
        for item in group_items:
            if item.checkState() == Qt.CheckState.Checked:
                group_lst.append(item.text())

        # получение выбранных преподавателей
        teacher_items = [self.teachers_list.item(x)
                         for x in range(self.teachers_list.count())]
        teacher_lst = []
        for item in teacher_items:
            if item.text() == '':
                continue
            if item.checkState() == Qt.CheckState.Checked:
                teacher_lst.append(item.text())

        # получение выбранных аудиторий
        auditorium_items = [self.auditoriums_list.item(x)
                            for x in range(self.auditoriums_list.count())]
        auditorium_lst = []
        for item in auditorium_items:
            if item.text() == '':
                continue
            if item.checkState() == Qt.CheckState.Checked:
                auditorium_lst.append(item.text())

        # заполнение пар
        self.groups, self.teachers, self.auditoriums = \
            get_pairs(group_lst, teacher_lst, auditorium_lst)
        fill_pairs(self.groups, self.teachers, self.auditoriums,
                   self.day_list, self.parameters_list)

        p_logging = []
        for x in range(1, self.parameters_list.count()):
            if str(
                    self.parameters_list.item(x).checkState()
            ).split('.')[1][:2] == 'Ch':
                p_logging.append(self.parameters_list.item(x).text())
        if len(p_logging) == 6:
            p_logging.clear()
            p_logging.append('Выбраны все параметры')
        logging(datetime.datetime.now(), 'INFO_F',
                f'Выбор отображения: группы {group_lst}; '
                f'преподаватели {teacher_lst}; аудитории {auditorium_lst}; '
                f'параметры {p_logging}')

    def double_click(self, item):
        # изменение состояние на противоположное
        if item.text() == 'Параметры:':
            pass
        elif item.checkState() == Qt.CheckState.Checked:
            item.setCheckState(Qt.CheckState.Unchecked)
        elif item.checkState() == Qt.CheckState.Unchecked:
            item.setCheckState(Qt.CheckState.Checked)

    def closeEvent(self, event):
        logging(datetime.datetime.now(), 'WARNING', 'Закрытие формы '
                                                    'основного окна программы')
