import streamlit as st
from src import stats
from src import extract
from src import nocap

# Streamlit page configuration
st.set_page_config(
    page_title="No Cap BookBot 📚",
    page_icon="📚",
    layout="wide",
    menu_items={"About": "The book bot that understood the assignment: making classic literature slap harder than your morning coffee, periodt. 💅📚✨"}
)

def main():
    # Header
    st.title("📚 No Cap BookBot")
    st.subheader("*Book analysis that hits different, no cap fr fr*")

    # Sidebar
    st.sidebar.header("🔑 Setup")
    api_key = st.sidebar.text_input(
        "OpenAI API Key", 
        type="password",
        help="Get your API key from https://platform.openai.com/api-keys"
    )

    # TODO: allow search on public domain book website like project gutenburg or similar
    st.sidebar.header("📖 Try a Sample")
    sample_books = {
        "Choose a sample...": "",
        "Romeo and Juliet (Short)": """Romeo and Juliet is a tragedy written by William Shakespeare. 
        Two young star-crossed lovers whose deaths ultimately reconcile their feuding families. 
        Romeo Montague and Juliet Capulet fall in love at first sight at a Capulet party. 
        They secretly marry the next day. Romeo kills Juliet's cousin Tybalt in a duel and is banished. 
        Juliet's parents arrange her marriage to Paris. To avoid this, she takes a potion to fake her death. 
        Romeo, believing she is truly dead, drinks poison. Juliet awakens, finds Romeo dead, and kills herself with his dagger.""",

        "The Great Gatsby (Short)": """The Great Gatsby by F. Scott Fitzgerald is set in 1922. 
        Nick Carraway moves to West Egg and becomes neighbors with the mysterious Jay Gatsby. 
        Gatsby throws lavish parties hoping to attract Daisy Buchanan, his lost love who is now married to Tom. 
        Gatsby and Daisy have an affair. Tom is also having an affair with Myrtle Wilson. 
        Daisy drives Gatsby's car and kills Myrtle in an accident. Myrtle's husband shoots Gatsby, thinking he was the driver. 
        The novel explores themes of the American Dream, wealth, and moral decay in the Jazz Age."""
    }

    selected_sample = st.sidebar.selectbox("Sample Books", list(sample_books.keys()))

    # Main content area
    col1, col2 = st.columns([1, 1])

    # TODO: figure out suitable upload size limit
    # Upload/text box section
    with col1:
        st.header("📤 Upload Your Book")
        uploaded_file = st.file_uploader(
            "Choose a text file", 
            type=['epub', 'pdf', 'txt'],
            help="Upload an .epub, .pdf, or .txt file of any book you want analyzed!"
        )

        book_text = ""
        if selected_sample != "Choose a sample...":
            book_text = sample_books[selected_sample]

        book_text = st.text_area(
            "Or paste/edit text here:", 
            value=book_text,
            height=225,
            help="Paste some bussin book text here or use a fire sample from the sidebar."
        )

    # Analysis section
    with col2:
        st.header("📊 Analysis Results")

        final_text = ""
        if uploaded_file is not None:
            uploaded_text = extract.extract_text_from_upload(uploaded_file)
            if uploaded_text:
                final_text = uploaded_text
                st.success(f"✅ File uploaded! GG! ({len(uploaded_text.split())} words)")
            else:
                st.error("❌ Could not read the file. Make sure it's a valid text file, or we're so cooked.")
        elif book_text.strip():
            final_text = book_text

        if st.button("🚀 Analyze This Book", type="primary"):
            if not final_text.strip():
                st.error("❌ Sus... Please upload a file or paste some text first, bestie!")
            elif not api_key:
                st.error("❌ Yikes, please add your OpenAI API key in the sidebar!")
            else:
                with st.spinner("Say less, let me cook... 👨🏻‍🍳🔥"):

                    # Summary section
                    genz_summary = nocap.get_genz_summary(final_text, api_key)
                    st.success("✨ Analysis complete! Here's the tea:")
                    st.subheader("🎭 Gen Z Summary")
                    st.markdown(f"*{genz_summary}*")

                    # Stats section
                    word_count = stats.get_word_count(final_text)
                    char_count = stats.get_char_count(final_text)
                    char_count_list = stats.get_sorted_char_count(char_count)
                    st.subheader("📈 Basic Stats")

                    stats_col1, stats_col2 = st.columns(2)
                    with stats_col1:
                        st.metric("📝 Total Words", f"{word_count:,}")
                        st.metric("🔤 Total Characters", f"{len(final_text):,}")

                    with stats_col2:
                        st.metric("📚 Estimated Reading Time", f"{word_count // 200} minutes")
                        st.metric("📄 Estimated Pages", f"{word_count // 250}")

                    # TODO: change to whole word instead of char
                    # Character frequency section
                    st.subheader("🔤 Most Common Letters")
                    st.markdown(stats.format_char_count(char_count_list))

                    # Share section
                    st.subheader("📱 Share This Banger Analysis")
                    st.info("Screenshot this analysis and share it on social media! Don't forget to tag #NoCapBookBot 📚✨")

    # Footer
    st.markdown("---")
    st.markdown("*Made with ❤️ and way too much caffeine. This bot is absolutely sending me.* ☕")
    st.markdown("**How to use:** Upload a file (or use a sample from the side bar), add your OpenAI API key, and smash that analyze button!")

if __name__ == "__main__":
    main()
