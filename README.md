# MCP Servers & Agent

This project contains MCP (Model Context Protocol) servers and an AI-powered agent that uses them with Google Gemini.

## Project Structure

```
mcp-servers/
├── email_mcp_server/        # Email MCP server
│   └── server.py            # Email sending server
├── pdf_operations_server/   # PDF Operations MCP server
│   └── server.py            # PDF manipulation server
├── agent.py                 # OpenAI Agents SDK Agent with Gemini + MCP
└── requirements.txt         # Python dependencies
```

## Setup

1. **Install dependencies:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Configure your Gemini API key:**
   
   Get an API key from [Google AI Studio](https://aistudio.google.com/apikey), then either:
   
   ```bash
   # Option 1: Set environment variable
   export GEMINI_API_KEY=your_api_key_here
   
   # Option 2: Create a .env file
   echo "GEMINI_API_KEY=your_api_key_here" > .env
   ```

3. **Start the Email MCP Server:**
   ```bash
   source .venv/bin/activate
   python3 -m email_mcp_server.server
   ```
   The server will run on `http://localhost:8000/mcp`

4. **Start the PDF Operations MCP Server:**
   ```bash
   source .venv/bin/activate
   python3 -m pdf_operations_server.server
   ```
   The server will run on `http://localhost:8001/mcp`

## Using the Agent

### Interactive Chat Mode

Run the agent for an interactive chat session:

```bash
python agent.py
```

The agent will connect to the MCP servers and start an interactive conversation where you can ask it to:
- Send emails
- Extract text from PDFs
- Merge, split, or rotate PDFs
- Convert PDFs to images
- And more!

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `GEMINI_API_KEY` | (required) | Your Google Gemini API key |
| `GEMINI_MODEL` | `gemini-2.0-flash` | Gemini model to use |
| `EMAIL_MCP_URL` | `http://localhost:8000/mcp` | Email MCP server URL |
| `PDF_MCP_URL` | `http://localhost:8001/mcp` | PDF Operations MCP server URL |

### Programmatic Usage

```python
import asyncio
from agent import create_agent, create_mcp_servers
from agents import Runner

async def main():
    # Create and initialize MCP servers
    mcp_servers = create_mcp_servers()
    
    try:
        # Connect to MCP servers
        for server in mcp_servers:
            await server.connect()
        
        # Create agent with connected servers
        agent = create_agent(mcp_servers=mcp_servers)
        
        # Use the agent with Runner
        result = await Runner.run(
            agent,
            input="Extract text from /path/to/document.pdf"
        )
        print(result.final_output)
    finally:
        # Clean up MCP servers (handle exceptions to ensure all cleanup attempts are made)
        for server in mcp_servers:
            try:
                await server.cleanup()
            except Exception as e:
                print(f"Warning: Error cleaning up server: {e}")

asyncio.run(main())
```

### Custom Configuration

```python
from agent import create_gemini_model, create_mcp_servers, create_agent
from agents.mcp import MCPServerStreamableHttp

# Create custom MCP servers
custom_servers = [
    MCPServerStreamableHttp(
        params={"url": "http://localhost:9000/mcp"},
        name="Custom MCP Server",
    ),
]

# Create agent with custom configuration
agent = create_agent(mcp_servers=custom_servers)
```

## Agent Features

- ✅ **Powered by Google Gemini**: Uses Gemini's OpenAI-compatible API via the OpenAI Agents SDK
- ✅ **MCP Integration**: Connects to multiple MCP servers for email and PDF operations
- ✅ **Interactive Chat**: Natural language conversation interface
- ✅ **Tool Calling**: Automatically uses the right tools based on your requests
- ✅ **Extensible**: Easy to add more MCP servers and capabilities

## Email MCP Server

The email server provides a `send_email` tool that can send emails via SMTP.

### Configuration

The server comes with **default SMTP settings** configured. You can:

1. **Use the defaults** - Just call `send_email` with basic parameters
2. **Override via parameters** - Pass `smtp_server`, `smtp_port`, `smtp_username`, `smtp_password` when calling
3. **Override via environment variables** - Set `SMTP_SERVER`, `SMTP_PORT`, `SMTP_USERNAME`, `SMTP_PASSWORD`

**Default Settings:**
- SMTP Server: `smtp.gmail.com`
- SMTP Port: `465`
- SMTP Username: `siddhantkapur98@gmail.com` (configured in server.py)
- SMTP Password: (configured in server.py)

**Note:** For Gmail, you'll need an App Password (not your regular password). The server uses SMTP_SSL for port 465.

### Available Tools

- **`send_email`**: Send an email
  - **Required Parameters:** `sender`, `recipient`, `subject`, `body`
  - **Optional Parameters:** `smtp_server`, `smtp_port`, `smtp_username`, `smtp_password`
  - **Returns:** `True` if successful, `False` otherwise
  
  If optional SMTP parameters are not provided, the server uses default values configured in `server.py`.

## PDF Operations MCP Server

The PDF operations server provides tools for working with PDF files.

### Configuration

The server can be configured via environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `PDF_OUTPUT_DIR` | (same as input) | Default output directory for generated files |
| `PDF_IMAGE_FORMAT` | `PNG` | Default image format for PDF to image conversion |
| `PDF_IMAGE_DPI` | `200` | Default DPI for image conversion |
| `PDF_SERVER_HOST` | `0.0.0.0` | Server host address |
| `PDF_SERVER_PORT` | `8001` | Server port |

### Available Tools

- **`get_pdf_info(path)`**: Get PDF metadata and information
  - Returns: page count, metadata (title, author, etc.), file size, encryption status

- **`extract_text_from_pdf(path, start_page?, end_page?)`**: Extract text from PDF
  - Optional page range support (1-based page numbers)
  - Returns: extracted text and page count

- **`merge_pdfs(files, output)`**: Merge multiple PDFs into one
  - Returns: output path, total page count, files merged count

- **`split_pdf(path, pages, output_dir?)`**: Split specific pages into individual PDFs
  - Returns: list of output file paths

- **`pdf_to_images(path, output_dir?, image_format?, dpi?, pages?)`**: Convert PDF pages to images
  - Supports PNG, JPEG, TIFF, BMP, GIF formats
  - Configurable DPI (1-600)
  - Optional specific page selection
  - Returns: list of image file paths

- **`rotate_pdf(path, rotation, pages?, output?)`**: Rotate pages in a PDF
  - Supports 90, 180, 270 degree rotations
  - Can rotate specific pages or all pages
  - Returns: output path, pages rotated count

- **`extract_pages(path, pages, output)`**: Extract specific pages to a new PDF
  - Returns: output path, page count

### Response Format

All tools return structured responses with consistent format:

```json
{
  "success": true,
  "output_path": "/path/to/output.pdf",
  "page_count": 3,
  ...
}
```

On error:
```json
{
  "success": false,
  "error": "Error message description"
}
```

## Troubleshooting

### "GEMINI_API_KEY environment variable is not set"
- Make sure you've set your Gemini API key via environment variable or `.env` file
- Get an API key from [Google AI Studio](https://aistudio.google.com/apikey)

### "Failed to connect to MCP server"
- Make sure the MCP server is running on the expected URL
- Check that the server started without errors
- Verify the server is accessible: `curl http://localhost:8000/mcp`

### Email sending fails
- **Using defaults**: Check SMTP credentials in `email_mcp_server/server.py` (default values)
- **Using custom credentials**: Verify your SMTP server, port, username, and password are correct
- **Gmail/Yahoo**: Use App Password, not your regular password
- **Port settings**: Gmail uses port 465 (SSL) or 587 (TLS)
- **Server logs**: Check server terminal for detailed error messages

### Import errors
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Verify you're using the correct Python version (3.9+)
- Activate your virtual environment: `source .venv/bin/activate`

## Extending the Agent

### Adding More MCP Servers

To add more MCP servers to the agent:

```python
from agent import create_agent
from agents.mcp import MCPServerStreamableHttp

# Create your custom MCP servers
custom_servers = [
    MCPServerStreamableHttp(
        params={"url": "http://localhost:8000/mcp"},
        name="Email Server",
    ),
    MCPServerStreamableHttp(
        params={"url": "http://localhost:8001/mcp"},
        name="PDF Server",
    ),
    MCPServerStreamableHttp(
        params={"url": "http://localhost:9000/mcp"},
        name="Your Custom Server",
    ),
]

agent = create_agent(mcp_servers=custom_servers)
```

### Using Different Gemini Models

Set the `GEMINI_MODEL` environment variable:

```bash
export GEMINI_MODEL=gemini-1.5-pro
```

Available models include:
- `gemini-2.0-flash` (default, fast)
- `gemini-1.5-flash` (fast, cost-effective)
- `gemini-1.5-pro` (more capable)

## Building More MCP Servers

You can build additional MCP servers for various purposes:
- File operations
- Web scraping
- Calendar management
- Database queries
- API integrations
- And much more!

Each server should follow the same pattern as `email_mcp_server`:
1. Use FastMCP framework
2. Define tools with `@mcp.tool` decorator
3. Run with `mcp.run(transport="http", host="0.0.0.0", port=<PORT>)`

## License

MIT
