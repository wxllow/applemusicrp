@echo off

poetry install

cd src\applemusicrp

mkdir dist
mkdir dist\windows

python setup-win.py py2exe
