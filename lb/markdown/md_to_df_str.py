import re
import pandas as pd


# Main function
def read_md_to_df_str(file, summarize=True, collapse=", ", encoding='utf-8'):
    """
    Read Markdown file and convert to a structured DataFrame.

    Parameters
    ----------
    file : str
        Path to the Markdown file.
    summarize : bool, optional
        If True, content under each heading is summarized into a single cell per heading level.
        If False, each line retains its own row in the output DataFrame.
    collapse : str, optional
        The string to use when collapsing multiple lines of content under each heading when summarize is True.
    encoding : str, optional
        The encoding to use when reading the file.

    Returns
    -------
    pandas.DataFrame
        A DataFrame where each row corresponds to a heading or content line.
        If summarize is True, each heading level is condensed into a single entry.
    """
    with open(file, 'r', encoding=encoding) as f:
        chr = f.readlines()
    
    return parse_md_to_df_str(chr, summarize=summarize, collapse=collapse)

def parse_md_to_df_str(chr, summarize=True, collapse=", "):
    """
    Parse Markdown content to a structured DataFrame.

    Parameters
    ----------
    chr : list of str
        A list of strings containing Markdown content.
    summarize : bool, optional
        If True, content under each heading is summarized into a single cell per heading level.
        If False, each line retains its own row in the output DataFrame.
    collapse : str, optional
        The string to use when collapsing multiple lines of content under each heading when summarize is True.

    Returns
    -------
    pandas.DataFrame
        A DataFrame where each row corresponds to a heading or content line.
        If summarize is True, each heading level is summarized into single entries per heading level.
    """
    h_lvs = detect_h_levels_unique(chr)
    h_cols = [f"h{lv}" for lv in h_lvs]
    
    df = pd.DataFrame({
        'line_num': range(1, len(chr) + 1),
        **{col: rep_headings(chr, lv) for col, lv in zip(h_cols, h_lvs)},
        'content_body': extract_body_content_vec(chr)
    })
    
    if not summarize:
        return df
    
    return df.groupby(h_cols).agg({
        'content_body': lambda x: collapse.join(filter(None, x))
    }).reset_index()

def extract_body_content_vec(chr):
    """
    Extract body content as vector.

    Parameters
    ----------
    chr : list of str
        A list of strings containing Markdown content.

    Returns
    -------
    list of str
        A list with body content preserved and non-body content replaced with empty strings.
    """
    return [line if detect_h_level_lines([line])[0] == 0 else "" for line in chr]

def rep_headings(chr, h=1):
    """
    Replicate headings across their scope.

    Parameters
    ----------
    chr : list of str
        A list of strings containing Markdown content.
    h : int, optional
        The heading level to process.

    Returns
    -------
    list of str
        A list where each element under a heading is filled with the heading's title.
    """
    h_lvs = detect_h_level_lines(chr)
    h_content = [line for line, lv in zip(chr, h_lvs) if lv == h]
    h_start_loc = [i for i, lv in enumerate(h_lvs) if lv == h]
    h_end_loc = find_end_loc_by_heading(h_lvs, h)
    
    out = [""] * len(chr)
    for content, start, end in zip(h_content, h_start_loc, h_end_loc):
        out[start:end+1] = [re.sub(r'^#+\s*', '', content.strip())] * (end - start + 1)
    
    return out

def detect_h_level_lines(chr):
    """
    Detect heading levels by line.

    Parameters
    ----------
    chr : list of str
        A list of strings containing Markdown content.

    Returns
    -------
    list of int
        A list indicating the heading level for each line.
    """
    return [len(re.match(r'^#+', line).group(0)) if re.match(r'^#+', line) else 0 for line in chr]

def detect_h_levels_unique(chr):
    """
    Detect unique heading levels.

    Parameters
    ----------
    chr : list of str
        A list of strings containing Markdown content.

    Returns
    -------
    list of int
        A list of unique heading levels found in the document, sorted in ascending order.
    """
    h_lvs = [lv for lv in detect_h_level_lines(chr) if lv > 0]
    return sorted(set(h_lvs))

def find_end_loc_by_heading(x, h=1):
    """
    Find ending locations by headings.

    Parameters
    ----------
    x : list of int
        A list indicating heading levels per line.
    h : int, optional
        The specific heading level to process.

    Returns
    -------
    list of int
        A list with the ending line positions for each heading.
    """
    h_consider_set = [i for i, lv in enumerate(x) if lv <= h] + [len(x)]
    h_loc = [i for i, lv in enumerate(x) if lv == h]
    
    out = []
    for loc in h_loc:
        end = next((i for i in h_consider_set if i > loc), len(x))
        out.append(end - 1 if end < len(x) else end)
    
    return out

# If you want to run this as a script
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python md_to_df_str.py <markdown_file>")
        sys.exit(1)
    
    df = read_md_to_df_str(sys.argv[1])
    print(df)