from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QMainWindow
from PyQt6.QtWidgets import QGridLayout, QLabel, QPushButton, \
    QListWidget, QListWidgetItem
from PyQt6.QtGui import QIcon

from data.filter_func import load_teacher, load_group, \
    change_teacher, change_group


class FilterForm(QMainWindow):
    """Класс окна выбора избранных групп и преподавателей."""

    def __init__(self, MainForm):
        super().__init__()
        self.main_form = MainForm
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Избранные группы и преподаватели')
        self.setWindowIcon(QIcon('image/filter.png'))

        # создание виджетов
        self.layout = QGridLayout()

        self.label_info = QLabel('Выберите группы и преподавателей '
                                 'для отображения в главном окне программы.')
        self.layout.addWidget(self.label_info, 0, 0, 1, 2)

        self.label_space = QLabel(' ')
        self.layout.addWidget(self.label_space, 1, 0, 1, 2)

        self.group_btn = QPushButton('Выделить / снять выделение')
        self.group_btn.clicked.connect(self.button_click_selected_group)
        self.layout.addWidget(self.group_btn, 2, 0, 1, 1)
        self.group_flag = 1

        self.teacher_btn = QPushButton('Выделить / снять выделение')
        self.teacher_btn.clicked.connect(self.button_click_selected_teacher)
        self.layout.addWidget(self.teacher_btn, 2, 1, 1, 1)
        self.teacher_flag = 1

        self.group_lst = QListWidget()
        self.layout.addWidget(self.group_lst, 3, 0, 1, 1)

        self.teacher_lst = QListWidget()
        self.layout.addWidget(self.teacher_lst, 3, 1, 1, 1)

        self.accept_btn = QPushButton('Применить')
        self.accept_btn.clicked.connect(self.button_click_accept)
        self.layout.addWidget(self.accept_btn, 4, 0, 1, 2)

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

        # загрузка списка преподавателей
        teachers = load_teacher()
        for teacher in teachers:
            item = QListWidgetItem(teacher.teacher)
            if teacher.selected:
                item.setCheckState(Qt.CheckState.Checked)
            else:
                item.setCheckState(Qt.CheckState.Unchecked)
            self.teacher_lst.addItem(item)

    def button_click_selected_group(self):
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

    def button_click_accept(self):
        group_items = [self.group_lst.item(x)
                       for x in range(self.group_lst.count())]
        teacher_items = [self.teacher_lst.item(x)
                         for x in range(self.teacher_lst.count())]

        change_group(group_items)
        change_teacher(teacher_items)

        self.main_form.update_lists()

        self.close()
