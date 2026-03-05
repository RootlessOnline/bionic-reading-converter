#!/bin/bash
# Bionic Reading PDF Converter - Setup Script
# This script sets up a virtual environment and installs dependencies

echo "🚀 Setting up Bionic Reading PDF Converter..."
echo ""

# Check if python3-venv is installed
if ! python3 -m venv --help &> /dev/null; then
    echo "⚠️  python3-venv is not installed."
    echo "   Installing it now (requires sudo)..."
    sudo apt update && sudo apt install -y python3-venv python3-pip
    echo ""
fi

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing Python dependencies..."
pip install --upgrade pip
pip install pdfplumber reportlab pypdf regex Pillow

echo ""
echo "✅ Setup complete!"
echo ""
echo "To use the converter:"
echo "  1. Activate the virtual environment: source venv/bin/activate"
echo "  2. Run: python3 process_pdf.py your_file.pdf -o enhanced.pdf"
echo ""
echo "Or run: ./run.sh"
