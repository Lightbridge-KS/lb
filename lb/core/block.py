def extract_from_tags(
    string: str,
    tags: str,
    verbose: bool = True,
):
    """Extract content inside XML tags.

    This function searches for content between specified XML tags in a given string using regular expressions.

    Args:
        string (str): The input string containing XML tags to search through.
        tags (str): The XML tag name to search for (without angle brackets).
        verbose (bool, optional): If True, prints a message when tags are not found. Defaults to True.

    Returns:
        str or None: The content between the specified tags if found, None otherwise.

    Examples:
        >>> text = "<person>John Doe</person>"
        >>> extract_from_tags(text, "person")
        'John Doe'
        >>> extract_from_tags("<data></data>", "name", verbose=True)
        No <name> tags found in the input string.
        None
    """
    # Use regular expressions to find content between tags
    import re

    match = re.search(rf"<{tags}>\s*(.*?)\s*</{tags}>", string, re.DOTALL)
    if not match:
        if verbose:
            print(f"No <{tags}> tags found in the input string.")
        return

    # Return the first match string
    return match.group(1)


def extract_from_codeblock(
    string: str,
    language: str = "",
    verbose: bool = True,
):
    """Extract content inside code block.

    This function extracts the content between code block markers (```) from a given string.

    Args:
        string (str): Input string containing code block(s).
        language (str, optional): Programming language identifier for the code block.
            If specified, searches for blocks with matching language tag. Defaults to "".
        verbose (bool, optional): If True, prints message when no code block is found.
            Defaults to True.

    Returns:
        str or None: Content inside the first matching code block if found,
            None if no matching code block is found.

    Example:
        >>> text = '''```python
        ... def hello():
        ...     print("Hello")
        ... ```'''
        >>> extract_from_codeblock(text, "python")
        'def hello():\n    print("Hello")'
    """
    # Use regular expressions to find content between codeblock
    import re

    match = re.search(rf"```{language}\s*(.*?)\s```", string, re.DOTALL)
    if not match:
        if verbose:
            print(f"No '{language}' code block found in the input string.")
        return

    # Return the first match string
    return match.group(1)
