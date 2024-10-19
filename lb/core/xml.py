

# %% auto 0
__all__ = ['extract_from_tags']

# %% 
def extract_from_tags(string: str, # string to extract
                      tags: str    # XML tags
                      ):  
    """Extract content inside XML tags"""
     # Use regular expressions to find content between tags
    import re
    match = re.search(rf'<{tags}>\s*(.*?)\s*</{tags}>', string, re.DOTALL)
    if not match:
        print(f"No <{tags}> tags found in the input string.")
        return

    # Return the first match string
    return  match.group(1)
