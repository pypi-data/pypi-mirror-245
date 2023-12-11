from setuptools import setup, find_packages

setup(
    name="NT_TextFileLoader",
    version="1.1.8",
    description ='''Python library to extract text from various file formats. the supported file formats are "JPG","JPEG","PNG","PDF","DOCX","DOC" and "TEXT".''',
    readme = "README.md",
    author="Vishnu.D",
    author_email="vishnu.d@narmtech.com",
    license="MIT",
    keywords =["text extractor", "text loader", "load text file", "read text from pdf", "load text from DOC","load text from DOCX", "read text from images","pip install nt-textfileloader"],
    packages=find_packages(),
    install_requires=[
            "PyPDF2",
            "python-docx",
            "docx2txt",
            "Pillow",
            "pytesseract",
            "langchain",
            "unstructured",
        ],


    classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3.9',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.11',
  ]
)