import os
import logging
from typing import Optional
from fastmcp import FastMCP
from PyPDF2 import PdfReader, PdfWriter
from pdf2image import convert_from_path
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize the FastMCP server
mcp = FastMCP("PDFOperationsMCPServer")

# Default settings (can be overridden via environment variables)
DEFAULT_OUTPUT_DIR = os.getenv("PDF_OUTPUT_DIR", "")
DEFAULT_IMAGE_FORMAT = os.getenv("PDF_IMAGE_FORMAT", "PNG")
DEFAULT_IMAGE_DPI = int(os.getenv("PDF_IMAGE_DPI", "200"))
DEFAULT_HOST = os.getenv("PDF_SERVER_HOST", "0.0.0.0")
DEFAULT_PORT = int(os.getenv("PDF_SERVER_PORT", "8001"))


def validate_file_path(path: str) -> None:
    """
    Validate that a file path exists and is a file.
    
    Args:
        path: Path to validate.
        
    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the path is not a file.
    """
    if not path or not path.strip():
        raise ValueError("File path cannot be empty")
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")
    if not os.path.isfile(path):
        raise ValueError(f"Path is not a file: {path}")


def validate_pdf_path(path: str) -> None:
    """
    Validate that a file path exists and is a PDF file.
    
    Args:
        path: Path to validate.
        
    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the path is not a PDF file.
    """
    validate_file_path(path)
    if not path.lower().endswith('.pdf'):
        raise ValueError(f"File is not a PDF: {path}")


def get_output_path(original_path: str, suffix: str, output_dir: Optional[str] = None) -> str:
    """
    Generate an output file path based on the original path and a suffix.
    
    Args:
        original_path: Original file path.
        suffix: Suffix to append to the filename.
        output_dir: Optional output directory. If not provided, uses the same directory as the original file.
        
    Returns:
        Generated output path.
    """
    base_name = os.path.splitext(os.path.basename(original_path))[0]
    ext = os.path.splitext(original_path)[1]
    
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        return os.path.join(output_dir, f"{base_name}{suffix}{ext}")
    
    return f"{os.path.splitext(original_path)[0]}{suffix}{ext}"


@mcp.tool
def get_pdf_info(path: str) -> dict:
    """
    Get information about a PDF file including number of pages, metadata, and file size.
    
    Args:
        path: Path to the PDF file.
        
    Returns:
        Dictionary containing PDF information:
        - page_count: Number of pages
        - metadata: PDF metadata (title, author, creator, etc.)
        - file_size_bytes: File size in bytes
        - is_encrypted: Whether the PDF is encrypted
    """
    try:
        validate_pdf_path(path)
        reader = PdfReader(path)
        file_size = os.path.getsize(path)
        
        metadata = {}
        if reader.metadata:
            metadata = {
                "title": reader.metadata.get("/Title", ""),
                "author": reader.metadata.get("/Author", ""),
                "creator": reader.metadata.get("/Creator", ""),
                "producer": reader.metadata.get("/Producer", ""),
                "subject": reader.metadata.get("/Subject", ""),
            }
        
        logger.info(f"Retrieved info for PDF: {path}")
        return {
            "success": True,
            "page_count": len(reader.pages),
            "metadata": metadata,
            "file_size_bytes": file_size,
            "is_encrypted": reader.is_encrypted
        }
    except FileNotFoundError as e:
        logger.error(f"File not found: {path}")
        return {"success": False, "error": str(e)}
    except ValueError as e:
        logger.error(f"Invalid file: {path} - {e}")
        return {"success": False, "error": str(e)}
    except Exception as e:
        logger.error(f"Failed to get PDF info: {e}")
        return {"success": False, "error": f"Failed to get PDF info: {e}"}


