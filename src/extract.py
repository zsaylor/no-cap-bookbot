import os
from enum import Enum
import streamlit as st
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import pymupdf
from io import BytesIO

def extract_text_from_upload(uploaded_file) -> str | None:
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
    try:
        uploaded_file.seek(0)
        epub_bytes = BytesIO(uploaded_file.read())

        book = epub.read_epub(epub_bytes)
        text = ""
        for item in book.get_items():
            if item.get_type() == ebooklib.ITEM_DOCUMENT:
                soup = BeautifulSoup(item.get_content(), 'html.parser')
                for script in soup(["script", "style"]):
                    script.decompose()
                text += soup.get_text() + "\n"
        return text if text.strip() else None

    except Exception as e:
        st.error(f"❌ Error processing EPUB file: {str(e)}")
        return None

def extract_text_from_pdf(uploaded_file) -> str | None:
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
    try:
        content = uploaded_file.getvalue().decode("utf-8")
    except UnicodeDecodeError:
        content = uploaded_file.getvalue().decode("latin-1")
    except Exception as e:
        st.error(f"❌ Error processing TXT file: {str(e)}")
        return None

    return content if content.strip() else None

