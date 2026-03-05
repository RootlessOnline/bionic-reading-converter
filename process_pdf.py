#!/usr/bin/env python3
"""
PDF Processing Script

Main orchestration script that coordinates:
1. PDF text extraction
2. Bionic reading transformation
3. Enhanced PDF generation

Provides progress reporting and handles large files efficiently.
"""

import sys
import os
import json
import argparse
import tempfile
import time
from pathlib import Path
from typing import Optional, Dict, Any
from dataclasses import dataclass, asdict

# Add scripts directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pdf_extractor import PDFExtractor, PDFDocument
from pdf_generator import PDFGenerator, GeneratorConfig
from bionic_reader import BionicReader, BionicConfig


@dataclass
class ProcessingConfig:
    """Configuration for PDF processing."""
    input_path: str
    output_path: str
    emphasis_ratio: float = 0.4
    min_word_length: int = 3
    bold_intensity: str = "medium"
    skip_short_words: bool = True
    preserve_layout: bool = True
    extract_images: bool = False
    extract_tables: bool = False


@dataclass
class ProcessingProgress:
    """Progress tracking for processing."""
    stage: str
    progress: float  # 0-100
    message: str
    timestamp: float

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class PDFProcessor:
    """Main PDF processor with bionic reading enhancement."""

    def __init__(self, config: ProcessingConfig):
        """Initialize processor with configuration."""
        self.config = config
        self.progress_callback = None
        self.start_time = time.time()

    def set_progress_callback(self, callback):
        """Set callback function for progress updates."""
        self.progress_callback = callback

    def report_progress(self, stage: str, progress: float, message: str):
        """Report processing progress."""
        progress_obj = ProcessingProgress(
            stage=stage,
            progress=progress,
            message=message,
            timestamp=time.time()
        )

        if self.progress_callback:
            self.progress_callback(progress_obj)
        else:
            print(json.dumps(progress_obj.to_dict()))

    def validate_input(self) -> bool:
        """Validate input file exists and is a PDF."""
        if not os.path.exists(self.config.input_path):
            raise FileNotFoundError(f"Input file not found: {self.config.input_path}")

        if not self.config.input_path.lower().endswith('.pdf'):
            raise ValueError("Input file must be a PDF file")

        # Check file size
        file_size = os.path.getsize(self.config.input_path)
        max_size = 50 * 1024 * 1024  # 50MB

        if file_size > max_size:
            raise ValueError(f"File too large: {file_size / 1024 / 1024:.1f}MB (max: 50MB)")

        return True

    def extract_pdf(self) -> PDFDocument:
        """Extract content from the input PDF."""
        self.report_progress("extraction", 0, "Starting PDF extraction...")

        extractor = PDFExtractor(
            extract_images=self.config.extract_images,
            extract_tables=self.config.extract_tables
        )

        document = extractor.extract(self.config.input_path)

        self.report_progress("extraction", 100, f"Extracted {document.num_pages} pages")

        return document

    def generate_pdf(self, document: PDFDocument) -> str:
        """Generate enhanced PDF with bionic reading."""
        self.report_progress("generation", 0, "Starting PDF generation...")

        # Create output directory if needed
        output_dir = os.path.dirname(self.config.output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)

        bionic_config = BionicConfig(
            emphasis_ratio=self.config.emphasis_ratio,
            min_word_length=self.config.min_word_length,
            skip_short_words=self.config.skip_short_words,
            bold_intensity=self.config.bold_intensity,
            preserve_formatting=True
        )

        generator_config = GeneratorConfig(
            output_path=self.config.output_path,
            apply_bionic=True,  # Enable bionic transformation in generator
            bionic_config=bionic_config,
            preserve_layout=self.config.preserve_layout
        )

        generator = PDFGenerator(generator_config)

        if self.config.preserve_layout:
            output_path = generator.generate_simple_pdf(document)
        else:
            output_path = generator.generate_text_flow_pdf(document)

        # Add Z.ai metadata
        self.report_progress("generation", 90, "Adding metadata...")
        try:
            from add_zai_metadata import add_metadata
            title = os.path.splitext(os.path.basename(self.config.input_path))[0]
            add_metadata(output_path, title=f"{title} - Bionic Enhanced")
        except Exception as e:
            print(f"Warning: Could not add metadata: {e}")

        self.report_progress("generation", 100, f"PDF generated: {output_path}")

        return output_path

    def process(self) -> Dict[str, Any]:
        """Execute the full processing pipeline."""
        result = {
            "success": False,
            "output_path": None,
            "input_path": self.config.input_path,
            "error": None,
            "statistics": {}
        }

        try:
            # Validate input
            self.validate_input()
            self.report_progress("validation", 100, "Input validated")

            # Extract
            document = self.extract_pdf()

            # Collect statistics
            total_words = sum(
                len(block.text.split())
                for page in document.pages
                for block in page.text_blocks
            )

            result["statistics"] = {
                "pages": document.num_pages,
                "text_blocks": sum(len(p.text_blocks) for p in document.pages),
                "estimated_words": total_words
            }

            # Generate (with bionic transformation)
            output_path = self.generate_pdf(document)

            result["success"] = True
            result["output_path"] = output_path

            elapsed_time = time.time() - self.start_time
            self.report_progress(
                "complete",
                100,
                f"Processing complete in {elapsed_time:.1f} seconds"
            )

        except Exception as e:
            result["error"] = str(e)
            self.report_progress("error", 0, f"Error: {str(e)}")
            raise

        return result


