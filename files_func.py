from bs4 import BeautifulSoup
import requests
import os

from urllib import request
import ssl

from data.schedule_func import add_pairs

from converter import get_timetable


def get_files(url):
    page = requests.get(url)

    soup = BeautifulSoup(page.text, "html.parser")
    blocks = soup.findAll(True, {"class": [
        "uk-card", "slider_ads", "uk-card-body", "uk-card-small"
    ]})

    files = []
    for block in blocks:
        soup_inst = BeautifulSoup(str(block), "html.parser")
        inst = soup_inst.find_all("a", {"class": "uk-text-bold"})
        if len(inst) > 0:
            if inst[0].text == 'Институт кибербезопасности и цифровых ' \
                               'технологий':
                for link in soup_inst.find_all('a', href=True):
                    if "javascript:void(0)" not in link['href']:
                        url = link['href']
                        if "pdf" not in link['href'] and \
                                "zach" not in link['href'] and \
                                'ekz' not in link['href']:
                            files.append(url)
    return files


def load_file(file, filename):
    r = requests.head(file)
    if r.status_code == 200:
        request.urlretrieve(file, filename)


def load_files(files):
    filenames = list()
    ssl._create_default_https_context = ssl._create_unverified_context
    for file in files:
        load_file(file, f'files/{file.split("/")[-1]}')
        filenames.append(f'files/{file.split("/")[-1]}')
    return filenames


def update_db():
    for file in load_files(get_files('https://www.mirea.ru/schedule/')):
        add_pairs(get_timetable(file))
        if os.path.isfile(file):
            os.remove(file)