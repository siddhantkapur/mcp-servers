import os
from fastmcp import FastMCP
from PyPDF2 import PdfReader, PdfWriter
from pdf2image import convert_from_path

# Initialize the FastMCP server
mcp = FastMCP("PDFOperationsMCPServer")

# Helper function to ensure file exists
def ensure_file_exists(path: str):
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")

@mcp.tool
def extract_text_from_pdf(path: str) -> str:
    """
    Extract text from a PDF file.

    Args:
        path: Path to the PDF file.

    Returns:
        Extracted text as a string.
    """
    try:
        ensure_file_exists(path)
        reader = PdfReader(path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        return f"Failed to extract text: {e}"

@mcp.tool
def merge_pdfs(files: list, output: str) -> str:
    """
    Merge multiple PDF files into one.

    Args:
        files: List of paths to PDF files to merge.
        output: Path to save the merged PDF.

    Returns:
        Path to the merged PDF.
    """
    try:
        writer = PdfWriter()
        for file in files:
            ensure_file_exists(file)
            reader = PdfReader(file)
            for page in reader.pages:
                writer.add_page(page)
        with open(output, "wb") as out_file:
            writer.write(out_file)
        return output
    except Exception as e:
        return f"Failed to merge PDFs: {e}"

@mcp.tool
def split_pdf(path: str, pages: list) -> list:
    """
    Split a PDF into individual pages.

    Args:
        path: Path to the PDF file.
        pages: List of page numbers to split.

    Returns:
        List of paths to the split PDF files.
    """
    try:
        ensure_file_exists(path)
        reader = PdfReader(path)
        output_files = []
        for page_num in pages:
            writer = PdfWriter()
            writer.add_page(reader.pages[page_num - 1])  # Page numbers are 1-based
            output_path = f"{os.path.splitext(path)[0]}_page_{page_num}.pdf"
            with open(output_path, "wb") as out_file:
                writer.write(out_file)
            output_files.append(output_path)
        return output_files
    except Exception as e:
        return f"Failed to split PDF: {e}"

@mcp.tool
def pdf_to_images(path: str) -> list:
    """
    Convert PDF pages to images.

    Args:
        path: Path to the PDF file.

    Returns:
        List of paths to the generated images.
    """
    try:
        ensure_file_exists(path)
        images = convert_from_path(path)
        image_files = []
        for i, image in enumerate(images):
            image_path = f"{os.path.splitext(path)[0]}_page_{i + 1}.png"
            image.save(image_path, "PNG")
            image_files.append(image_path)
        return image_files
    except Exception as e:
        return f"Failed to convert PDF to images: {e}"

if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8001)