@mcp.tool
def extract_text_from_pdf(
    path: str,
    start_page: Optional[int] = None,
    end_page: Optional[int] = None
) -> dict:
    """
    Extract text from a PDF file.

    Args:
        path: Path to the PDF file.
        start_page: Optional starting page number (1-based). Defaults to first page.
        end_page: Optional ending page number (1-based, inclusive). Defaults to last page.

    Returns:
        Dictionary containing:
        - success: Whether the operation succeeded
        - text: Extracted text as a string (if successful)
        - page_count: Number of pages processed
        - error: Error message (if failed)
    """
    try:
        validate_pdf_path(path)
        reader = PdfReader(path)
        total_pages = len(reader.pages)
        
        # Validate and set page range
        start_idx = 0 if start_page is None else max(0, start_page - 1)
        end_idx = total_pages if end_page is None else min(total_pages, end_page)
        
        if start_idx >= total_pages:
            return {
                "success": False,
                "error": f"Start page {start_page} exceeds total pages ({total_pages})"
            }
        
        text_parts = []
        for i in range(start_idx, end_idx):
            page_text = reader.pages[i].extract_text()
            if page_text:
                text_parts.append(page_text)
        
        text = "\n".join(text_parts)
        pages_processed = end_idx - start_idx
        
        logger.info(f"Extracted text from {pages_processed} pages of {path}")
        return {
            "success": True,
            "text": text,
            "page_count": pages_processed
        }
    except FileNotFoundError as e:
        logger.error(f"File not found: {path}")
        return {"success": False, "error": str(e)}
    except ValueError as e:
        logger.error(f"Invalid file: {path} - {e}")
        return {"success": False, "error": str(e)}
    except Exception as e:
        logger.error(f"Failed to extract text: {e}")
        return {"success": False, "error": f"Failed to extract text: {e}"}


@mcp.tool
def merge_pdfs(files: list, output: str) -> dict:
    """
    Merge multiple PDF files into one.

    Args:
        files: List of paths to PDF files to merge.
        output: Path to save the merged PDF.

    Returns:
        Dictionary containing:
        - success: Whether the operation succeeded
        - output_path: Path to the merged PDF (if successful)
        - page_count: Total number of pages in merged PDF
        - error: Error message (if failed)
    """
    try:
        if not files or len(files) == 0:
            return {"success": False, "error": "No files provided to merge"}
        
        if not output or not output.strip():
            return {"success": False, "error": "Output path cannot be empty"}
        
        # Validate all input files first
        for file in files:
            validate_pdf_path(file)
        
        writer = PdfWriter()
        total_pages = 0
        
        for file in files:
            reader = PdfReader(file)
            for page in reader.pages:
                writer.add_page(page)
                total_pages += 1
        
        # Ensure output directory exists
        output_dir = os.path.dirname(output)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        
        with open(output, "wb") as out_file:
            writer.write(out_file)
        
        logger.info(f"Merged {len(files)} PDFs into {output} ({total_pages} pages)")
        return {
            "success": True,
            "output_path": output,
            "page_count": total_pages,
            "files_merged": len(files)
        }
    except FileNotFoundError as e:
        logger.error(f"File not found during merge: {e}")
        return {"success": False, "error": str(e)}
    except ValueError as e:
        logger.error(f"Invalid file during merge: {e}")
        return {"success": False, "error": str(e)}
    except Exception as e:
        logger.error(f"Failed to merge PDFs: {e}")
        return {"success": False, "error": f"Failed to merge PDFs: {e}"}


@mcp.tool
def split_pdf(
    path: str,
    pages: list,
    output_dir: Optional[str] = None
) -> dict:
    """
    Split a PDF into individual pages or page ranges.

    Args:
        path: Path to the PDF file.
        pages: List of page numbers (1-based) to extract.
        output_dir: Optional directory to save split PDFs. Defaults to same directory as input.

    Returns:
        Dictionary containing:
        - success: Whether the operation succeeded
        - output_files: List of paths to the split PDF files (if successful)
        - error: Error message (if failed)
    """
    try:
        validate_pdf_path(path)
        
        if not pages or len(pages) == 0:
            return {"success": False, "error": "No pages specified to split"}
        
        reader = PdfReader(path)
        total_pages = len(reader.pages)
        
        # Validate page numbers
        for page_num in pages:
            if not isinstance(page_num, int) or page_num < 1:
                return {"success": False, "error": f"Invalid page number: {page_num}. Page numbers must be positive integers."}
            if page_num > total_pages:
                return {"success": False, "error": f"Page {page_num} exceeds total pages ({total_pages})"}
        
        output_files = []
        effective_output_dir = output_dir or DEFAULT_OUTPUT_DIR or os.path.dirname(path)
        
        if effective_output_dir:
            os.makedirs(effective_output_dir, exist_ok=True)
        
        base_name = os.path.splitext(os.path.basename(path))[0]
        
        for page_num in pages:
            writer = PdfWriter()
            writer.add_page(reader.pages[page_num - 1])
            
            if effective_output_dir:
                output_path = os.path.join(effective_output_dir, f"{base_name}_page_{page_num}.pdf")
            else:
                output_path = f"{os.path.splitext(path)[0]}_page_{page_num}.pdf"
            
            with open(output_path, "wb") as out_file:
                writer.write(out_file)
            output_files.append(output_path)
        
        logger.info(f"Split {len(pages)} pages from {path}")
        return {
            "success": True,
            "output_files": output_files,
            "pages_extracted": len(output_files)
        }
    except FileNotFoundError as e:
        logger.error(f"File not found: {path}")
        return {"success": False, "error": str(e)}
    except ValueError as e:
        logger.error(f"Invalid input: {e}")
        return {"success": False, "error": str(e)}
    except Exception as e:
        logger.error(f"Failed to split PDF: {e}")
        return {"success": False, "error": f"Failed to split PDF: {e}"}


