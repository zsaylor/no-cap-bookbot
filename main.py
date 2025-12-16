"""
No Cap BookBot - Main Streamlit Application

A book analysis tool that generates entertaining Gen Z-style summaries of classic
and contemporary literature using OpenAI's GPT models. Upload EPUB, PDF, or TXT
files to get summaries that actually hit different.
"""

import streamlit as st

import src.extract as extract
import src.stats as stats
from src.BookSummarizer import BookSummarizer
from src.prompt import GENZ_PROMPT
from src.sample_books import sample_books

st.set_page_config(
    page_title="No Cap BookBot 📚",
    page_icon="📚",
    layout="wide",
    menu_items={
        "About": "The book bot that understood the assignment: making classic literature slap harder than your morning coffee, periodt. 💅📚✨"
    },
)


def summarize(book_text: str, api_key: str, genz_prompt: str) -> str:
    """
    Generate a Gen Z-style summary of a book using AI.

    Args:
        book_text: The complete text of the book to summarize.
        api_key: OpenAI API key for authentication.
        genz_prompt: Custom prompt defining the Gen Z transformation style.

    Returns:
        str: The Gen Z-style summary of the book.
    """
    summarizer = BookSummarizer(api_key)
    return summarizer.process_book(book_text, genz_prompt)


def main():
    """
    Main application entry point.

    Sets up the Streamlit UI with file upload, text input, API key configuration,
    and displays analysis results including Gen Z summaries and text statistics.
    """
    # Header
    st.title("📚 No Cap BookBot")
    st.subheader("*Book analysis that hits different, no cap fr fr*")

    # Sidebar
    st.sidebar.header("🔑 Setup")
    api_key = st.sidebar.text_input(
        "OpenAI API Key",
        type="password",
        help="Get your API key from https://platform.openai.com/api-keys",
    )

    st.sidebar.header("📖 Try a Sample")
    selected_sample = st.sidebar.selectbox("Sample Books", list(sample_books.keys()))

    # Main content area
    col1, col2 = st.columns([1, 1])

    # Upload/text box section
    with col1:
        st.header("📤 Upload Your Book")
        uploaded_file = st.file_uploader(
            "Choose a text file",
            type=["epub", "pdf", "txt"],
            help="Upload an .epub, .pdf, or .txt file of any book you want analyzed!",
        )

        book_text = ""
        if selected_sample != "Choose a sample...":
            book_text = sample_books[selected_sample]

        book_text = st.text_area(
            "Or paste/edit text here:",
            value=book_text,
            height=225,
            help="Paste some bussin book text here or use a fire sample from the sidebar.",
        )

    # Analysis section
    with col2:
        st.header("📊 Analysis Results")

        final_text = ""
        if uploaded_file is not None:
            uploaded_text = extract.extract_text_from_upload(uploaded_file)
            if uploaded_text:
                final_text = uploaded_text
                st.success(
                    f"✅ File uploaded! GG! ({len(uploaded_text.split())} words)"
                )
            else:
                st.error(
                    "❌ Could not read the file. Make sure it's a valid text file, or we're so cooked."
                )
        elif book_text.strip():
            final_text = book_text

        if st.button("🚀 Analyze This Book", type="primary"):
            if not final_text.strip():
                st.error(
                    "❌ Sus... Please upload a file or paste some text first, bestie!"
                )
            elif not api_key:
                st.error("❌ Yikes, please add your OpenAI API key in the sidebar!")
            else:
                with st.spinner("Say less, let me cook... 👨🏻‍🍳🔥"):
                    # Summary section
                    genz_summary = summarize(final_text, api_key, GENZ_PROMPT)
                    st.success("✨ Analysis complete! Here's the tea:")
                    st.subheader("🎭 Gen Z Summary")
                    st.markdown(f"*{genz_summary}*")

                    # Stats section
                    word_count = stats.get_word_count(final_text)
                    st.subheader("📈 Basic Stats")

                    stats_col1, stats_col2 = st.columns(2)
                    with stats_col1:
                        st.metric("📝 Total Words", f"{word_count:,}")

                    with stats_col2:
                        st.metric(
                            "📚 Estimated Reading Time", f"{word_count // 200} minutes"
                        )

                    # Word frequency section
                    st.subheader("🔤 Most Common Words")
                    st.markdown(stats.get_common_words(final_text))

                    # Share section
                    st.subheader("📱 Share This Banger Analysis")
                    st.info(
                        "Screenshot this analysis and share it on social media! Don't forget to tag #NoCapBookBot 📚✨"
                    )

    # Footer
    st.markdown("---")
    st.markdown(
        "*Made with ❤️ and way too much caffeine. This bot is absolutely sending me.* ☕"
    )
    st.markdown(
        "**How to use:** Upload a file (or use a sample from the side bar), add your OpenAI API key, and smash that analyze button!"
    )


if __name__ == "__main__":
    main()
