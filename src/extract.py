"""
Text extraction module for No Cap BookBot.

This module handles extracting text content from various file formats including
EPUB, PDF, and TXT files uploaded through the Streamlit interface.
"""

import os
import tempfile
from enum import Enum
from io import BytesIO

import ebooklib
import pymupdf
import streamlit as st
from bs4 import BeautifulSoup
from ebooklib import epub


def extract_text_from_upload(uploaded_file) -> str | None:
    """
    Extract text content from an uploaded file.

    Automatically detects the file type based on extension and routes to the
    appropriate extraction function. Supports EPUB, PDF, and TXT formats.

    Args:
        uploaded_file: Streamlit UploadedFile object containing the file data.

    Returns:
        str: Extracted text content, or None if extraction fails or file is invalid.
    """
    if uploaded_file is None:
        return None

    FileType = Enum("FileType", ["EPUB", "PDF", "TXT"])
    supported_file_types = {
        ".epub": FileType.EPUB,
        ".pdf": FileType.PDF,
        ".txt": FileType.TXT,
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
                return extract_text_from_epub(uploaded_file)
            case FileType.PDF:
                return extract_text_from_pdf(uploaded_file)
            case FileType.TXT:
                return extract_text_from_txt(uploaded_file)
            case _:
                return None

    except Exception as e:
        st.error(f"❌ Error processing file: {str(e)}")
        return None


def extract_text_from_epub(uploaded_file) -> str | None:
    """
    Extract text content from an EPUB file.

    EPUB files are ZIP archives internally, so this function writes the uploaded
    file to a temporary location for ebooklib to process, then extracts all text
    from document items while removing script and style tags.

    Args:
        uploaded_file: Streamlit UploadedFile object containing EPUB data.

    Returns:
        str: Extracted and cleaned text content, or None if extraction fails.
    """
    tmp_file_path = None
    try:
        # Write uploaded file to a temporary file
        # EPUB files are ZIP archives and ebooklib needs filesystem access
        with tempfile.NamedTemporaryFile(delete=False, suffix=".epub") as tmp_file:
            uploaded_file.seek(0)
            tmp_file.write(uploaded_file.read())
            tmp_file_path = tmp_file.name

        # Read from the temporary file path
        book = epub.read_epub(tmp_file_path)
        
        text = ""
        for item in book.get_items():
            if item.get_type() == ebooklib.ITEM_DOCUMENT:
                soup = BeautifulSoup(item.get_content(), "html.parser")
                for script in soup(["script", "style"]):
                    script.decompose()
                text += soup.get_text() + "\n"
        
        return text if text.strip() else None

    except Exception as e:
        st.error(f"❌ Error processing EPUB file: {str(e)}")
        return None
    
    finally:
        # Clean up the temporary file
        if tmp_file_path and os.path.exists(tmp_file_path):
            try:
                os.unlink(tmp_file_path)
            except Exception:
                pass  # Ignore cleanup errors


def extract_text_from_pdf(uploaded_file) -> str | None:
    """
    Extract text content from a PDF file.

    Uses PyMuPDF to extract text from all pages of the PDF document.

    Args:
        uploaded_file: Streamlit UploadedFile object containing PDF data.

    Returns:
        str: Extracted text content from all pages, or None if extraction fails.
    """
    try:
        uploaded_file.seek(0)
        doc = pymupdf.open(stream=uploaded_file.read(), filetype="pdf")
        text = "".join(page.get_text() for page in doc.pages())
        doc.close()
        return text if text.strip() else None

    except Exception as e:
        st.error(f"❌ Error processing PDF file: {str(e)}")
        return None


def extract_text_from_txt(uploaded_file) -> str | None:
    """
    Extract text content from a plain text file.

    Attempts to decode the file using UTF-8, falling back to Latin-1 if needed.

    Args:
        uploaded_file: Streamlit UploadedFile object containing text data.

    Returns:
        str: Decoded text content, or None if extraction fails.
    """
    try:
        content = uploaded_file.getvalue().decode("utf-8")
    except UnicodeDecodeError:
        content = uploaded_file.getvalue().decode("latin-1")
    except Exception as e:
        st.error(f"❌ Error processing TXT file: {str(e)}")
        return None

    return content if content.strip() else None
