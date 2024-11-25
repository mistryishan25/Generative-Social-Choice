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
