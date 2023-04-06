import datetime

from PyQt6.QtCore import Qt, QSize, QUrl
from PyQt6.QtWidgets import QMainWindow, QWidget
from PyQt6.QtWidgets import QGridLayout, QToolBar, \
    QLabel, QPushButton, QListWidget, QListWidgetItem
from PyQt6.QtGui import QAction, QIcon, QDesktopServices, QColor

from forms import DateForm, FilterForm
# from forms import CheckForm

from config import VERSION

from data.update_time_func import get_time
from data.filter_func import load_group, load_teacher

from mainform_func import fill_dates, get_pairs, fill_pairs

from calendar_func import set_now_month, set_previous_month, set_next_month


class MainForm(QMainWindow):
    """Класс основного окна программы."""

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle(f'Учебное расписание РТУ МИРЭА (v{VERSION})')
        self.setWindowIcon(QIcon('image/icon.png'))

        # создание панели инструментов
        self.toolbar = QToolBar()
        self.toolbar.setIconSize(QSize(24, 24))
        self.toolbar.setMovable(False)
        self.addToolBar(self.toolbar)

        self.button_action_info = QAction(QIcon('image/info.png'),
                                          'Информация', self)
        self.button_action_info.triggered.connect(
            self.toolbar_button_click_info
        )
        self.toolbar.addAction(self.button_action_info)

        self.toolbar.addSeparator()

        self.button_action_download = QAction(QIcon('image/download.png'),
                                              'Загрузить расписание', self)
        self.button_action_download.triggered.connect(
            self.toolbar_button_click_download
        )
        self.toolbar.addAction(self.button_action_download)

        self.toolbar.addSeparator()

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

        self.button_action_left = QAction(QIcon('image/left.png'),
                                          'Предыдущий месяц', self)
        self.button_action_left.triggered.connect(
            self.toolbar_button_click_left
        )
        self.toolbar.addAction(self.button_action_left)

        self.button_action_now = QAction(QIcon('image/now.png'),
                                         'Текущий месяц', self)
        self.button_action_now.triggered.connect(
            self.toolbar_button_click_now
        )
        self.toolbar.addAction(self.button_action_now)

        self.button_action_right = QAction(QIcon('image/right.png'),
                                           'Следующий месяц', self)
        self.button_action_right.triggered.connect(
            self.toolbar_button_click_right
        )
        self.toolbar.addAction(self.button_action_right)

        self.toolbar.addSeparator()

        self.button_action_report = QAction(QIcon('image/report.png'),
                                            'Сообщить об ошибке', self)
        self.button_action_report.triggered.connect(
            self.toolbar_button_click_report
        )
        self.toolbar.addAction(self.button_action_report)

        # создание виджетов
        self.layout = QGridLayout()

        self.groups_list = QListWidget()
        self.layout.addWidget(self.groups_list, 0, 0, 2, 1)

        # загрузка списка групп
        groups = load_group()
        for group in groups:
            if group.selected:
                item = QListWidgetItem(group.group)
                item.setCheckState(Qt.CheckState.Unchecked)
                self.groups_list.addItem(item)

        self.teachers_list = QListWidget()
        self.layout.addWidget(self.teachers_list, 2, 0, 2, 1)

        # загрузка списка преподавателей
        teachers = load_teacher()
        for teacher in teachers:
            if teacher.selected:
                item = QListWidgetItem(teacher.teacher)
                item.setCheckState(Qt.CheckState.Unchecked)
                self.teachers_list.addItem(item)

        self.parameters_list = QListWidget()
        self.layout.addWidget(self.parameters_list, 4, 0, 2, 1)

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

        self.accept_btn = QPushButton('Применить')
        self.accept_btn.clicked.connect(self.button_click_accept)
        self.layout.addWidget(self.accept_btn, 6, 0, 1, 1)

        time = get_time()
        if time is None:
            time = '<i>расписание не загружалось</i>'
        else:
            time = time[0]
        self.label_update = QLabel(f'Последняя загрузка расписания: {time}')
        self.label_update.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.label_update, 6, 1, 1, 6)

        self.day_list = [QListWidget() for _ in range(36)]
        counter = 0
        for i in range(6):
            for j in range(1, 7):
                self.layout.addWidget(self.day_list[counter], i, j)
                counter += 1

        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

        # заполнение дат
        dates = set_now_month()
        fill_dates(self.day_list, dates)

    def update_dates(self):
        dates = set_now_month()
        fill_dates(self.day_list, dates)

    def update_lists(self):
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
            if teacher.selected:
                item = QListWidgetItem(teacher.teacher)
                item.setCheckState(Qt.CheckState.Unchecked)
                self.teachers_list.addItem(item)

    def update_time_download(self):
        time = get_time()
        if time is None:
            time = '<i>расписание не загружалось</i>'
        else:
            time = time[0]
        self.label_update.setText(f'Последняя загрузка расписания: {time}')

    def toolbar_button_click_info(self):
        pass

    def toolbar_button_click_download(self):
        self.date_form = DateForm.DateForm(self)
        self.date_form.show()

    # def toolbar_button_click_check(self):
    #     self.check_form = CheckForm.CheckForm(self)
    #     self.check_form.show()

    def toolbar_button_click_filter(self):
        self.filter_form = FilterForm.FilterForm(self)
        self.filter_form.show()

    def toolbar_button_click_left(self):
        date = self.day_list[6].item(0).text()
        for lst in self.day_list:
            lst.clear()

        # заполнение дат
        dates = set_previous_month(date)
        fill_dates(self.day_list, dates)

        fill_pairs(self.groups, self.teachers, self.day_list,
                   self.parameters_list)

    def toolbar_button_click_now(self):
        # заполнение дат
        dates = set_now_month()
        fill_dates(self.day_list, dates)

        fill_pairs(self.groups, self.teachers, self.day_list,
                   self.parameters_list)

    def toolbar_button_click_right(self):
        date = self.day_list[6].item(0).text()
        for lst in self.day_list:
            lst.clear()

        # заполнение дат
        dates = set_next_month(date)
        fill_dates(self.day_list, dates)

        fill_pairs(self.groups, self.teachers, self.day_list,
                   self.parameters_list)

    def toolbar_button_click_report(self):
        url = f'mailto:smolentsev@kb9-mirea.ru' \
              f'?subject=Ошибка в приложении Учебное расписание РТУ МИРЭА ' \
              f'(v{VERSION}) {datetime.datetime.now()}' \
              f'&body=Подробно опишите ошибку, приложите скриншоты:'
        QDesktopServices.openUrl(QUrl(url))

    def button_click_accept(self):
        for lst in self.day_list:
            lst.clear()

        # заполнение дат
        dates = set_now_month()
        fill_dates(self.day_list, dates)

        group_items = [self.groups_list.item(x)
                       for x in range(self.groups_list.count())]
        group_lst = []
        for item in group_items:
            if item.checkState() == Qt.CheckState.Checked:
                group_lst.append(item.text())

        teacher_items = [self.teachers_list.item(x)
                         for x in range(self.teachers_list.count())]
        teacher_lst = []
        for item in teacher_items:
            if item.checkState() == Qt.CheckState.Checked:
                teacher_lst.append(item.text())

        self.groups, self.teachers = get_pairs(group_lst, teacher_lst)
        fill_pairs(self.groups, self.teachers, self.day_list,
                   self.parameters_list)
