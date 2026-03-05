# Bionic Reading PDF Converter

Transform PDFs with bionic reading enhancement - optimized for ADHD readers.

## Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/RootlessOnline/bionic-reading-converter.git
cd bionic-reading-converter
```

### 2. Run the setup script
```bash
chmod +x setup.sh
./setup.sh
```

This will:
- Create a Python virtual environment
- Install all required dependencies

### 3. Convert a PDF
```bash
source venv/bin/activate
python3 process_pdf.py your_file.pdf -o enhanced.pdf
```

### Or use the interactive script:
```bash
./run.sh
```

## Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `-r, --ratio` | Emphasis ratio (0.1-0.7) | 0.4 |
| `-m, --min-length` | Minimum word length | 3 |
| `-i, --intensity` | Bold intensity (light/medium/heavy) | medium |

## Examples

```bash
# Basic usage
python3 process_pdf.py document.pdf -o enhanced.pdf

# Light emphasis
python3 process_pdf.py document.pdf -o enhanced.pdf -r 0.3 -i light

# Heavy emphasis
python3 process_pdf.py document.pdf -o enhanced.pdf -r 0.5 -i heavy
```

## What is Bionic Reading?

Bionic reading is a method that highlights the initial letters or syllables of words, helping guide the reader's eye through text more efficiently. This can:

- Improve reading speed by up to 25%
- Reduce cognitive load
- Help readers with ADHD maintain focus
- Prevent skipping lines

## Files Included

| File | Description |
|------|-------------|
| `process_pdf.py` | Main processing script |
| `bionic_reader.py` | Bionic transformation algorithm |
| `pdf_extractor.py` | PDF text extraction |
| `pdf_generator.py` | PDF reconstruction |
| `index.html` | Visual preview interface |
| `sample_document.pdf` | Test PDF |

## Requirements

- Python 3.8+
- The setup script will install: pdfplumber, reportlab, pypdf, regex, Pillow

## License

MIT License - Feel free to use and modify!
