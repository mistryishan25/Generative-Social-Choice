import re
import pandas as pd
import tiktoken


def count_tokens(text, model="llava-v1.5-7b-4096-preview"):
    """
    Counts the number of tokens in a given text for a specific model.
    """
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))


def split_into_batches(comments, max_input_tokens):
    """Split comments into batches based on token limits."""
    batches = []
    current_batch = []
    current_tokens = 0

    for comment in comments:
        tokens = count_tokens(comment, model=model)
        if current_tokens + tokens <= max_input_tokens:
            current_batch.append(comment)
            current_tokens += tokens
        else:
            batches.append(current_batch)
            current_batch = [comment]
            current_tokens = tokens

    if current_batch:
        batches.append(current_batch)

    return batches



def clean_reddit_comments(comment):
    """
    Cleans a Reddit comment by:
    - Removing newline characters (\n)
    - Removing Markdown formatting for boldface (** or __) and italics (* or _)
    - Removing extra spaces
    - Stripping unnecessary quotes (like > at the beginning of lines)
    """
    # if comment.isinstance(list):
    #     comment = comment[0]
    # Remove newline characters
    comment = comment.replace('\n', ' ')
    
    # Remove Markdown formatting for bold (**bold**) and italics (*italic* or _italic_)
    comment = re.sub(r'(\*\*|__)(.*?)\1', r'\2', comment)  # Remove bold
    comment = re.sub(r'(\*|_)(.*?)\1', r'\2', comment)    # Remove italics
    
    # Remove block quotes (lines starting with >)
    comment = re.sub(r'^>\s?', '', comment, flags=re.MULTILINE)
    
    # Remove extra spaces
    comment = re.sub(r'\s+', ' ', comment).strip()
    
    return comment

# def replace_word(text, word):
#     # Use regular expression to match the word with word boundaries, ignoring case
#     if word in ["NTA", "YTA", "ESH", "NAH", "INFO", "YWBTA", "YTA"]:
#         pattern = r'\b' + re.escape(word) + r'\b'

#     return re.sub(pattern, '', text, flags=re.IGNORECASE).strip()

def replace_word(text, word):
    try:
        # Handle NaN or non-string values (convert to empty string if NaN or None)
        if pd.isna(text):
            text = ""
        if pd.isna(word):
            word = ""
        
        # Ensure both text and word are strings
        text = str(text)
        word = str(word)
        
        # Replace the word using regex (case-insensitive)
        pattern = r'\b' + re.escape(word) + r'\b'
        return re.sub(pattern, '', text, flags=re.IGNORECASE).strip()
    
    except Exception as e:
        print(f"Error processing text: {text}")
        print(f"Error with word: {word}")
        print(f"Exception: {e}")
        return text  # Return the original text in case of error