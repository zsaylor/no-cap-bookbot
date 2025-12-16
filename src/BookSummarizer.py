"""
AI-powered book summarization module for No Cap BookBot.

This module handles intelligent chunking of large texts and uses OpenAI's GPT models
to generate summaries, including custom Gen Z-style summaries.
"""

from typing import List, Optional

import openai
import streamlit as st


class BookSummarizer:
    """
    Handles AI-powered book summarization with intelligent chunking.

    This class processes books of any length by breaking them into manageable chunks,
    summarizing each chunk while maintaining context, then creating a master summary
    and finally transforming it into the desired style (e.g., Gen Z slang).

    Attributes:
        client: OpenAI API client instance.
        chunk_size: Maximum words per chunk (default: 100,000).
        overlap_size: Word overlap between chunks to maintain context (default: 1,000).
        max_output_tokens_per_chunk: Max tokens for chunk summaries (default: 1,000).
        final_summary_max_tokens: Max tokens for final summary (default: 500).
    """

    def __init__(self, api_key: str):
        """
        Initialize the BookSummarizer with OpenAI API credentials.

        Args:
            api_key: OpenAI API key for authentication.
        """
        self.client = openai.OpenAI(api_key=api_key)
        self.chunk_size = 100000  # Max words per chunk to stay within context limits
        self.overlap_size = 1000  # Word overlap to maintain narrative continuity
        self.max_output_tokens_per_chunk = 1000  # Detailed chunk summaries
        self.final_summary_max_tokens = 500  # Concise final output

    def model_response(self, prompt: str, max_tokens: int, temperature: float) -> str:
        """
        Send a prompt to OpenAI's GPT model and return the response.

        Args:
            prompt: The text prompt to send to the model.
            max_tokens: Maximum number of tokens in the response.
            temperature: Sampling temperature (0.0 = deterministic, 1.0 = creative).

        Returns:
            str: The model's response text, or an error message if the API call fails.
        """
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=temperature,
            )
            return response.choices[0].message.content.strip()

        except Exception as e:
            return f"Oops fam, the AI summary failed: {str(e)}"

    def create_chunks(self, words: List[str]) -> List[str]:
        """
        Split a list of words into overlapping chunks for processing.

        Creates chunks of configurable size with overlap to maintain context
        between chunks for better summarization continuity.

        Args:
            words: List of words from the book text.

        Returns:
            List[str]: List of text chunks, each as a joined string.
        """
        chunks = []
        start = 0
        while start < len(words):
            end = min(start + self.chunk_size, len(words))
            chunk_text = " ".join(words[start:end])
            chunks.append(chunk_text)

            if end >= len(words):
                break

            start += self.chunk_size - self.overlap_size

        return chunks

    def summarize_chunk(self, chunk: str, chunk_number: int, total_chunks: int) -> str:
        """
        Summarize a single chunk of text with positional context.

        Args:
            chunk: The text chunk to summarize.
            chunk_number: The position of this chunk (1-indexed).
            total_chunks: Total number of chunks in the book.

        Returns:
            str: A detailed summary of the chunk focusing on plot, characters, and themes.
        """
        position_context = ""
        if chunk_number == 1:
            position_context = "This is the beginning of the book."
        elif chunk_number == total_chunks:
            position_context = "This is the end of the book."
        else:
            position_context = (
                f"This is part {chunk_number} of {total_chunks} of the book."
            )

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
        """
        Combine multiple chunk summaries into a cohesive master summary.

        Args:
            chunk_summaries: List of individual chunk summaries to combine.

        Returns:
            str: A comprehensive narrative summary capturing the complete story arc.
        """
        combined_summaries = "\n\n".join(
            [f"Section {i + 1}: {summary}" for i, summary in enumerate(chunk_summaries)]
        )

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
        """
        Transform a master summary into Gen Z style using a custom prompt.

        Args:
            master_summary: The comprehensive book summary to transform.
            genz_prompt: Custom prompt defining the Gen Z transformation style.

        Returns:
            str: The summary rewritten in Gen Z slang and style.
        """
        final_prompt = f"""
        {genz_prompt}

        Book summary: {master_summary}
        """

        return self.model_response(final_prompt, self.final_summary_max_tokens, 0.8)

    def get_genz_summary_simple(self, book_text: str, genz_prompt: str) -> str:
        """
        Generate a Gen Z summary directly from book text (for shorter books).

        Skips the chunking process for books under the chunk size threshold.

        Args:
            book_text: The complete book text.
            genz_prompt: Custom prompt defining the Gen Z transformation style.

        Returns:
            str: Gen Z-style summary generated directly from the full text.
        """
        final_prompt = f"""
        {genz_prompt}

        Book text: {book_text}
        """
        return self.model_response(final_prompt, 500, 0.8)

    def process_book(self, book_text: str, genz_prompt: str) -> str:
        """
        Main entry point for processing a book and generating a Gen Z summary.

        Automatically chooses between simple (short books) and chunked (long books)
        processing based on book length. Displays progress indicators for long books.

        Args:
            book_text: The complete book text to summarize.
            genz_prompt: Custom prompt defining the Gen Z transformation style.

        Returns:
            str: The final Gen Z-style summary of the book.
        """
        words = book_text.split()
        if len(words) <= self.chunk_size:
            return self.get_genz_summary_simple(book_text, genz_prompt)

        chunks = self.create_chunks(words)
        total_chunks = len(chunks)

        progress_bar = st.progress(0)
        status_text = st.empty()

        chunk_summaries = []
        for i, chunk in enumerate(chunks, 1):
            status_text.text(f"📖 Processing section {i} of {total_chunks}...")
            progress_bar.progress(
                i / (total_chunks + 2)
            )  # +2 for master summary and final Gen Z conversion
            chunk_summary = self.summarize_chunk(chunk, i, total_chunks)
            chunk_summaries.append(chunk_summary)

        status_text.text("🔗 Combining sections into master summary...")
        progress_bar.progress((total_chunks + 1) / (total_chunks + 2))
        master_summary = self.create_master_summary(chunk_summaries)

        status_text.text("✨ Transforming to Gen Z style...")
        progress_bar.progress(1.0)
        genz_summary = self.get_genz_summary(master_summary, genz_prompt)

        progress_bar.empty()
        status_text.empty()

        return genz_summary
