import re
from collections import Counter

def get_word_count(book_text: str) -> int:
    words = book_text.split()
    return len(words)

def get_common_words(book_text: str) -> str:
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

