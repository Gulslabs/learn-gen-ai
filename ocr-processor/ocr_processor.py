#!/usr/bin/env python3
"""
Handwriting OCR Script for Apartment Maintenance Expenses
Uses Google Cloud Vision API's DOCUMENT_TEXT_DETECTION feature
to extract handwritten text from images and save to text files.
"""

import os
import sys
from pathlib import Path
from google.cloud import vision


def process_image(client, image_path, output_dir):
    """
    Process a single image and extract handwritten text.
    
    Args:
        client: Google Cloud Vision ImageAnnotatorClient
        image_path: Path to the input image
        output_dir: Directory to save the output text file
    """
    try:
        # Read the image file
        with open(image_path, 'rb') as image_file:
            content = image_file.read()

        # Create image object
        image = vision.Image(content=content)

        # Perform document text detection
        response = client.document_text_detection(image=image)

        # Check for errors
        if response.error.message:
            raise Exception(f'{response.error.message}')

        # Extract full text
        full_text = response.full_text_annotation.text

        # Create output filename (same name as input, but .txt extension)
        image_name = Path(image_path).stem
        output_path = Path(output_dir) / f"{image_name}.txt"

        # Save to text file
        with open(output_path, 'w', encoding='utf-8') as text_file:
            text_file.write(full_text)

        print(f"✓ Processed: {Path(image_path).name} -> {output_path.name}")
        return True

    except Exception as e:
        print(f"✗ Error processing {Path(image_path).name}: {str(e)}")
        return False


def main():
    """Main function to process all images in the input directory."""
    
    # Configuration
    INPUT_DIR = "./images"
    OUTPUT_DIR = "./text"
    
    # Supported image formats
    SUPPORTED_FORMATS = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.tif'}

    # Create output directory if it doesn't exist
    Path(OUTPUT_DIR).mkdir(exist_ok=True)

    # Check if input directory exists
    if not Path(INPUT_DIR).exists():
        print(f"Error: Input directory '{INPUT_DIR}' does not exist.")
        print(f"Please create it and add your images.")
        sys.exit(1)

    # Get all image files from input directory
    image_files = [
        f for f in Path(INPUT_DIR).iterdir()
        if f.is_file() and f.suffix.lower() in SUPPORTED_FORMATS
    ]

    if not image_files:
        print(f"No images found in '{INPUT_DIR}' directory.")
        print(f"Supported formats: {', '.join(SUPPORTED_FORMATS)}")
        sys.exit(1)

    print(f"Found {len(image_files)} image(s) to process.")
    print(f"Output will be saved to '{OUTPUT_DIR}' directory.\n")

    # Initialize Google Cloud Vision client
    try:
        client = vision.ImageAnnotatorClient()
    except Exception as e:
        print(f"Error initializing Google Cloud Vision client: {str(e)}")
        print("Make sure you have set up authentication correctly.")
        sys.exit(1)

    # Process each image
    successful = 0
    failed = 0

    for image_path in sorted(image_files):
        if process_image(client, str(image_path), OUTPUT_DIR):
            successful += 1
        else:
            failed += 1

    # Print summary
    print(f"\n{'='*50}")
    print(f"Processing Complete!")
    print(f"Successfully processed: {successful}")
    print(f"Failed: {failed}")
    print(f"Output saved to: {OUTPUT_DIR}/")
    print(f"{'='*50}")


if __name__ == "__main__":
    main()