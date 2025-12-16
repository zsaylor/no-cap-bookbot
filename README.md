# 📚 No Cap BookBot

> *Book analysis that hits different, no cap fr fr*

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=Streamlit&logoColor=white)](https://streamlit.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![OpenAI](https://img.shields.io/badge/OpenAI-412991?logo=openai&logoColor=white)](https://openai.com)

A modern book analysis web application that transforms classic literature into entertaining Gen Z-style summaries using AI. Upload your favorite books in multiple formats and get summaries that actually make sense to the TikTok generation.

---

## ✨ Features

- 🤖 **AI-Powered Summaries** - Leverages OpenAI's GPT-4o-mini for intelligent text analysis
- 📖 **Multi-Format Support** - Handles EPUB, PDF, and TXT files seamlessly
- 🧩 **Smart Chunking** - Automatically processes large books with intelligent context-aware chunking
- 💬 **Gen Z Translation** - Transforms summaries using authentic Gen Z slang and internet culture
- 📊 **Text Analytics** - Word counts, reading time estimates, and frequency analysis
- 🎨 **Clean UI** - Beautiful, responsive interface built with Streamlit
- ⚡ **Progress Tracking** - Real-time progress indicators for long book processing
- 📚 **Sample Library** - Pre-loaded with classic literature for instant testing

---

## 🎯 What Makes This Special

Traditional book summaries are dry and boring. No Cap BookBot reimagines classic literature through the lens of modern internet culture, making it:

- **Engaging** - Summaries that feel like a conversation with your internet-savvy friend
- **Accessible** - Complex themes explained in relatable, contemporary language
- **Educational** - Demonstrates practical AI/NLP implementation with real-world applications
- **Technically Impressive** - Showcases file processing, API integration, and intelligent text chunking

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/no-cap-bookbot.git
   cd no-cap-bookbot
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   streamlit run main.py
   ```

5. **Open your browser**
   - The app will automatically open at `http://localhost:8501`
   - Enter your OpenAI API key in the sidebar
   - Upload a book or try one of the samples!

---

## 📖 Usage

### Option 1: Upload Your Own Book
1. Click "Choose a file" and select an EPUB, PDF, or TXT file
2. The app will automatically extract and display the text
3. Click "🚀 Analyze This Book" to generate your summary

### Option 2: Try a Sample Book
1. Select a book from the "Sample Books" dropdown in the sidebar
2. The text will populate automatically
3. Click "🚀 Analyze This Book" to see the Gen Z magic

### Option 3: Paste Text Directly
1. Copy any book text you want analyzed
2. Paste it into the text area
3. Click "🚀 Analyze This Book" for instant results

---

## 🛠️ Tech Stack

**Frontend & UI**
- [Streamlit](https://streamlit.io) - Modern web app framework for data/ML applications

**AI & NLP**
- [OpenAI GPT-4o-mini](https://openai.com) - Advanced language model for summarization
- Custom prompting system with comprehensive Gen Z slang dictionary

**File Processing**
- [EbookLib](https://github.com/aerkalov/ebooklib) - EPUB file parsing and text extraction
- [PyMuPDF](https://pymupdf.readthedocs.io/) - High-performance PDF text extraction
- [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/) - HTML parsing and cleaning

**Python Core**
- Type hints for better code quality
- Modular architecture with clear separation of concerns
- Comprehensive docstrings following Google style

---

## 📂 Project Structure

```
no-cap-bookbot/
├── main.py                 # Streamlit app entry point
├── requirements.txt        # Python dependencies
├── LICENSE                 # MIT License
├── README.md              # You are here!
└── src/
    ├── BookSummarizer.py  # AI summarization with intelligent chunking
    ├── extract.py         # Multi-format file text extraction
    ├── stats.py           # Text analysis and statistics
    ├── prompt.py          # Gen Z prompt template and slang dictionary
    └── sample_books.py    # Curated sample book library
```

---

## 🎨 Example Output

**Input:** Romeo and Juliet by William Shakespeare

**Gen Z Summary:**
> *"Okay so Romeo and Juliet is literally the most chaotic love story ever, no cap. These two teens from families that absolutely HATE each other meet at a party and it's giving main character energy immediately. They fall so hard they literally get married the next day (red flag much?). But then everything goes sideways when Romeo's bestie dies and Romeo catches a body in revenge, so now he's banished. Juliet's fam tries to force her into marrying some other guy, so she fakes her own death with this sus potion. The plan was lowkey genius but the message never reaches Romeo, and when he finds her 'dead' he literally unalives himself. Then Juliet wakes up, sees Romeo dead, and does the same thing. The families finally realize they're the problem but like... too late bestie. This story lives rent-free in my head as the ultimate example of when family drama goes too far, periodt."*

---

## 🔧 Configuration

### Chunking Parameters

For very large books, the app uses intelligent chunking. You can adjust these in `src/BookSummarizer.py`:

```python
self.chunk_size = 100000      # Words per chunk
self.overlap_size = 1000      # Word overlap for context continuity
```

### API Settings

The app uses GPT-4o-mini by default for cost efficiency. To change the model, edit `src/BookSummarizer.py`:

```python
model="gpt-4o-mini"  # Change to "gpt-4" for higher quality
```

---

## 💡 How It Works

1. **File Upload & Text Extraction**
   - Detects file type and routes to appropriate parser
   - EPUB: Uses temporary file approach for ZIP archive access
   - PDF: Streams bytes directly to PyMuPDF
   - TXT: Handles UTF-8 with Latin-1 fallback

2. **Smart Text Processing**
   - Books under 100k words: Direct summarization
   - Large books: Intelligent chunking with overlap for context
   - Each chunk gets positional context (beginning/middle/end)

3. **Multi-Stage Summarization**
   - Stage 1: Summarize each chunk individually
   - Stage 2: Combine chunk summaries into master narrative
   - Stage 3: Transform into Gen Z style using custom prompt

4. **Results Display**
   - Gen Z summary with authentic slang
   - Word count and reading time estimate
   - Top 5 most common meaningful words
   - Social sharing encouragement

---

## 🤝 Contributing

Contributions are welcome! This project is perfect for:
- Adding support for more file formats (MOBI, AZW, etc.)
- Implementing caching to reduce API costs
- Creating additional summary styles (Shakespearean, Academic, etc.)
- Adding sentiment analysis or theme extraction
- Improving the UI/UX with custom CSS

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙋‍♂️ Author

**Zachary Saylor**

This project demonstrates:
- Full-stack web development with Python
- AI/ML integration with modern LLMs
- Multi-format file processing
- Clean code architecture and documentation
- User-centric design thinking

---

## 🌟 Acknowledgments

- OpenAI for providing the GPT API
- The Streamlit team for an amazing framework
- All the Gen Z consultants (TikTok) who helped with the slang dictionary
- Classic literature authors whose works deserve modern retellings

---

## 📬 Contact

Questions? Feedback? Job offers? 😊

Feel free to open an issue or reach out!

---

<div align="center">

**Made with ❤️ and way too much caffeine**

*This bot is absolutely sending me* ☕

</div>
