# Path: gui/themes/dark_theme.py

def get_dark_theme():
    return """
    QMainWindow {
        background-color: #0b0e14;
    }
    QWidget {
        background-color: #0b0e14;
        color: #e0e0e0;
        font-family: 'Segoe UI', sans-serif;
        font-size: 13px;
    }
    QFrame#Panel {
        background-color: #0f172a;
        border: 1px solid #1e293b;
        border-radius: 8px;
    }
    QLabel#Header {
        color: #bb86fc;
        font-size: 18px;
        font-weight: bold;
    }
    QLabel#SubHeader {
        color: #bb86fc;
        font-size: 14px;
        font-weight: bold;
    }
    QLineEdit {
        background-color: #1e293b;
        border: 1px solid #334155;
        border-radius: 4px;
        padding: 8px;
        color: #ffffff;
    }
    QLineEdit:focus {
        border: 1px solid #bb86fc;
    }
    QPushButton {
        background-color: #1f2937;
        border: none;
        border-radius: 4px;
        padding: 8px 16px;
        color: #ffffff;
        font-weight: bold;
    }
    QPushButton:hover {
        background-color: #374151;
    }
    QPushButton#ActionButton {
        background-color: #bb86fc;
        color: #000000;
    }
    QPushButton#ActionButton:hover {
        background-color: #d7b7fd;
    }
    QComboBox {
        background-color: #1e293b;
        border: 1px solid #334155;
        border-radius: 4px;
        padding: 5px;
        color: #ffffff;
    }
    QComboBox::drop-down {
        border: none;
    }
    QTextEdit {
        background-color: #0f172a;
        border: none;
        color: #f1f5f9;
        font-family: 'Segoe UI', sans-serif;
        font-size: 14px;
    }
    QScrollBar:vertical {
        border: none;
        background: #0b0e14;
        width: 10px;
        margin: 0px;
    }
    QScrollBar::handle:vertical {
        background: #334155;
        min-height: 20px;
        border-radius: 5px;
    }
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
        height: 0px;
    }
    QCheckBox {
        spacing: 8px;
    }
    QCheckBox::indicator {
        width: 18px;
        height: 18px;
        background-color: #1e293b;
        border: 1px solid #334155;
        border-radius: 4px;
    }
    QCheckBox::indicator:checked {
        background-color: #bb86fc;
    }
    """
