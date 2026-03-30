"""
Splash Screen with AXEL Animation
AXEL is a copy/clone of InMoov 2 - Full humanoid with 20 joints
Professional startup animation shown when application launches
"""

from PyQt6.QtWidgets import QSplashScreen, QApplication, QMainWindow
from PyQt6.QtGui import QPixmap, QPainter, QColor, QFont, QLinearGradient
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QRect, QSize
import sys


class AXELSplashScreen(QSplashScreen):
    """Professional splash screen with AXEL logo and animation"""
    
    animation_finished = pyqtSignal()
    
    def __init__(self, parent=None):
        # Create a custom pixmap for the splash screen
        pixmap = QPixmap(800, 600)
        pixmap.fill(QColor(30, 30, 40))  # Dark background
        
        super().__init__(pixmap)
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.FramelessWindowHint)
        
        self.animation_step = 0
        self.max_steps = 50
        
        # Timer for animation
        self.timer = QTimer()
        self.timer.timeout.connect(self.animate_splash)
        
    def show_with_animation(self):
        """Show splash screen and start animation"""
        self.show()
        self.timer.start(30)  # Update every 30ms for smooth animation
        
    def animate_splash(self):
        """Update splash screen animation"""
        if self.animation_step < self.max_steps:
            self.animation_step += 1
            self.update_splash_content()
        else:
            self.timer.stop()
            self.animation_finished.emit()
            
    def update_splash_content(self):
        """Paint animated splash screen content"""
        pixmap = QPixmap(800, 600)
        
        # Gradient background (dark to slightly lighter)
        gradient = QLinearGradient(0, 0, 800, 600)
        gradient.setColorAt(0, QColor(25, 25, 35))
        gradient.setColorAt(1, QColor(45, 45, 60))
        pixmap.fill(QColor(30, 30, 40))
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.fillRect(pixmap.rect(), gradient)
        
        # Animated circle (loading indicator)
        progress = self.animation_step / self.max_steps
        circle_angle = int(progress * 360)
        circle_center_x, circle_center_y = 400, 250
        circle_radius = 60
        
        # Draw outer circle
        painter.setPen(QColor(100, 150, 255))  # Blue
        painter.drawEllipse(
            circle_center_x - circle_radius,
            circle_center_y - circle_radius,
            circle_radius * 2,
            circle_radius * 2
        )
        
        # Draw rotating arc
        painter.setPen(QColor(0, 100, 255))
        painter.drawArc(
            circle_center_x - circle_radius,
            circle_center_y - circle_radius,
            circle_radius * 2,
            circle_radius * 2,
            0, circle_angle * 16  # Qt uses 16th of degree
        )
        
        # Draw AXEL text with fade-in effect
        font = QFont()
        font.setPointSize(72)
        font.setBold(True)
        painter.setFont(font)
        
        # Alpha fade-in: text becomes more visible as animation progresses
        alpha = int(255 * (progress ** 0.5))  # Smoother fade with square root
        text_color = QColor(255, 255, 255, alpha)
        painter.setPen(text_color)
        
        painter.drawText(QRect(0, 350, 800, 100), Qt.AlignmentFlag.AlignCenter, "AXEL")
        
        # Draw subtitle
        font.setPointSize(14)
        painter.setFont(font)
        subtitle_color = QColor(150, 200, 255, int(alpha * 0.7))
        painter.setPen(subtitle_color)
        painter.drawText(
            QRect(0, 480, 800, 40),
            Qt.AlignmentFlag.AlignCenter,
            "Humanoid Robot (InMoov 2 Clone) | 20 Joints | 2 Arms | 10 Fingers"
        )
        
        # Draw loading text
        loading_text = "Initializing" + "." * ((self.animation_step // 10) % 4)
        font.setPointSize(11)
        painter.setFont(font)
        loading_color = QColor(100, 150, 255, alpha)
        painter.setPen(loading_color)
        painter.drawText(QRect(0, 540, 800, 40), Qt.AlignmentFlag.AlignCenter, loading_text)
        
        painter.end()
        self.setPixmap(pixmap)


def show_splash_screen():
    """Create and show splash screen"""
    splash = AXELSplashScreen()
    splash.show_with_animation()
    QApplication.processEvents()
    return splash


if __name__ == "__main__":
    app = QApplication(sys.argv)
    splash = show_splash_screen()
    
    # Simulate work
    QTimer.singleShot(4000, app.quit)
    
    sys.exit(app.exec())
