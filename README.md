source venv/bin/activate
pyinstaller --onefile --windowed --name tictactoe --add-data "assets:assets"  main.py
