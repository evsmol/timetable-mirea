import os

from data import db_session
from data.schedule_func import add_pairs

from converter import get_timetable
from get_files import get_files, load_files

db_session.global_init('db/timetable.db')

for file in load_files(get_files('https://www.mirea.ru/schedule/')):
    add_pairs(get_timetable(file))

    if os.path.isfile(file):
        os.remove(file)