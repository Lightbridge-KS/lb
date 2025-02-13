__all__ = ['read_docx', 'read_docx_dir', 'read_docx_dir_df']

from pathlib import Path
import pandas as pd
import docx

from ..core.fs import list_dir

def read_docx(path: Path) -> str:
    """Reads the content of a .docx file and returns it as a string.

    Args:
        path (Path): The path to the .docx file to be read

    Returns:
        str: The text content of the document with paragraphs joined together

    Raises:
        docx.opc.exceptions.PackageNotFoundError: If the file is not found
        docx.opc.exceptions.InvalidXmlError: If the file is not a valid .docx file
    """
    doc = docx.Document(path)
    doc_gen = (para.text for para in doc.paragraphs)
    return "".join(doc_gen)


def read_docx_dir(directory: Path, recursive=True) -> dict:
    """Reads all .docx files in a directory and returns a dictionary.

    Args:
        directory (Path): Path to directory containing .docx files
        recursive (bool, optional): Whether to search subdirectories recursively. Defaults to True.

    Returns:
        dict: Dictionary with filenames (without extension) as keys and document contents as values
            {filename1: doc_content1, filename2: doc_content2, ...}
    """
    paths_ls = list_dir(directory, pattern="*.docx", recursive=recursive)
    stem_ls = [path.stem for path in paths_ls]
    doc_ls = [read_docx(path) for path in paths_ls]
    return dict(zip(stem_ls, doc_ls))


def read_docx_dir_df(directory: Path, recursive=True) -> pd.DataFrame:
    """Reads all .docx files in a directory and returns a pandas DataFrame.

    This function scans a directory for .docx files and creates a DataFrame containing the
    filename, full path, and content of each document.

    Args:
        directory (Path): Path object pointing to the directory to scan
        recursive (bool, optional): Whether to scan subdirectories recursively. Defaults to True.

    Returns:
        pd.DataFrame: DataFrame with columns:
            - filename: Name of the file without extension
            - path: Full path to the file
            - content: Text content of the document

    Examples:
        >>> docs_df = read_docx_dir_df(Path("documents/"))
        >>> print(docs_df.columns)
        Index(['filename', 'path', 'content'], dtype='object')
    """
    paths_ls = list_dir(directory, pattern="*.docx", recursive=recursive)
    stem_ls = [path.stem for path in paths_ls]
    doc_ls = [read_docx(path) for path in paths_ls]
    return pd.DataFrame({"filename": stem_ls, "path": paths_ls, "content": doc_ls})
