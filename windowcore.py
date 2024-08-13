import sys
import random
import string
import os
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QShortcut
from PyQt5.QtGui import QKeySequence, QColor, QPalette
import pygame

class RandomWindow(QWidget):
    def __init__(self, screen_width, screen_height, app):
        super().__init__()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.app = app  # Reference to the main application instance
        self.initUI()

        # Initial direction and speed
        self.dx = random.choice([-5, 5])
        self.dy = random.choice([-5, 5])

        # Timer for moving the window
        self.move_timer = QTimer(self)
        self.move_timer.timeout.connect(self.move_window)
        self.move_timer.start(50)  # Update every 50 ms for smooth movement

        # Timer for flashing background colors
        self.color_timer = QTimer(self)
        self.color_timer.timeout.connect(self.flash_background)
        self.color_timer.start(100)  # Change color every 100 ms

        # List of rainbow colors
        self.rainbow_colors = [
            QColor(148, 0, 211),  # Violet
            QColor(75, 0, 130),  # Indigo
            QColor(0, 0, 255),  # Blue
            QColor(0, 255, 0),  # Green
            QColor(255, 255, 0),  # Yellow
            QColor(255, 127, 0),  # Orange
            QColor(255, 0, 0)  # Red
        ]
        self.current_color_index = 0

        # Add Esc shortcut
        self.esc_shortcut = QShortcut(QKeySequence("Esc"), self)
        self.esc_shortcut.activated.connect(self.terminate_all)

    def initUI(self):
        # Random title text
        title = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10))
        self.setWindowTitle(title)

        # Random body text
        body_text = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(20))
        label = QLabel(body_text, self)
        label.setAlignment(Qt.AlignCenter)

        # Random window size
        width = random.randint(100, 200)
        height = random.randint(100, 200)
        self.resize(width, height)

        # Window layout
        layout = QVBoxLayout()
        layout.addWidget(label)
        self.setLayout(layout)

        # Start at a random position
        x = random.randint(0, self.screen_width - self.width())
        y = random.randint(0, self.screen_height - self.height())
        self.move(x, y)

    def move_window(self):
        current_x = self.x()
        current_y = self.y()

        # Calculate new position
        new_x = current_x + self.dx
        new_y = current_y + self.dy

        # Bounce off the sides
        if new_x <= 0 or new_x + self.width() >= self.screen_width:
            self.dx = -self.dx
        if new_y <= 0 or new_y + self.height() >= self.screen_height:
            self.dy = -self.dy

        # Move window to the new position
        self.move(current_x + self.dx, current_y + self.dy)
        self.raise_()  # Bring window to the foreground

    def flash_background(self):
        # Set the background color
        palette = self.palette()
        palette.setColor(QPalette.Background, self.rainbow_colors[self.current_color_index])
        self.setPalette(palette)

        # Update to the next color
        self.current_color_index = (self.current_color_index + 1) % len(self.rainbow_colors)

    def terminate_all(self):
        self.app.terminate_app()  # Call the terminate method of the main application

# Main application
class App(QApplication):
    def __init__(self, sys_argv):
        super().__init__(sys_argv)
        self.windows = []
        self.timer = QTimer()
        self.timer.timeout.connect(self.create_random_window)

        # Get the screen geometry
        screen_geometry = QApplication.primaryScreen().availableGeometry()
        self.screen_width = screen_geometry.width()
        self.screen_height = screen_geometry.height()

        # Initialize pygame and start playing the mp3 file
        pygame.init()
        self.music = pygame.mixer.music
        script_dir = os.path.dirname(os.path.abspath(__file__))
        mp3_path = os.path.join(script_dir, "windowcore.mp3")
        self.music.load(mp3_path)
        self.music.play(-1)  # Loop indefinitely

        self.start_random_timer()

        # Create a hidden main window to manage the shortcut
        self.main_window = QWidget()
        self.shortcut = QShortcut(QKeySequence("Ctrl+E"), self.main_window)
        self.shortcut.activated.connect(self.terminate_app)

    def start_random_timer(self):
        interval = int(random.uniform(10, 100))  # interval in milliseconds (0.01 to 0.1 seconds)
        self.timer.start(interval)

    def create_random_window(self):
        window = RandomWindow(self.screen_width, self.screen_height, self)
        window.show()
        self.windows.append(window)
        self.start_random_timer()  # Restart the timer for the next window

    def terminate_app(self):
        for window in self.windows:
            window.close()
        self.music.stop()  # Stop the music
        self.quit()

if __name__ == '__main__':
    app = App(sys.argv)
    sys.exit(app.exec_())
