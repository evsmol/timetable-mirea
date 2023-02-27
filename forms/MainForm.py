from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import QMainWindow, QWidget
from PyQt6.QtWidgets import QGridLayout, QStatusBar, QToolBar, \
    QLabel, QPushButton, QListWidget, QListWidgetItem
from PyQt6.QtGui import QAction, QIcon

from config import VERSION

from data.update_time_func import get_time


class MainForm(QMainWindow):
    """Класс основного окна программы."""

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle(f'Учебное расписание РТУ МИРЭА (v{VERSION})')

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

        self.teachers_list = QListWidget()
        self.layout.addWidget(self.teachers_list, 2, 0, 2, 1)

        self.parameters_list = QListWidget()
        self.layout.addWidget(self.parameters_list, 4, 0, 2, 1)

        self.accept_btn = QPushButton('Применить')
        self.layout.addWidget(self.accept_btn, 6, 0, 1, 1)

        time = get_time()
        if time is None:
            time = '<i>расписание не загружалось</i>'
        self.label_update = QLabel(f'Последнее обновление расписания: {time}')
        self.label_update.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.label_update, 6, 1, 1, 6)

        day_list = [QListWidget() for _ in range(36)]
        counter = 0
        for i in range(6):
            for j in range(1, 7):
                self.layout.addWidget(day_list[counter], i, j)
                counter += 1

        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

    def toolbar_button_click_info(self):
        pass

    def toolbar_button_click_download(self):
        pass

    def toolbar_button_click_filter(self):
        pass

    def toolbar_button_click_left(self):
        pass

    def toolbar_button_click_right(self):
        pass

    def toolbar_button_click_report(self):
        pass
