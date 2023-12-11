# NT-TextLoader

[![N|Solid](https://narmtech.com/img/companylogo.png)](https://nodesource.com/products/nsolid)

A Python module for extracting text content from various file types including PDFs, DOCX, DOC, text files, and images using Optical Character Recognition (OCR).


### Installation Instructions

Before using this package, ensure you have installed the following system-level dependencies:

- Tesseract OCR:
  ```bash
  !apt install tesseract-ocr
  !apt install libtesseract-dev
  !apt-get --no-install-recommends install libreoffice -y
  !apt-get install -y libreoffice-java-common



## Installation

Install the package using pip:

```bash
pip install NT-TextLoader
```

## Usage

```python
from NT_TextLoader import TextFileLoader

# Load text from a file
file_path = 'path/to/your/file'
extracted_text = TextFileLoader.load_text(file_path)
print(extracted_text)
```

## Supported File Types

- **PDF**: Extracts text from PDF files.
- **DOCX**: Extracts text from DOCX files.
- **DOC**: Extracts text from legacy DOC files.
- **Text files**: Loads text content from TXT files.
- **Images (JPG, PNG, JPEG, WEBP)**: Uses OCR to extract text from images.

## Requirements

- PyPDF2
- python-docx
- Pillow
- pytesseract (For image-based text extraction)
- langchain 

## Contributions

Contributions, issues, and feature requests are welcome!

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
