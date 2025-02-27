import sys
import asyncio
import itertools
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtCore import QThread, pyqtSignal
from kahoot import KahootClient
from colorama import Fore, init

init(autoreset=True)

def logo():
    print(f"""{Fore.MAGENTA}
       ==----------     ---------:      
       =-:-:::::--:     -::::::--:      
       --:+     -::     -:     =-:      
      +=-:=     -::     ::     =-:=     
      ::::::::::::::::::::     =-:+     
      ::                       =-:=     
      ::                       =-:=     
      ::--=====================--:---   
       --:-                       -::   
       =-:+                       -::   
       =-:+                       -:-   
       =-:+     -::-----------::::::-   
       =-:+     -::     ::     =-:=     
       =-:+     -::     ::     =-:=     
       =-:+     -:-     ::     =-:      
       =-:+     -::     ::     --:      
       =-:=++===-:-     ::-====--:      
       --::::::::::     ::::::::::    {Fore.LIGHTMAGENTA_EX}
       https://github.com/H-zz-H69
              Made by H-zz-H  
    """)

class BotRunner(QThread):
    update_signal = pyqtSignal(str)

    def __init__(self, game_pin, base_username, count):
        super().__init__()
        self.game_pin = game_pin
        self.base_username = base_username
        self.count = count

    async def join_game(self, game_pin, username):
        client = KahootClient()
        try:
            await client.join_game(game_pin, username)
            self.update_signal.emit(f"Successfully joined game as {username}")
        except Exception as e:
            self.update_signal.emit(f"Error joining game as {username}: {e}")

    async def run_bots(self):
        tasks = [self.join_game(self.game_pin, f"{self.base_username}_{i+1}") for i in range(self.count)]
        await asyncio.gather(*tasks)

    def run(self):
        asyncio.run(self.run_bots())

class KahootBotGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("Made by H-zz-H | github.com/H-zz-H69")
        self.setGeometry(100, 100, 400, 300)
        
        layout = QVBoxLayout()
        
        self.label_pin = QLabel("Game PIN:")
        self.entry_pin = QLineEdit()
        
        self.label_username = QLabel("Base Username:")
        self.entry_username = QLineEdit()
        
        self.label_count = QLabel("Bot Count:")
        self.entry_count = QLineEdit()
        
        self.button_start = QPushButton("Start Bots")
        self.button_start.clicked.connect(self.start_bots)
        
        self.output_label = QLabel("Status: Waiting for input...")
        
        layout.addWidget(self.label_pin)
        layout.addWidget(self.entry_pin)
        layout.addWidget(self.label_username)
        layout.addWidget(self.entry_username)
        layout.addWidget(self.label_count)
        layout.addWidget(self.entry_count)
        layout.addWidget(self.button_start)
        layout.addWidget(self.output_label)
        
        self.setLayout(layout)
        self.apply_styles()
    
    def apply_styles(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #121212;
                color: #FFFFFF;
                font-size: 14px;
            }
            QLineEdit {
                background-color: #333333;
                border: 1px solid #555555;
                padding: 5px;
                border-radius: 5px;
                color: white;
            }
            QPushButton {
                background-color: #6200EE;
                color: white;
                border-radius: 5px;
                padding: 7px;
            }
            QPushButton:hover {
                background-color: #3700B3;
            }
            QLabel {
                font-weight: bold;
            }
        """)
    
    def start_bots(self):
        game_pin = self.entry_pin.text()
        base_username = self.entry_username.text()
        try:
            bot_count = int(self.entry_count.text())
            if bot_count <= 0:
                raise ValueError
        except ValueError:
            QMessageBox.critical(self, "Error", "Bot count must be a positive number.")
            return
        
        self.output_label.setText("Running bots...")
        self.bot_runner = BotRunner(game_pin, base_username, bot_count)
        self.bot_runner.update_signal.connect(self.output_label.setText)
        self.bot_runner.start()

if __name__ == "__main__":
    logo()
    app = QApplication(sys.argv)
    gui = KahootBotGUI()
    gui.show()
    sys.exit(app.exec_())
