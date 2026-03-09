#!/bin/bash
# BhilNet Development Environment Setup

echo "🚀 Setting up BhilNet development environment..."

# Check if Python 3.8+ is installed
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" = "$required_version" ]; then
    echo "✅ Python $python_version detected (>= 3.8 required)"
else
    echo "❌ Python $python_version detected (>= 3.8 required)"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Create configuration directory
echo "📁 Creating configuration directory..."
mkdir -p logs

echo "✅ Development environment setup complete!"
echo ""
echo "🎮 To start BhilNet:"
echo "   source venv/bin/activate"
echo "   python main.py"
echo ""
echo "🔧 To deactivate environment:"
echo "   deactivate"
