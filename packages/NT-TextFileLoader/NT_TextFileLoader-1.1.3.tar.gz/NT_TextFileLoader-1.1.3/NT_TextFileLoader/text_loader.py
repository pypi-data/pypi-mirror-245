"""
Module for loading text from different file types.
"""

import PyPDF2
import docx
from PIL import Image
import pytesseract
import tempfile
from langchain.document_loaders import UnstructuredWordDocumentLoader

class TextFileLoader:
    """
    Class for loading text from various file types.
    """

    @staticmethod
    def load_text(file_path):

        """
        Load text from different file types.

        Args:
        - file_path (str): Path to the file to be loaded.

        Returns:
        - str: Extracted text from the file.
        """

        try:
            file_type = file_path.split(".")[-1]

            if file_type == 'pdf':
                return TextFileLoader.load_pdf(file_path)
            elif file_type == 'docx':
                return TextFileLoader.load_docx(file_path)
            elif file_type == 'doc':
                return TextFileLoader.load_doc(file_path)
            elif file_type == 'txt':
                return TextFileLoader.load_text_file(file_path)
            elif file_type.lower() in (("jpg,png,jpeg,webp")):
                return TextFileLoader.load_image(file_path)
            else:
                return "File type not supported"
        except Exception as e:
            return f"Error loading file: {str(e)}"

    @staticmethod
    def load_pdf(file_path):

        """
        Load text from a PDF file.

        Args:
        - file_path (str): Path to the PDF file.

        Returns:
        - str: Extracted text from the PDF.
        """
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ''
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    text += page.extract_text()

                # Check if extracted text has enough length
                if len(text) >= 50:
                    return text
                else:
                    # Attempt image extraction and OCR if text length is insufficient
                    with tempfile.TemporaryDirectory() as temp_dir:
                        images = []
                        # Convert PDF pages to images
                        for page_num in range(len(pdf_reader.pages)):
                            page = pdf_reader.getPage(page_num)
                            img = Image.open(page)
                            img_path = f"{temp_dir}/page_{page_num + 1}.png"
                            img.save(img_path, 'PNG')
                            images.append(img_path)

                        # Use OCR to extract text from images
                        extracted_text = ''
                        for img_path in images:
                            image = Image.open(img_path)
                            ocr_text = pytesseract.image_to_string(image)
                            extracted_text += ocr_text + '\n'

                        return extracted_text.strip() if extracted_text else "No text found in the PDF"
        except Exception as e:
            return f"Error loading PDF or extracting text: {str(e)}"

    @staticmethod
    def load_docx(file_path):

        """
        Load text from a DOCX file.

        Args:
        - file_path (str): Path to the DOCX file.

        Returns:
        - str: Extracted text from the DOCX.
        """

        try:
            doc = docx.Document(file_path)
            text = ''
            for para in doc.paragraphs:
                text += para.text
            return text
        except Exception as e:
            return f"Error loading DOCX: {str(e)}"

    @staticmethod
    def load_doc(file_path):
      
        """
        Load text from a DOC file.

        Args:
        - file_path (str): Path to the DOC file.

        Returns:
        - str: Extracted text from the DOC.
        """

        try:
            loader = UnstructuredWordDocumentLoader(file_path)
            data = loader.load()
            text = ""
            for i in range(len(data)):
                text=text+"\n"+data[i].page_content
            return text.strip()
        except Exception as e:
            return f"Error loading DOC: {str(e)}"

    @staticmethod
    def load_text_file(file_path):
        try:
            with open(file_path, 'r') as file:
                text = file.read()
            return text
        except Exception as e:
            return f"Error loading text file: {str(e)}"

    @staticmethod
    def load_image(file_path):

        """
        Load text from a text file.

        Args:
        - file_path (str): Path to the text file.

        Returns:
        - str: Extracted text from the text file.
        """

        try:
            image = Image.open(file_path)
            text = pytesseract.image_to_string(image)
            return text.strip() if text else "No text found in the image"
        except Exception as e:
            return f"Error loading image or extracting text: {str(e)}"