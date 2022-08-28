"%USERPROFILE%\AppData\Local\Programs\Python\Python310\Scripts\pyinstaller.exe" ^
 ^
--add-data "data/icon.jpg;." ^
--add-data "data/theme.json;." ^
--add-data "data/FreeSansBold.ttf;." ^
 ^
--name "Snake" ^
--icon "data/icon.ico" ^
--noconfirm ^
--windowed ^
--onefile ^
--clean ^
./scripts/main.py

rmdir /s /q "./build"
del "./Snake.spec"