def create_batches_by_token_count(comments, max_tokens= 32000):
    """
    Create batches of comments based on token count (approximated by word count).
    Sentences are preserved, and we group comments into batches without tokenizing them.
    """
    batches = []
    batch = []
    batch_tokens = 0

    # Iterate over comments and create batches
    for comment in comments:
        # Count the number of words in the comment (approximates the token count)
        comment_tokens = len(comment.split())

        # If adding this comment would exceed the token limit, start a new batch
        if batch_tokens + comment_tokens > max_tokens:
            batches.append(batch)  # Save the current batch
            batch = [comment]  # Start a new batch with this comment
            batch_tokens = comment_tokens
        else:
            batch.append(comment)  # Add the comment to the current batch
            batch_tokens += comment_tokens

    if batch:
        batches.append(batch)  # Add the remaining batch

    return batches


def extract_verdict_and_remainder(comment_body):

    pattern = r'\b(' + '|'.join(VERDICTS) + r')[,\.]?\b'
    match = re.search(pattern, comment_body, flags=re.IGNORECASE)
    if match:
        # Extract the matched verdict in uppercase
        verdict = match.group(1).upper()
        # Remove the first occurrence of the verdict from the text
        remaining_text = re.sub(pattern, '', comment_body, count=1, flags=re.IGNORECASE).strip()
        return verdict, remaining_text  # Return both the verdict and the remaining text
    return None, comment_body  # If no match, return None for verdict and the original text
