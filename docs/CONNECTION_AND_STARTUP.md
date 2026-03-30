# AXEL Connection & Startup Flow

## 🚀 Professional Startup Experience

The AXEL robot control software now features a professional startup flow that matches industry standards like NED2:

### Flow Sequence

```
1. Application Launch
        ↓
2. Splash Screen (AXEL Animated Logo)
   └─ Shows loading animation with rotating circle
   └─ Fade-in text effect
   └─ Duration: ~5 seconds
        ↓
3. Core Module Initialization
   └─ StateManager initialized
   └─ SafetyManager initialized
   └─ RobotController initialized
        ↓
4. Connection Dialog (Ethernet or WiFi)
   └─ User selects connection type
   └─ Configurable IP/Port/Timeout
   └─ Validates and tests connection
        ↓
5. Main Control Window
   └─ Once connected, full control interface appears
   └─ Ready for robot control
```

## 🔌 Connection Options

### Ethernet Connection (Recommended)
- **Default**: Yes
- **IP Address**: 192.168.1.100 (configurable)
- **Port**: 5005 (configurable)
- **Timeout**: 5 seconds (configurable)
- **Stability**: Wired connection - most reliable
- **Use Case**: Lab/development, stationary robot

### WiFi Connection (Mobile)
- **Default**: Alternative
- **IP Address**: 192.168.1.200 (configurable)
- **Port**: 5005 (configurable)
- **Timeout**: 5 seconds (configurable)
- **Mobility**: Wireless - can move robot anywhere in lab
- **Use Case**: Demonstrations, field testing, mobile operation

## ⚙️ Configuration

Edit `config/robot_config.yaml`:

```yaml
connection:
  type: "both"  # "ethernet", "wifi", or "both"
  default_connection: "ethernet"  # Shown first in dialog
  
  ethernet:
    enabled: true
    ip_address: "192.168.1.100"
    port: 5005
    timeout: 5  # seconds
  
  wifi:
    enabled: true
    ssid: "AXEL_ROBOT"  # Network name
    ip_address: "192.168.1.200"
    port: 5005
    timeout: 5  # seconds

power:
  battery_enabled: false  # Robot always powered via AC/secteur
  has_battery_display: false
  cpu_temp_monitoring: true
```

## 🖼️ Splash Screen

Professional animated splash screen with:
- **Dark gradient background** - Professional appearance
- **Animated loading circle** - Shows system is initializing
- **Fade-in text** - "AXEL" appears smoothly
- **Subtitle** - "Humanoid Robot Control System"
- **Loading indicator** - "Initializing..." with dots

### Customization

Edit `axel_gui/splash_screen.py`:

```python
# Change colors
pixmap.fill(QColor(30, 30, 40))  # Background
circle_color = QColor(100, 150, 255)  # Loading ring
text_color = QColor(255, 255, 255)  # "AXEL" text

# Change animation speed
self.timer.start(30)  # milliseconds per frame (lower = faster)

# Change text
painter.drawText(..., "Your Robot Name")
```

## 🔗 Connection Dialog

Professional connection interface with:

### Features
- **Radio buttons** - Clear selection of Ethernet or WiFi
- **Configuration fields** - IP address, port, timeout customizable
- **Connection validation** - Tests connection before accepting
- **Status display** - Shows connection progress and results
- **Professional styling** - Blue buttons, clean layout

### User Flow

1. **Select Connection Type**
   - Radio button for Ethernet (default)
   - Radio button for WiFi
   - Both show current configuration

2. **Configure Settings** (if needed)
   - IP Address field (validates format)
   - Port field (1-65535)
   - Timeout field (seconds)

3. **Connect**
   - Click "Connect" button
   - Progress bar shows (indeterminate)
   - Connection test runs in background thread
   - Success or error message shown

4. **Continue or Retry**
   - Success → Main window opens
   - Failure → Can retry or cancel

## 🔄 State Management

### ConnectionStatus
The StateManager now tracks connection state:

```python
# Update connection status
state_manager.update_connection_status("connected", "ethernet")

# Get current status
state = state_manager.get_current_state()
print(state.connection_status)  # "connected", "connecting", or "disconnected"
print(state.connection_type)    # "ethernet" or "wifi"
```

### No Battery Tracking
**IMPORTANT**: Robot is always powered via AC (secteur).

- Battery level display removed
- CPU temperature monitoring still available
- RobotState no longer tracks `battery_level`
- Configuration has `battery_enabled: false`

