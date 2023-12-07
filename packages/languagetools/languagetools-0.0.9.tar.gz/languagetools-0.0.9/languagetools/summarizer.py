import openai
import getpass
import os
import tiktoken
from concurrent.futures import ThreadPoolExecutor

def split_into_chunks(text, tokens, model, overlap):
    encoding = tiktoken.encoding_for_model(model)
    tokenized_text = encoding.encode(text)
    chunks = []
    for i in range(0, len(tokenized_text), tokens - overlap):
        chunk = encoding.decode(tokenized_text[i:i + tokens])
        chunks.append(chunk)
    return chunks

def chunk_summaries(summaries, tokens, model, overlap):
    encoding = tiktoken.encoding_for_model(model)
    chunked_summaries = []
    current_chunk = ""
    current_tokens = 0

    for summary in summaries:
        tokenized_summary = encoding.encode(summary)
        new_tokens = current_tokens + len(tokenized_summary)

        # If the new token count exceeds the limit, handle the current chunk
        if new_tokens > tokens:
            # If current chunk is empty or summary alone exceeds limit, add summary as standalone
            if current_tokens == 0 or len(tokenized_summary) > tokens:
                chunked_summaries.append(summary)
            else:
                chunked_summaries.append(current_chunk)
                current_chunk = summary
                current_tokens = len(tokenized_summary)
            continue

        # Add summary to the current chunk
        current_chunk += "\n\n" + summary if current_chunk else summary
        current_tokens = new_tokens

    # Add remaining chunk if not empty
    if current_chunk:
        chunked_summaries.append(current_chunk)

    return chunked_summaries


def summarize_chunk(transcription, model):
    """Summarize a chunk of text using a given language model."""
    response = openai.ChatCompletion.create(
        model=model,
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": "You are a highly skilled AI trained in language comprehension and summarization. I would like you to read the following text and summarize it into a concise abstract paragraph. Aim to retain the most important points, providing a coherent and readable summary that could help a person understand the main points of the discussion without needing to read the entire text. Please avoid unnecessary details or tangential points."
            },
            {
                "role": "user",
                "content": transcription
            }
        ]
    )
    return response['choices'][0]['message']['content']

def summarize_summaries(transcription, model):
    """Summarize previously summarized text."""
    response = openai.ChatCompletion.create(
        model=model,
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": "You are tasked with taking multiple summarized texts and merging them into one unified and concise summary. Maintain the core essence of the content and provide a clear and comprehensive summary that encapsulates all the main points from the individual summaries."
            },
            {
                "role": "user",
                "content": transcription
            }
        ]
    )
    return response['choices'][0]['message']['content']

def summarize_chunks(chunks, model):
    """Summarize the chunks of text using summarize_chunk."""
    with ThreadPoolExecutor() as executor:
        summaries = list(executor.map(lambda chunk: summarize_chunk(chunk, model), chunks))
    return summaries

def compress_summaries(summaries, model, chunk_size, overlap):
    """Compress the summaries in a while loop."""
    while len(summaries) > 1:
        # Use the previously defined chunk_summaries function to chunk the summaries
        summary_chunks = chunk_summaries(summaries, chunk_size, model, overlap)

        # Use multithreading to summarize each chunk simultaneously
        with ThreadPoolExecutor() as executor:
            summaries = list(executor.map(lambda chunk: summarize_summaries(chunk, model), summary_chunks))

    return summaries[0]

def summarize(text, model="gpt-3.5-turbo", chunk_size=2000, overlap=50):
    """Summarize a given text using a specified model."""
    # Retrieve OpenAI API key
    openai_api_key = os.getenv('OPENAI_API_KEY')
    if openai_api_key is None:
        openai_api_key = getpass.getpass(prompt="Please enter your OpenAI API key: ")
    openai.api_key = openai_api_key

    # Split the text into chunks
    chunks = split_into_chunks(text, chunk_size, model, overlap)

    # (Map) Summarize each chunk
    summaries = summarize_chunks(chunks, model)

    # (Reduce) Compress the summaries
    final_summary = compress_summaries(summaries, model, chunk_size, overlap)

    return final_summary