def process_pdf(
    input_path: str,
    output_path: str,
    emphasis_ratio: float = 0.4,
    min_word_length: int = 3,
    bold_intensity: str = "medium",
    preserve_layout: bool = True
) -> Dict[str, Any]:
    """Convenience function for processing a PDF."""
    config = ProcessingConfig(
        input_path=input_path,
        output_path=output_path,
        emphasis_ratio=emphasis_ratio,
        min_word_length=min_word_length,
        bold_intensity=bold_intensity,
        preserve_layout=preserve_layout
    )

    processor = PDFProcessor(config)
    return processor.process()


def main():
    """Command-line interface for PDF processing."""
    parser = argparse.ArgumentParser(
        description="Process PDF with bionic reading enhancement"
    )

    parser.add_argument(
        "input",
        help="Input PDF file path"
    )
    parser.add_argument(
        "-o", "--output",
        required=True,
        help="Output PDF file path"
    )
    parser.add_argument(
        "-r", "--ratio",
        type=float,
        default=0.4,
        help="Emphasis ratio (0.1-0.7, default: 0.4)"
    )
    parser.add_argument(
        "-m", "--min-length",
        type=int,
        default=3,
        help="Minimum word length to transform (default: 3)"
    )
    parser.add_argument(
        "-i", "--intensity",
        choices=["light", "medium", "heavy"],
        default="medium",
        help="Bold intensity (default: medium)"
    )
    parser.add_argument(
        "--flow-layout",
        action="store_true",
        help="Use flowing text layout instead of preserving original layout"
    )
    parser.add_argument(
        "--extract-images",
        action="store_true",
        help="Extract images (increases processing time)"
    )
    parser.add_argument(
        "--extract-tables",
        action="store_true",
        help="Extract tables (increases processing time)"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output progress as JSON lines"
    )

    args = parser.parse_args()

    config = ProcessingConfig(
        input_path=args.input,
        output_path=args.output,
        emphasis_ratio=args.ratio,
        min_word_length=args.min_length,
        bold_intensity=args.intensity,
        preserve_layout=not args.flow_layout,
        extract_images=args.extract_images,
        extract_tables=args.extract_tables
    )

    processor = PDFProcessor(config)

    if not args.json:
        def progress_callback(progress: ProcessingProgress):
            elapsed = progress.timestamp - processor.start_time
            print(f"[{elapsed:.1f}s] {progress.stage}: {progress.progress:.0f}% - {progress.message}")

        processor.set_progress_callback(progress_callback)

    try:
        result = processor.process()

        if args.json:
            print(json.dumps(result))
        else:
            if result["success"]:
                print(f"\n✅ Success! Output saved to: {result['output_path']}")
                print(f"📊 Statistics: {result['statistics']}")
            else:
                print(f"\n❌ Error: {result['error']}")
                sys.exit(1)

    except Exception as e:
        if args.json:
            print(json.dumps({"success": False, "error": str(e)}))
        else:
            print(f"\n❌ Fatal error: {e}")
            sys.exit(1)


if __name__ == "__main__":
    main()
