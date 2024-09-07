import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, QSize
from pynput import keyboard
from PIL import Image

# Global variables
win_key_disabled = False
listener = None

class WinKeyToggleApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.register_hotkey()

    def initUI(self):
        """Initialize the user interface."""
        self.setWindowTitle('WinKey Disabler')
        self.setWindowIcon(QIcon("resources/enabled.ico"))
        self.layout = QVBoxLayout()

        # Set initial image and labels
        self.current_image = "enabled.png"
        self.instruction_label = QLabel('Click the Windows Image or', self)
        self.instruction_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.instruction_label)

        self.status_label = QLabel('WIN + Backspace to DISABLE WinKey', self)
        self.status_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.status_label)

        # Create a button with image icon
        self.toggle_button = QPushButton(self)
        self.update_button_icon()
        self.toggle_button.setFixedSize(128, 128)  # Set button size to 128x128
        self.toggle_button.clicked.connect(self.toggle_win_key)
        self.layout.addWidget(self.toggle_button, alignment=Qt.AlignCenter)

        self.setLayout(self.layout)
        self.setGeometry(300, 300, 350, 200)
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowTitleHint)  # Remove maximize button
        self.setFixedSize(350, 200)  # Make window non-resizable

    def update_button_icon(self):
        """Update the button icon based on the current state of the Windows key."""
        img_name = "disabled.png" if win_key_disabled else "enabled.png"
        img_path = os.path.join("resources", img_name)
        pixmap = QPixmap(img_path)
        self.toggle_button.setIcon(QIcon(pixmap))
        self.toggle_button.setIconSize(QSize(128, 128))  # Set icon size to match button size

    def update_status_label(self):
        """Update the status label to reflect the current state."""
        if win_key_disabled:
            self.status_label.setText('WIN + Backspace to ENABLE WinKey')
        else:
            self.status_label.setText('WIN + Backspace to DISABLE WinKey')

    def toggle_win_key(self):
        """Toggle the Windows key and update the button icon and status label."""
        global win_key_disabled
        if win_key_disabled:
            self.unhook_win_key()
            win_key_disabled = False
        else:
            self.block_win_key()
            win_key_disabled = True
        self.update_button_icon()  # Update button icon based on the new state
        self.update_status_label()  # Update status label based on the new state

    def register_hotkey(self):
        """Register the hotkey for WIN + Backspace using keyboard library."""
        import keyboard
        keyboard.add_hotkey('win+backspace', self.toggle_win_key)

    def block_win_key(self):
        """Block the Windows key using pynput."""
        global listener
        def on_press(key):
            if key == keyboard.Key.cmd:
                return False  # Block the Windows key
        listener = keyboard.Listener(on_press=on_press)
        listener.start()

    def unhook_win_key(self):
        """Unhook the Windows key."""
        global listener
        if listener:
            listener.stop()
            listener = None

def load_icon(icon_name):
    """Load an icon image from the 'resources' directory."""
    icon_path = os.path.join("resources", icon_name)
    if os.path.exists(icon_path):
        return Image.open(icon_path)
    else:
        raise FileNotFoundError(f"Icon file {icon_name} not found in 'resources' directory.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app_window = WinKeyToggleApp()
    app_window.show()
    sys.exit(app.exec_())