## 🧪 Testing Startup Components

Run the startup test without launching full GUI:

```bash
python test_startup.py
```

This will:
1. Create and display splash screen
2. Create and display connection dialog
3. Verify both components work correctly

## 📝 Code Integration

### In Main Application

The flow is automatically handled:

```python
# axel_gui/main_window.py

class AXELMainWindow:
    def run(self):
        # 1. Show splash
        self.show_splash_screen()
        
        # 2. Create main window
        self.setup_ui()
        
        # 3. Initialize modules
        self.initialize_core_modules()
        
        # 4. Close splash, show connection dialog
        self.show_connection_dialog()
        
        # 5. Show main window when connected
        self.window.show()
        
        return self.app.exec()
```

### Manual Connection Dialog Usage

```python
from axel_gui.connection_dialog import ConnectionDialog

dialog = ConnectionDialog(config)
dialog.connection_established.connect(
    lambda t, ip, p: print(f"Connected via {t} at {ip}:{p}")
)

if dialog.exec():  # Returns True if connected
    print("User connected successfully")
else:
    print("User cancelled connection")
```

### Manual Splash Screen Usage

```python
from axel_gui.splash_screen import AXELSplashScreen

splash = AXELSplashScreen()
splash.animation_finished.connect(lambda: print("Splash animation done"))
splash.show_with_animation()
```

## 🎨 Styling Customization

### Splash Screen
Edit colors and fonts in `axel_gui/splash_screen.py`:
- Background gradient colors (lines 41-42)
- Circle/ring colors (lines 64-69)
- Text color and fade (lines 73-75)
- Font sizes (lines 55, 80, 86)

### Connection Dialog
Edit styles in `axel_gui/connection_dialog.py`:
- Button colors and styling (lines 180-200)
- Text colors (lines 168-169)
- Form field styling (lines 230-280)

Example custom style:

```python
self.connect_btn.setStyleSheet("""
    QPushButton {
        background-color: #00AA00;  # Green instead of blue
        color: white;
        padding: 10px 20px;
        font-weight: bold;
        border-radius: 4px;
    }
    QPushButton:hover {
        background-color: #008800;
    }
""")
```

## 🚨 Error Handling

### Connection Failures
- **Invalid IP format**: Dialog shows error message, suggests correct format
- **Network unreachable**: Shows "Could not connect to robot"
- **Timeout**: Shows "Connection timeout" with retry option
- **Port closed**: Shows "Port not open on robot"

### Recovery
- User can modify IP/port/timeout and retry
- Cancel button always available
- Application closes gracefully if cancelled

## 📊 Status Information

After connection, status bar shows:
```
Connected: ETHERNET | 192.168.1.100:5005 | Temp: 45.2°C | E-STOP: OK
```

Components:
- Connection type (ETHERNET or WIFI)
- IP:Port
- CPU temperature
- E-STOP status

## 🔐 Security Considerations

- No password authentication (internal network)
- IP validation prevents malformed addresses
- Connection timeout prevents hanging
- E-STOP always available regardless of connection state

## 📚 Related Files

- **Configuration**: `config/robot_config.yaml`
- **Splash Screen**: `axel_gui/splash_screen.py` (240 lines)
- **Connection Dialog**: `axel_gui/connection_dialog.py` (390 lines)
- **Main Window**: `axel_gui/main_window.py` (updated with integration)
- **State Manager**: `axel_core/state_manager.py` (updated for connection tracking)
- **Tests**: `tests/test_core.py` (updated test cases)

## ✅ Checklist - Ready for Phase 2

- [x] Splash screen with AXEL animation
- [x] Connection dialog with Ethernet/WiFi options
- [x] IP address validation
- [x] Connection testing and feedback
- [x] StateManager updated for connection tracking
- [x] Battery removed (always-powered robot)
- [x] Professional styling and animations
- [x] All tests passing (14/14)
- [x] Startup flow documented

## 🎯 Next Steps (Phase 2)

Once users can connect:
1. **Control Panel** - Joint sliders for robot movement
2. **Monitoring Panel** - Real-time status display
3. **Safety Panel** - E-STOP interface
4. **Teach Panel** - Position saving/loading
5. **3D Visualization** - Real-time visualization

Then Phase 3:
- URDF model creation
- Gazebo simulation setup
- RViz integration

See `QUICK_ACTION_PLAN.md` and `NED2_COMPARISON_ROADMAP.md` for details.
