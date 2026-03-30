#!/bin/bash
# AXEL Robot PC Software - Installation and Quick Start Script

echo "=========================================="
echo "AXEL Robot Software Setup Script"
echo "=========================================="
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version || { echo "Python 3 not found!"; exit 1; }

# Create virtual environment
echo ""
echo "Creating Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo ""
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Run tests
echo ""
echo "Running tests to verify setup..."
pytest tests/ -v || { echo "Tests failed!"; exit 1; }

echo ""
echo "=========================================="
echo "✅ Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Activate virtual environment:"
echo "   source venv/bin/activate"
echo ""
echo "2. Run the application:"
echo "   python axel_gui/main_window.py"
echo ""
echo "3. Read documentation:"
echo "   - docs/QUICKSTART.md (getting started)"
echo "   - docs/ARCHITECTURE.md (system design)"
echo "   - README.md (project overview)"
echo ""
echo "Happy coding! 🚀"
