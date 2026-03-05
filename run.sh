#!/bin/bash
echo "Installing Python dependencies..."
pip install -r requirements.txt

echo ""
echo "=========================================="
echo "Bionic Reading PDF Converter"
echo "=========================================="
echo ""
echo "Usage:"
echo "  python3 process_pdf.py input.pdf -o output.pdf [options]"
echo ""
echo "Options:"
echo "  -r, --ratio      Emphasis ratio (0.1-0.7, default: 0.4)"
echo "  -m, --min-length Minimum word length (default: 3)"
echo "  -i, --intensity  Bold intensity: light, medium, heavy"
echo ""
echo "Example:"
echo "  python3 process_pdf.py sample_document.pdf -o enhanced.pdf -r 0.4 -m 3 -i medium"
echo ""

# Test with sample
read -p "Process sample PDF? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then
    python3 process_pdf.py sample_document.pdf -o sample_bionic_enhanced.pdf -r 0.4 -m 3 -i medium
    echo ""
    echo "✅ Done! Check sample_bionic_enhanced.pdf"
fi
