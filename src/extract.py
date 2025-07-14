import os
from enum import Enum
from io import StringIO
import streamlit as st
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import pdfplumber

def extract_text_from_upload(uploaded_file):
    """Extracts book text based on the uploaded file type."""

    if uploaded_file is None:
        return None

    FileType = Enum("FileType", ["EPUB", "PDF", "TXT"])
    supported_file_types = {
        ".epub": FileType.EPUB,
        ".pdf": FileType.PDF,
        ".txt": FileType.TXT
    }

    try:
        extension = os.path.splitext(uploaded_file.name)[1].lower()

        if extension not in supported_file_types:
            st.error(f"❌ Unsupported file type: '{extension}'")
            st.info("📄 Supported formats: " + ", ".join(supported_file_types.keys()))
            return None

        uploaded_file_type = supported_file_types[extension]
        match uploaded_file_type:
            case FileType.EPUB:
                extract_text_from_epub(uploaded_file)
            case FileType.PDF:
                extract_text_from_pdf(uploaded_file)
            case FileType.TXT:
                extract_text_from_txt(uploaded_file)
            case _:
                return None

    except Exception as e:
        st.error(f"❌ Error processing file: {str(e)}")
        return None

def extract_text_from_epub(uploaded_file):
    try:
        uploaded_file.seek(0)
        book = epub.read_epub(uploaded_file)

        text = ""
        for item in book.get_items():
            if item.get_type() == ebooklib.ITEM_DOCUMENT:
                # Parse HTML content
                soup = BeautifulSoup(item.get_content(), 'html.parser')
                # Remove script and style elements
                for script in soup(["script", "style"]):
                    script.decompose()
                text += soup.get_text() + "\n"

        return text if text.strip() else None

    except Exception as e:
        st.error(f"❌ Error processing EPUB file: {str(e)}")
        return None

def extract_text_from_pdf(uploaded_file):
    try:
        uploaded_file.seek(0)

        text = ""
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"

        return text if text.strip() else None

    except Exception as e:
        st.error(f"❌ Error processing PDF file: {str(e)}")
        return None

def extract_text_from_txt(uploaded_file):
    try:
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        return stringio.read()
    except UnicodeDecodeError:
        try:
            stringio = StringIO(uploaded_file.getvalue().decode("latin-1"))
            return stringio.read()
        except Exception:
            raise
    except Exception as e:
        st.error(f"❌ Error processing TXT file: {str(e)}")
        return None