@mcp.tool
def pdf_to_images(
    path: str,
    output_dir: Optional[str] = None,
    image_format: Optional[str] = None,
    dpi: Optional[int] = None,
    pages: Optional[list] = None
) -> dict:
    """
    Convert PDF pages to images.

    Args:
        path: Path to the PDF file.
        output_dir: Optional directory to save images. Defaults to same directory as input.
        image_format: Image format (PNG, JPEG, etc.). Defaults to PNG.
        dpi: Resolution in DPI. Defaults to 200.
        pages: Optional list of page numbers (1-based) to convert. Converts all pages if not specified.

    Returns:
        Dictionary containing:
        - success: Whether the operation succeeded
        - image_files: List of paths to the generated images (if successful)
        - error: Error message (if failed)
    """
    try:
        validate_pdf_path(path)
        
        # Use defaults if not provided
        effective_format = (image_format or DEFAULT_IMAGE_FORMAT).upper()
        effective_dpi = dpi or DEFAULT_IMAGE_DPI
        effective_output_dir = output_dir or DEFAULT_OUTPUT_DIR or os.path.dirname(path)
        
        # Validate format
        valid_formats = ["PNG", "JPEG", "JPG", "TIFF", "BMP", "GIF"]
        if effective_format not in valid_formats:
            return {"success": False, "error": f"Invalid image format: {effective_format}. Valid formats: {valid_formats}"}
        
        # Normalize JPEG format
        if effective_format == "JPG":
            effective_format = "JPEG"
        
        # Validate DPI
        if effective_dpi < 1 or effective_dpi > 600:
            return {"success": False, "error": f"DPI must be between 1 and 600, got {effective_dpi}"}
        
        if effective_output_dir:
            os.makedirs(effective_output_dir, exist_ok=True)
        
        # Convert PDF to images
        convert_kwargs = {"dpi": effective_dpi}
        if pages:
            # pdf2image uses 1-based page numbers
            convert_kwargs["first_page"] = min(pages)
            convert_kwargs["last_page"] = max(pages)
        
        images = convert_from_path(path, **convert_kwargs)
        
        base_name = os.path.splitext(os.path.basename(path))[0]
        ext = effective_format.lower()
        if ext == "jpeg":
            ext = "jpg"
        
        image_files = []
        
        # If specific pages requested, filter the images
        if pages:
            page_offset = min(pages) - 1
            for i, image in enumerate(images):
                actual_page = page_offset + i + 1
                if actual_page in pages:
                    if effective_output_dir:
                        image_path = os.path.join(effective_output_dir, f"{base_name}_page_{actual_page}.{ext}")
                    else:
                        image_path = f"{os.path.splitext(path)[0]}_page_{actual_page}.{ext}"
                    image.save(image_path, effective_format)
                    image_files.append(image_path)
        else:
            for i, image in enumerate(images):
                if effective_output_dir:
                    image_path = os.path.join(effective_output_dir, f"{base_name}_page_{i + 1}.{ext}")
                else:
                    image_path = f"{os.path.splitext(path)[0]}_page_{i + 1}.{ext}"
                image.save(image_path, effective_format)
                image_files.append(image_path)
        
        logger.info(f"Converted {len(image_files)} pages from {path} to {effective_format} images")
        return {
            "success": True,
            "image_files": image_files,
            "format": effective_format,
            "dpi": effective_dpi,
            "pages_converted": len(image_files)
        }
    except FileNotFoundError as e:
        logger.error(f"File not found: {path}")
        return {"success": False, "error": str(e)}
    except ValueError as e:
        logger.error(f"Invalid input: {e}")
        return {"success": False, "error": str(e)}
    except Exception as e:
        logger.error(f"Failed to convert PDF to images: {e}")
        return {"success": False, "error": f"Failed to convert PDF to images: {e}"}


