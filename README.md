# Bionic Reading PDF Converter (Standalone)

A simple command-line tool to convert PDFs with bionic reading enhancement.

## Quick Start

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Convert a PDF:
   ```bash
   python3 process_pdf.py your_file.pdf -o enhanced.pdf
   ```

3. Open `index.html` in a browser for a visual interface and live preview.

## Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `-r, --ratio` | Emphasis ratio (0.1-0.7) | 0.4 |
| `-m, --min-length` | Minimum word length | 3 |
| `-i, --intensity` | Bold intensity (light/medium/heavy) | medium |

## Example

```bash
# Light emphasis
python3 process_pdf.py document.pdf -o output.pdf -r 0.3 -i light

# Heavy emphasis
python3 process_pdf.py document.pdf -o output.pdf -r 0.5 -i heavy
```

## How It Works

The bionic reading algorithm:
1. Extracts text from your PDF
2. Bolds the first portion of each word
3. Rebuilds the PDF with enhanced readability

This helps readers with ADHD by providing visual anchors that guide the eye through text.
