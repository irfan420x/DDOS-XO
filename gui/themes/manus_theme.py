# Path: gui/themes/manus_theme.py

MANUS_STYLE = """
QMainWindow {
    background-color: #0A0A0C;
    color: #E2E2E9;
}

QWidget {
    font-family: 'Inter', 'Segoe UI', 'Roboto', sans-serif;
    font-size: 13px;
}

/* Sidebar Styling */
QFrame#Sidebar {
    background-color: #111114;
    border-right: 1px solid #1F1F23;
}

/* Main Content Area */
QFrame#MainContent {
    background-color: #0A0A0C;
}

/* Panels & Cards */
QFrame#Panel {
    background-color: #141417;
    border: 1px solid #232328;
    border-radius: 16px;
}

QFrame#Panel:hover {
    border: 1px solid #303038;
}

/* Buttons */
QPushButton {
    background-color: #1F1F23;
    color: #E2E2E9;
    border: 1px solid #2D2D35;
    border-radius: 10px;
    padding: 10px 20px;
    font-weight: 600;
}

QPushButton:hover {
    background-color: #2D2D35;
    border: 1px solid #3D3D48;
}

QPushButton#PrimaryButton {
    background-color: #5850EC;
    color: white;
    border: none;
    font-weight: bold;
}

QPushButton#PrimaryButton:hover {
    background-color: #6366F1;
}

QPushButton#DangerButton {
    background-color: #EF4444;
    color: white;
    border: none;
}

/* Inputs */
QLineEdit, QTextEdit, QComboBox {
    background-color: #111114;
    color: #E2E2E9;
    border: 1px solid #1F1F23;
    border-radius: 10px;
    padding: 12px;
    selection-background-color: #5850EC;
}

QLineEdit:focus, QTextEdit:focus, QComboBox:focus {
    border: 1px solid #5850EC;
    background-color: #141417;
}

/* Labels */
QLabel#Header {
    font-size: 22px;
    font-weight: 800;
    color: #FFFFFF;
    letter-spacing: -0.5px;
}

QLabel#SubHeader {
    font-size: 12px;
    font-weight: 700;
    color: #6B7280;
    text-transform: uppercase;
    letter-spacing: 1px;
}

/* Scrollbars */
QScrollBar:vertical {
    border: none;
    background: transparent;
    width: 6px;
    margin: 0px;
}

QScrollBar::handle:vertical {
    background: #2D2D35;
    min-height: 30px;
    border-radius: 3px;
}

QScrollBar::handle:vertical:hover {
    background: #3D3D48;
}

/* Progress Bars */
QProgressBar {
    background-color: #1F1F23;
    border: none;
    border-radius: 3px;
    text-align: center;
}

QProgressBar::chunk {
    background-color: #5850EC;
    border-radius: 3px;
}

/* Tabs */
QTabWidget::pane {
    border: 1px solid #1F1F23;
    background: #111114;
    border-radius: 12px;
}

QTabBar::tab {
    background: transparent;
    color: #6B7280;
    padding: 12px 24px;
    font-weight: 600;
}

QTabBar::tab:selected {
    color: #FFFFFF;
    border-bottom: 2px solid #5850EC;
}

/* Chat Bubbles (Simulated via HTML in QTextEdit) */
.user-msg {
    background-color: #1F1F23;
    border-radius: 12px;
    padding: 10px;
    margin: 5px;
    color: #E2E2E9;
}

.luna-msg {
    background-color: #141417;
    border-left: 4px solid #5850EC;
    padding: 10px;
    margin: 5px;
    color: #FFFFFF;
}
"""
