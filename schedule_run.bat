@echo off

call %~dp0schedule_bot\venv\Scripts\activate

cd %~dp0schedule_bot

set TOKEN=5181037643:AAFyv3QXAV2FO4xiGovmM_JTd3MDV23UpBk

python schedule_bot.py

pause