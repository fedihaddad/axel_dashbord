"""
Connection Dialog
Allow user to select connection method (Ethernet or WiFi) before controlling robot
"""

from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                             QRadioButton, QButtonGroup, QLineEdit, QSpinBox,
                             QGroupBox, QFormLayout, QProgressBar, QMessageBox)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer, QThread
from PyQt6.QtGui import QFont, QIcon
import socket
import time


class ConnectionWorker(QThread):
    """Background worker for connection attempts"""
    
    connection_status = pyqtSignal(bool, str)  # success, message
    
    def __init__(self, connection_type, ip, port, timeout):
        super().__init__()
        self.connection_type = connection_type
        self.ip = ip
        self.port = port
        self.timeout = timeout
        self._is_running = True
    
    def run(self):
        """Try to connect to robot"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            
            # Try to connect
            result = sock.connect_ex((self.ip, self.port))
            sock.close()
            
            if result == 0:
                self.connection_status.emit(
                    True,
                    f"✓ Connected via {self.connection_type}\nIP: {self.ip}:{self.port}"
                )
            else:
                self.connection_status.emit(
                    False,
                    f"✗ Could not connect to robot at {self.ip}:{self.port}"
                )
        except Exception as e:
            self.connection_status.emit(False, f"✗ Connection error: {str(e)}")
    
    def stop(self):
        """Stop the worker"""
        self._is_running = False


class ConnectionDialog(QDialog):
    """Dialog for selecting and establishing robot connection"""
    
    connection_established = pyqtSignal(str, str, int)  # connection_type, ip, port
    
    def __init__(self, config, parent=None):
        super().__init__(parent)
        self.config = config
        self.connection_worker = None
        self.setWindowTitle("AXEL - Robot Connection")
        self.setGeometry(100, 100, 600, 500)
        self.setModal(True)
        # Ensure window appears on top and is visible
        from PyQt6.QtCore import Qt
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
        
        self.init_ui()
        
    def init_ui(self):
        """Initialize UI components"""
        layout = QVBoxLayout()
        
        # Header with AXEL branding
        header = QLabel("AXEL Robot Control System")
        header_font = QFont()
        header_font.setPointSize(18)
        header_font.setBold(True)
        header.setFont(header_font)
        header.setStyleSheet("color: #0066cc; margin-bottom: 10px;")
        layout.addWidget(header)
        
        subtitle = QLabel("Select connection method to control the robot")
        subtitle_font = QFont()
        subtitle_font.setPointSize(11)
        subtitle.setFont(subtitle_font)
        subtitle.setStyleSheet("color: #666666; margin-bottom: 20px;")
        layout.addWidget(subtitle)
        
        # Simulation mode option (for development/testing)
        self.connection_group = QButtonGroup()
        
        # Simulation mode
        simulation_box = QGroupBox("SIMULATION MODE (Development)")
        simulation_layout = QVBoxLayout()
        self.simulation_radio = QRadioButton("Run in simulation mode (no real robot needed)")
        self.simulation_radio.setChecked(True)  # Default to simulation
        self.connection_group.addButton(self.simulation_radio, 2)
        simulation_layout.addWidget(self.simulation_radio)
        sim_desc = QLabel("Perfect for testing UI and developing features without a physical robot")
        sim_desc.setStyleSheet("color: #666666; font-size: 10px; margin-left: 20px;")
        simulation_layout.addWidget(sim_desc)
        simulation_box.setLayout(simulation_layout)
        layout.addWidget(simulation_box)
        
        # Divider
        divider = QLabel("--- OR ---")
        divider.setStyleSheet("color: #cccccc; text-align: center; margin: 10px 0;")
        layout.addWidget(divider)
        
        # Connection method selection
        # Ethernet option
        ethernet_box = self.create_connection_box(
            "ethernet",
            "🔌 Ethernet Connection",
            "Wired connection - recommended for stability",
            self.config.get("connection", {}).get("ethernet", {})
        )
        layout.addWidget(ethernet_box)
        
        # WiFi option
        wifi_box = self.create_connection_box(
            "wifi",
            "📡 WiFi Connection",
            "Wireless connection - for mobile operation",
            self.config.get("connection", {}).get("wifi", {})
        )
        layout.addWidget(wifi_box)
        
        # Progress bar (hidden initially)
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setMaximum(0)  # Indeterminate progress
        layout.addWidget(self.progress_bar)
        
        # Status label
        self.status_label = QLabel()
        self.status_label.setStyleSheet("color: #333333; margin: 10px 0;")
        layout.addWidget(self.status_label)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.connect_btn = QPushButton("🔗 Connect")
        self.connect_btn.setStyleSheet("""
            QPushButton {
                background-color: #0066cc;
                color: white;
                padding: 10px 20px;
                font-size: 12px;
                font-weight: bold;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #0052a3;
            }
            QPushButton:pressed {
                background-color: #003d7a;
            }
        """)
        self.connect_btn.clicked.connect(self.on_connect)
        button_layout.addWidget(self.connect_btn)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #cccccc;
                color: black;
                padding: 10px 20px;
                font-size: 12px;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #aaaaaa;
            }
        """)
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
        layout.addStretch()
        
        self.setLayout(layout)
        
        # Set default connection type
        default = self.config.get("connection", {}).get("default_connection", "ethernet")
        if default == "wifi":
            self.wifi_radio.setChecked(True)
        else:
            self.ethernet_radio.setChecked(True)
    
    def create_connection_box(self, connection_id, title, description, settings):
        """Create a connection option box"""
        box = QGroupBox(title)
        layout = QVBoxLayout()
        
        # Description
        desc_label = QLabel(description)
        desc_label.setStyleSheet("color: #666666; font-size: 10px;")
        layout.addWidget(desc_label)
        
        # Radio button
        radio = QRadioButton("")
        self.connection_group.addButton(radio, 0 if connection_id == "ethernet" else 1)
        
        if connection_id == "ethernet":
            self.ethernet_radio = radio
            self.ethernet_settings = {}
        else:
            self.wifi_radio = radio
            self.wifi_settings = {}
        
        # Settings form
        form = QFormLayout()
        
        # IP Address
        ip_input = QLineEdit()
        ip_input.setText(settings.get("ip_address", "192.168.1.100"))
        ip_input.setPlaceholderText("192.168.1.100")
        form.addRow("IP Address:", ip_input)
        
        if connection_id == "ethernet":
            self.ethernet_ip = ip_input
        else:
            self.wifi_ip = ip_input
        
        # Port
        port_input = QSpinBox()
        port_input.setMinimum(1)
        port_input.setMaximum(65535)
        port_input.setValue(settings.get("port", 5005))
        form.addRow("Port:", port_input)
        
        if connection_id == "ethernet":
            self.ethernet_port = port_input
        else:
            self.wifi_port = port_input
        
        # Timeout
        timeout_input = QSpinBox()
        timeout_input.setMinimum(1)
        timeout_input.setMaximum(30)
        timeout_input.setValue(settings.get("timeout", 5))
        timeout_input.setSuffix(" sec")
        form.addRow("Timeout:", timeout_input)
        
        if connection_id == "ethernet":
            self.ethernet_timeout = timeout_input
        else:
            self.wifi_timeout = timeout_input
        
        # Add radio and form to layout
        radio_layout = QHBoxLayout()
        radio_layout.addWidget(radio)
        radio_layout.addLayout(form)
        radio_layout.addStretch()
        layout.addLayout(radio_layout)
        
        box.setLayout(layout)
        box.setStyleSheet("""
            QGroupBox {
                border: 2px solid #cccccc;
                border-radius: 4px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px 0 3px;
            }
        """)
        
        return box
    
    def on_connect(self):
        """Attempt to connect to robot"""
        # Check if simulation mode is selected
        if self.connection_group.checkedId() == 2:  # Simulation
            self.progress_bar.setVisible(True)
            self.connect_btn.setEnabled(False)
            self.status_label.setText("Simulation mode activated...")
            self.status_label.setStyleSheet("color: #0066cc;")
            
            # Simulate a short "loading" period
            QTimer.singleShot(1000, self.on_simulation_success)
            return
        
        # Real connection attempt
        # Determine which connection type is selected
        if self.connection_group.checkedId() == 0:  # Ethernet
            connection_type = "Ethernet"
            ip = self.ethernet_ip.text()
            port = self.ethernet_port.value()
            timeout = self.ethernet_timeout.value()
        else:  # WiFi (ID = 1)
            connection_type = "WiFi"
            ip = self.wifi_ip.text()
            port = self.wifi_port.value()
            timeout = self.wifi_timeout.value()
        
        # Validate IP
        if not self.is_valid_ip(ip):
            QMessageBox.warning(self, "Invalid IP", "Please enter a valid IP address")
            return
        
        # Show progress
        self.progress_bar.setVisible(True)
        self.connect_btn.setEnabled(False)
        self.status_label.setText("Connecting...")
        self.status_label.setStyleSheet("color: #0066cc;")
        
        # Start connection worker
        self.connection_worker = ConnectionWorker(connection_type, ip, port, timeout)
        self.connection_worker.connection_status.connect(self.on_connection_result)
        self.connection_worker.start()
    
    def on_simulation_success(self):
        """Handle successful simulation mode activation"""
        self.progress_bar.setVisible(False)
        self.connect_btn.setEnabled(True)
        
        self.status_label.setText("[SIM] Simulation Mode Ready!")
        self.status_label.setStyleSheet("color: #00aa00; font-weight: bold;")
        
        # Emit connection established with "simulation" connection type
        self.connection_established.emit("simulation", "127.0.0.1", 5005)
        self.accept()
    
    def on_connection_result(self, success, message):
        """Handle connection result"""
        self.progress_bar.setVisible(False)
        self.connect_btn.setEnabled(True)
        
        if success:
            self.status_label.setText(message)
            self.status_label.setStyleSheet("color: #00aa00; font-weight: bold;")
            
            # Determine connection type
            if self.connection_group.checkedId() == 0:  # Ethernet
                connection_type = "ethernet"
                ip = self.ethernet_ip.text()
                port = self.ethernet_port.value()
            else:  # WiFi
                connection_type = "wifi"
                ip = self.wifi_ip.text()
                port = self.wifi_port.value()
            
            # Wait a moment then close dialog
            QTimer.singleShot(1500, lambda: self.on_connection_success(connection_type, ip, port))
        else:
            self.status_label.setText(message)
            self.status_label.setStyleSheet("color: #cc0000; font-weight: bold;")
    
    def on_connection_success(self, connection_type, ip, port):
        """Called when connection succeeds"""
        self.connection_established.emit(connection_type, ip, port)
        self.accept()
    
    @staticmethod
    def is_valid_ip(ip_string):
        """Validate IP address format"""
        parts = ip_string.split('.')
        if len(parts) != 4:
            return False
        try:
            return all(0 <= int(part) <= 255 for part in parts)
        except ValueError:
            return False


if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    
    # Mock config
    config = {
        "connection": {
            "default_connection": "ethernet",
            "ethernet": {
                "ip_address": "192.168.1.100",
                "port": 5005,
                "timeout": 5
            },
            "wifi": {
                "ip_address": "192.168.1.200",
                "port": 5005,
                "timeout": 5
            }
        }
    }
    
    dialog = ConnectionDialog(config)
    dialog.connection_established.connect(
        lambda t, ip, p: print(f"Connected via {t} at {ip}:{p}")
    )
    dialog.exec()
