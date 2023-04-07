#!/bin/sh

cd ~/Desktop || exit
try git clone https://github.com/evsmol/timetable.git

if [ '1' = $(python3 --version) ]; then
  exit
else
  xcode-select --install
  /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
  brew install python3
fi

cd timetable || exit
python3 -m pip install --user --upgrade pip
python3 -m pip install requests

python3 app.py