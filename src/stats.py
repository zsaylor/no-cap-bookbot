"""
Text statistics module for No Cap BookBot.

Provides functions for analyzing book text, including word counts and
identifying the most frequently used words (excluding common stop words).
"""

import re
from collections import Counter

def get_word_count(book_text: str) -> int:
    """
    Count the total number of words in the given text.

    Args:
        book_text: The text to analyze.

    Returns:
        int: The total word count.
    """
    words = book_text.split()
    return len(words)

def get_common_words(book_text: str) -> str:
    """
    Identify and format the 5 most common meaningful words in the text.

    Filters out common stop words and returns a formatted string showing
    the top 5 words with their occurrence counts.

    Args:
        book_text: The text to analyze.

    Returns:
        str: Formatted markdown string listing the top 5 words and counts,
             or an error message if no valid words are found.
    """
    stop_words = {
        'the', 'a', 'an', 'and', 'is', 'in', 'it', 'of', 'for', 'on',
        'with', 'as', 'at', 'by', 'to', 'was', 'were', 'be', 'are',
        'i', 'you', 'he', 'she', 'they', 'we', 'my', 'your', 'his',
        'her', 'their', 'our', 'this', 'that', 'what', 'which', 'who'
    }

    lower_case_book = book_text.lower()
    words = re.findall(r'\b\w+\b', lower_case_book)
    filtered_words = [word for word in words if word not in stop_words and len(word) > 1]
    word_counts = Counter(filtered_words)

    sorted_words = sorted(word_counts.items(), key=lambda x: (-x[1], x[0]))
    top_5_words = sorted_words[:5]
    if not top_5_words:
        return "Oops fam, looks like I'm cappin'."

    formatted_lines = []
    for i, (word, count) in enumerate(top_5_words, 1):
        formatted_lines.append(f"{i}. **{word}**: {count}")
    return "\n".join(formatted_lines)

