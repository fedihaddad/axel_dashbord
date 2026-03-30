"""
AXEL Robot PC Software - Setup Configuration

Academic Project (PFE) for humanoid robot supervision and simulation
"""

from setuptools import setup, find_packages

setup(
    name="axel-robot-software",
    version="0.1.0",
    description="Desktop PC application for AXEL humanoid robot supervision",
    author="Your Name",
    author_email="your.email@institution.com",
    url="https://github.com/yourusername/axel-robot-software",
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=[
        "PyQt6>=6.0.0",
        "numpy>=1.20.0",
        "PyYAML>=5.4.0",
        "pydantic>=2.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "pylint>=2.15.0",
        ],
        "ros": [
            "rclpy>=0.13.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "axel-gui=axel_gui.main_window:main",
        ]
    },
)
