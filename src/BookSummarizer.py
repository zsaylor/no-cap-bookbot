import openai
from typing import List

class BookSummarizer:
    def __init__(self, api_key: str):
        self.client = openai.OpenAI(api_key=api_key)
        self.chunk_size = 100000
        self.overlap_size = 1000
        self.max_output_tokens_per_chunk = 1000
        self.final_summary_max_tokens = 500

    def model_response(self, prompt: str, max_tokens: int, temperature: float) -> str:
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=temperature
            )
            return response.choices[0].message.content.strip()

        except Exception as e:
            return f"Oops fam, the AI summary failed: {str(e)}"

    def create_chunks(self, words: List[str]) -> List[str]:
        chunks = []
        start = 0
        while start < len(words):
            end = min(start + self.chunk_size, len(words))
            chunk_text = ' '.join(words[start:end])
            chunks.append(chunk_text)

            if end >= len(words):
                break

            start += self.chunk_size - self.overlap_size

        return chunks

    def summarize_chunk(self, chunk: str, chunk_number: int, total_chunks: int) -> str:
        position_context = ""
        if chunk_number == 1:
            position_context = "This is the beginning of the book."
        elif chunk_number == total_chunks:
            position_context = "This is the end of the book."
        else:
            position_context = f"This is part {chunk_number} of {total_chunks} of the book."

        chunk_prompt = f"""
        {position_context} Provide a detailed summary of this section of the book. 

        Focus on:
        - Key plot points and story developments
        - Important character introductions, developments, or changes
        - Major themes or conflicts
        - Setting details if relevant
        - Any resolution or cliffhangers

        Keep the summary comprehensive but concise.

        Text section:
        {chunk}
        """

        return self.model_response(chunk_prompt, self.max_output_tokens_per_chunk, 0.3)

    def create_master_summary(self, chunk_summaries: List[str]) -> str:
        combined_summaries = "\n\n".join([f"Section {i+1}: {summary}" for i, summary in enumerate(chunk_summaries)])

        master_prompt = f"""
        Below are summaries of different sections of a book. Create a comprehensive, 
        cohesive summary that captures the complete story arc, main characters, 
        key themes, and plot resolution.

        Focus on:
        - Overall plot progression from beginning to end
        - Character development arcs
        - Major themes and conflicts
        - How the story resolves
        - The book's main message or takeaway

        Make it flow as one coherent narrative summary.

        Section summaries:
        {combined_summaries}
        """

        return self.model_response(master_prompt, 800, 0.3)

    def get_genz_summary(self, master_summary: str, genz_prompt: str) -> str:
        final_prompt = f"""
        {genz_prompt}

        Book summary: {master_summary}
        """

        return self.model_response(final_prompt, self.final_summary_max_tokens, 0.8)

    def get_genz_summary_simple(self, book_text: str, genz_prompt: str) -> str:
        final_prompt = f"""
        {genz_prompt}

        Book text: {book_text}
        """
        return self.model_response(final_prompt, 500, 0.8)

    def process_book(self, book_text: str, genz_prompt: str) -> str:
        words = book_text.split()
        if len(words) <= self.chunk_size:
            return self.get_genz_summary_simple(book_text, genz_prompt)

        chunks = self.create_chunks(words)
        chunk_summaries = []
        for i, chunk in enumerate(chunks, 1):
            chunk_summary = self.summarize_chunk(chunk, i, len(chunks))
            chunk_summaries.append(chunk_summary)

        master_summary = self.create_master_summary(chunk_summaries)
        genz_summary = self.get_genz_summary(master_summary, genz_prompt)

        return genz_summary

