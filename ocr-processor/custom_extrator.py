#!/usr/bin/env python3
"""
Transaction Parser for OCR Text Files
Parses raw OCR text files and extracts structured transaction records.
Creates a separate structured file for each raw text file.
"""

import re
import sys
from pathlib import Path


def extract_transactions(full_text):
    """
    Parse the OCR text and extract individual transactions.
    Each transaction typically has: date, description, and amount.
    
    Args:
        full_text: Raw text from OCR
        
    Returns:
        List of transaction strings
    """
    transactions = []
    lines = full_text.strip().split('\n')
    
    # Pattern to detect dates (DD/MM/YY or DD/MM/YYYY or variations)
    date_pattern = r'\b\d{1,2}[\/\-\.]\s*\d{1,2}[\/\-\.]\s*\d{2,4}\b'
    
    transaction_lines = []
    header_lines = []
    in_transactions = False
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Check if line contains a date (likely start of new transaction)
        date_match = re.search(date_pattern, line)
        
        if date_match:
            in_transactions = True
            
            # Save previous transaction if exists
            if transaction_lines:
                transactions.append('\n'.join(transaction_lines))
                transaction_lines = []
            
            # Start new transaction
            transaction_lines.append(line)
        elif in_transactions and transaction_lines:
            # Continue current transaction - check if it looks like part of same entry
            # Lines with numbers/amounts or descriptions likely belong to current transaction
            if re.search(r'[\d:,]+', line) or len(line) > 5:
                transaction_lines.append(line)
            else:
                # Might be start of description-only line
                transaction_lines.append(line)
        elif not in_transactions:
            # Header lines (before first transaction)
            header_lines.append(line)
    
    # Don't forget the last transaction
    if transaction_lines:
        transactions.append('\n'.join(transaction_lines))
    
    # Prepare output with header
    output_parts = []
    if header_lines:
        output_parts.append("=== HEADER ===")
        output_parts.append('\n'.join(header_lines))
        output_parts.append("")
    
    if transactions:
        output_parts.append("=== TRANSACTIONS ===")
        output_parts.append("")
        for i, transaction in enumerate(transactions, 1):
            output_parts.append(f"--- Transaction {i} ---")
            output_parts.append(transaction)
            output_parts.append("")
    
    return '\n'.join(output_parts)


def process_text_file(text_path, output_dir):
    """
    Process a single text file and create structured output.
    
    Args:
        text_path: Path to the raw text file
        output_dir: Directory to save the structured output
    """
    try:
        # Read the raw text file
        with open(text_path, 'r', encoding='utf-8') as f:
            raw_text = f.read()
        
        # Extract and format transactions
        structured_text = extract_transactions(raw_text)
        
        # Create output filename with _structured suffix
        file_stem = Path(text_path).stem
        output_path = Path(output_dir) / f"{file_stem}_structured.txt"
        
        # Save structured output
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(structured_text)
        
        print(f"✓ Parsed: {Path(text_path).name} -> {output_path.name}")
        return True
        
    except Exception as e:
        print(f"✗ Error processing {Path(text_path).name}: {str(e)}")
        return False


def main():
    """Main function to process all text files in the output directory."""
    
    # Configuration
    INPUT_DIR = "./text"
    OUTPUT_DIR = "./text/structured"  # Save structured files in same directory
    
    # Check if directory exists
    if not Path(INPUT_DIR).exists():
        print(f"Error: Directory '{INPUT_DIR}' does not exist.")
        print(f"Please run handwriting_ocr.py first to generate text files.")
        sys.exit(1)
    
    # Get all .txt files (but not _structured ones to avoid reprocessing)
    text_files = [
        f for f in Path(INPUT_DIR).iterdir()
        if f.is_file() and f.suffix == '.txt'
    ]
    
    if not text_files:
        print(f"No text files found in '{INPUT_DIR}' directory.")
        print(f"Please run handwriting_ocr.py first.")
        sys.exit(1)
    
    print(f"Found {len(text_files)} text file(s) to parse.")
    print(f"Structured output will be saved to '{OUTPUT_DIR}' directory.\n")
    
    # Process each text file
    successful = 0
    failed = 0
    
    for text_path in sorted(text_files):
        if process_text_file(text_path, OUTPUT_DIR):
            successful += 1
        else:
            failed += 1
    
    # Print summary
    print(f"\n{'='*50}")
    print(f"Parsing Complete!")
    print(f"Successfully parsed: {successful}")
    print(f"Failed: {failed}")
    print(f"Structured files saved to: {OUTPUT_DIR}/")
    print(f"{'='*50}")


if __name__ == "__main__":
    main()