@mcp.tool
def rotate_pdf(
    path: str,
    rotation: int,
    pages: Optional[list] = None,
    output: Optional[str] = None
) -> dict:
    """
    Rotate pages in a PDF file.
    
    Args:
        path: Path to the PDF file.
        rotation: Rotation angle in degrees (90, 180, or 270).
        pages: Optional list of page numbers (1-based) to rotate. Rotates all pages if not specified.
        output: Optional output file path. Defaults to overwriting the original file.
        
    Returns:
        Dictionary containing:
        - success: Whether the operation succeeded
        - output_path: Path to the rotated PDF (if successful)
        - pages_rotated: Number of pages rotated
        - error: Error message (if failed)
    """
    try:
        validate_pdf_path(path)
        
        # Validate rotation angle
        valid_rotations = [90, 180, 270, -90, -180, -270]
        if rotation not in valid_rotations:
            return {"success": False, "error": f"Invalid rotation angle: {rotation}. Valid angles: 90, 180, 270 (or negative equivalents)"}
        
        reader = PdfReader(path)
        writer = PdfWriter()
        total_pages = len(reader.pages)
        
        # Validate page numbers if specified
        if pages:
            for page_num in pages:
                if not isinstance(page_num, int) or page_num < 1:
                    return {"success": False, "error": f"Invalid page number: {page_num}"}
                if page_num > total_pages:
                    return {"success": False, "error": f"Page {page_num} exceeds total pages ({total_pages})"}
        
        pages_to_rotate = set(pages) if pages else set(range(1, total_pages + 1))
        
        for i, page in enumerate(reader.pages):
            if (i + 1) in pages_to_rotate:
                page.rotate(rotation)
            writer.add_page(page)
        
        output_path = output or path
        
        # Ensure output directory exists
        output_dir = os.path.dirname(output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        
        with open(output_path, "wb") as out_file:
            writer.write(out_file)
        
        logger.info(f"Rotated {len(pages_to_rotate)} pages in {path} by {rotation} degrees")
        return {
            "success": True,
            "output_path": output_path,
            "pages_rotated": len(pages_to_rotate),
            "rotation": rotation
        }
    except FileNotFoundError as e:
        logger.error(f"File not found: {path}")
        return {"success": False, "error": str(e)}
    except ValueError as e:
        logger.error(f"Invalid input: {e}")
        return {"success": False, "error": str(e)}
    except Exception as e:
        logger.error(f"Failed to rotate PDF: {e}")
        return {"success": False, "error": f"Failed to rotate PDF: {e}"}


@mcp.tool
def extract_pages(
    path: str,
    pages: list,
    output: str
) -> dict:
    """
    Extract specific pages from a PDF and save them to a new file.
    
    Args:
        path: Path to the source PDF file.
        pages: List of page numbers (1-based) to extract.
        output: Path to save the extracted pages.
        
    Returns:
        Dictionary containing:
        - success: Whether the operation succeeded
        - output_path: Path to the new PDF (if successful)
        - page_count: Number of pages extracted
        - error: Error message (if failed)
    """
    try:
        validate_pdf_path(path)
        
        if not pages or len(pages) == 0:
            return {"success": False, "error": "No pages specified to extract"}
        
        if not output or not output.strip():
            return {"success": False, "error": "Output path cannot be empty"}
        
        reader = PdfReader(path)
        total_pages = len(reader.pages)
        
        # Validate page numbers
        for page_num in pages:
            if not isinstance(page_num, int) or page_num < 1:
                return {"success": False, "error": f"Invalid page number: {page_num}"}
            if page_num > total_pages:
                return {"success": False, "error": f"Page {page_num} exceeds total pages ({total_pages})"}
        
        writer = PdfWriter()
        
        for page_num in pages:
            writer.add_page(reader.pages[page_num - 1])
        
        # Ensure output directory exists
        output_dir = os.path.dirname(output)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        
        with open(output, "wb") as out_file:
            writer.write(out_file)
        
        logger.info(f"Extracted {len(pages)} pages from {path} to {output}")
        return {
            "success": True,
            "output_path": output,
            "page_count": len(pages)
        }
    except FileNotFoundError as e:
        logger.error(f"File not found: {path}")
        return {"success": False, "error": str(e)}
    except ValueError as e:
        logger.error(f"Invalid input: {e}")
        return {"success": False, "error": str(e)}
    except Exception as e:
        logger.error(f"Failed to extract pages: {e}")
        return {"success": False, "error": f"Failed to extract pages: {e}"}


if __name__ == "__main__":
    logger.info(f"Starting PDF Operations MCP Server on {DEFAULT_HOST}:{DEFAULT_PORT}")
    mcp.run(transport="http", host=DEFAULT_HOST, port=DEFAULT_PORT)