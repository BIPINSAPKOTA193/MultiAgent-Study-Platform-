"""PDF and text file extraction utilities"""

from typing import Optional
from pathlib import Path
import io

from pypdf import PdfReader
from ..core.logger import logger


def extract_text_from_pdf(file_path: Optional[str] = None, file_content: Optional[bytes] = None) -> str:
    """
    Extract text from PDF file.
    
    Args:
        file_path: Path to PDF file
        file_content: PDF file content as bytes
    
    Returns:
        Extracted text as string
    
    Raises:
        ValueError: If neither file_path nor file_content is provided
        Exception: If PDF extraction fails
    """
    if file_path is None and file_content is None:
        raise ValueError("Either file_path or file_content must be provided")
    
    try:
        if file_content:
            # Read from bytes
            pdf_file = io.BytesIO(file_content)
            reader = PdfReader(pdf_file)
        else:
            # Read from file path
            reader = PdfReader(file_path)
        
        text_parts = []
        for page in reader.pages:
            text = page.extract_text()
            if text:
                text_parts.append(text)
        
        full_text = "\n\n".join(text_parts)
        logger.info(f"Extracted {len(full_text)} characters from PDF")
        
        return full_text
    
    except Exception as e:
        logger.error(f"Error extracting text from PDF: {str(e)}")
        raise


def extract_text_from_file(file_path: str) -> str:
    """
    Extract text from file (PDF or plain text).
    
    Args:
        file_path: Path to file
    
    Returns:
        Extracted text as string
    """
    path = Path(file_path)
    
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    # Determine file type
    suffix = path.suffix.lower()
    
    if suffix == ".pdf":
        return extract_text_from_pdf(file_path=file_path)
    elif suffix in [".txt", ".md", ".text"]:
        # Plain text file
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        logger.info(f"Extracted {len(content)} characters from text file")
        return content
    else:
        # Try as text file
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            logger.info(f"Extracted {len(content)} characters from file")
            return content
        except UnicodeDecodeError:
            raise ValueError(f"Unsupported file type: {suffix}")
