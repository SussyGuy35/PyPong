title lmao

pyinstaller --noconfirm --onefile --windowed --icon "data/icon.ico" --splash "splash.png" --add-data "data;data/" --hidden-import "pyi_splash"  "pong.py"