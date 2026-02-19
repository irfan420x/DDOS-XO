# Path: gui/themes/manus_theme.py

MANUS_STYLE = """
QMainWindow {
    background-color: #0F0F12;
    color: #E0E0E6;
}

QWidget {
    font-family: 'Segoe UI', 'Roboto', sans-serif;
    font-size: 13px;
}

/* Sidebar Styling */
QFrame#Sidebar {
    background-color: #16161D;
    border-right: 1px solid #2A2A35;
}

/* Main Content Area */
QFrame#MainContent {
    background-color: #0F0F12;
}

/* Panels & Cards */
QFrame#Panel {
    background-color: #1C1C26;
    border: 1px solid #2A2A35;
    border-radius: 12px;
}

QFrame#Panel:hover {
    border: 1px solid #3D3D4D;
}

/* Buttons */
QPushButton {
    background-color: #2A2A35;
    color: #E0E0E6;
    border: 1px solid #3D3D4D;
    border-radius: 8px;
    padding: 8px 16px;
    font-weight: 600;
}

QPushButton:hover {
    background-color: #3D3D4D;
    border: 1px solid #4D4D5D;
}

QPushButton#PrimaryButton {
    background-color: #4F46E5;
    color: white;
    border: none;
}

QPushButton#PrimaryButton:hover {
    background-color: #6366F1;
}

QPushButton#DangerButton {
    background-color: #DC2626;
    color: white;
    border: none;
}

/* Inputs */
QLineEdit, QTextEdit, QComboBox {
    background-color: #16161D;
    color: #E0E0E6;
    border: 1px solid #2A2A35;
    border-radius: 6px;
    padding: 8px;
}

QLineEdit:focus, QTextEdit:focus, QComboBox:focus {
    border: 1px solid #4F46E5;
}

/* Labels */
QLabel#Header {
    font-size: 18px;
    font-weight: bold;
    color: #FFFFFF;
}

QLabel#SubHeader {
    font-size: 14px;
    font-weight: 600;
    color: #9CA3AF;
}

/* Scrollbars */
QScrollBar:vertical {
    border: none;
    background: #0F0F12;
    width: 8px;
    margin: 0px;
}

QScrollBar::handle:vertical {
    background: #2A2A35;
    min-height: 20px;
    border-radius: 4px;
}

QScrollBar::handle:vertical:hover {
    background: #3D3D4D;
}

/* Tabs */
QTabWidget::pane {
    border: 1px solid #2A2A35;
    background: #16161D;
    border-radius: 8px;
}

QTabBar::tab {
    background: #16161D;
    color: #9CA3AF;
    padding: 10px 20px;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
}

QTabBar::tab:selected {
    background: #1C1C26;
    color: #FFFFFF;
    border-bottom: 2px solid #4F46E5;
}
"""
