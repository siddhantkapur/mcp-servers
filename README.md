# MCP Servers & Agent

This project contains MCP (Model Context Protocol) servers and an agent that uses them.

## Project Structure

```
mcp-servers/
├── email_mcp_server/        # Email MCP server
│   └── server.py            # Email sending server
├── pdf_operations_server/   # PDF Operations MCP server
│   └── server.py            # PDF manipulation server
├── agent.py                 # MCP Agent for using MCP tools
└── requirements.txt         # Python dependencies
```

## Setup

1. **Install dependencies:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Start the Email MCP Server:**
   ```bash
   source .venv/bin/activate
   python3 -m email_mcp_server.server
   ```
   The server will run on `http://localhost:8000/mcp`

3. **Start the PDF Operations MCP Server:**
   ```bash
   source .venv/bin/activate
   python3 -m pdf_operations_server.server
   ```
   The server will run on `http://localhost:8001/mcp`

## Using the Agent

### Command Line Usage (Interactive)

The easiest way to use the agent is through the interactive command line:

```bash
python agent.py send
```

This will prompt you for:
- Recipient email address
- Subject
- Email body (multi-line input)
- Sender email address
- SMTP Server (optional, defaults to smtp.gmail.com)
- SMTP Port (optional, defaults to 465)
- **SMTP Username/Email (required)**
- **SMTP Password/App Password (required)**
- Confirmation before sending

The SMTP credentials you provide will be passed to the MCP server for sending the email.

### Programmatic Usage (Async - Recommended)

```python
import asyncio
from agent import MCPAgent

async def main():
    # Use async context manager (automatically handles connection/disconnection)
    async with MCPAgent() as agent:
        # Send an email
        success = await agent.send_email(
            sender="your-email@gmail.com",
            recipient="recipient@gmail.com",
            subject="Hello",
            body="This is a test email!"
        )
        
        if success:
            print("Email sent successfully!")

asyncio.run(main())
```

### Programmatic Usage (Synchronous)

```python
from agent import MCPAgentSync

# Create agent instance
agent = MCPAgentSync()

# Connect to MCP server
agent.connect()

try:
    # Send an email
    success = agent.send_email(
        sender="your-email@gmail.com",
        recipient="recipient@gmail.com",
        subject="Hello",
        body="This is a test email!"
    )
    
    if success:
        print("Email sent successfully!")
finally:
    agent.disconnect()
```

### Advanced Usage

#### List Available Tools

```python
# Async
async with MCPAgent() as agent:
    tools = await agent.list_tools()
    for tool in tools:
        print(f"Tool: {tool['name']}")

# Sync
agent = MCPAgentSync()
agent.connect()
try:
    tools = agent.list_tools()
    for tool in tools:
        print(f"Tool: {tool['name']}")
finally:
    agent.disconnect()
```

#### Call Any Tool Directly

```python
# Async
async with MCPAgent() as agent:
    result = await agent.call_tool("send_email", {
        "sender": "sender@gmail.com",
        "recipient": "recipient@gmail.com",
        "subject": "Test",
        "body": "Hello!"
    })
    
    if result["success"]:
        print("Tool executed successfully!")

# Sync
agent = MCPAgentSync()
agent.connect()
try:
    result = agent.call_tool("send_email", {
        "sender": "sender@gmail.com",
        "recipient": "recipient@gmail.com",
        "subject": "Test",
        "body": "Hello!"
    })
    if result["success"]:
        print("Tool executed successfully!")
finally:
    agent.disconnect()
```

## Agent Features

- ✅ **Built with FastMCP Client SDK**: Uses official FastMCP Client for reliable MCP protocol handling
- ✅ **Automatic Session Management**: Handles MCP session creation and management automatically
- ✅ **Tool Discovery**: List all available tools from the MCP server
- ✅ **Error Handling**: Graceful error handling and reporting
- ✅ **Async & Sync Support**: Both async/await and synchronous wrappers available
- ✅ **Interactive CLI**: Easy-to-use command line interface that prompts for SMTP credentials
- ✅ **Easy to Extend**: Simple API for adding new tool methods

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

### "Failed to connect to MCP server"
- Make sure the MCP server is running on `http://localhost:8000/mcp`
- Check that the server started without errors
- Verify the server is accessible: `curl http://localhost:8000/mcp`

### "No valid session ID provided"
- The agent should handle this automatically
- Make sure you're calling `agent.connect()` before using tools (or use the context manager)

### Email sending fails
- **Using defaults**: Check SMTP credentials in `email_mcp_server/server.py` (default values)
- **Using custom credentials**: Verify your SMTP server, port, username, and password are correct
- **Gmail/Yahoo**: Use App Password, not your regular password
- **Port settings**: Gmail uses port 465 (SSL) or 587 (TLS)
- **Server logs**: Check server terminal for detailed error messages
- **Test connection**: Try connecting with a regular email client first to verify credentials

### Import errors
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Verify you're using the correct Python version (3.8+)
- Activate your virtual environment: `source .venv/bin/activate`

## Extending the Agent

To add support for new MCP tools:

1. **Add a convenience method to the `MCPAgent` class:**
   ```python
   async def my_new_tool(self, arg1: str, arg2: int) -> dict:
       return await self.call_tool("my_new_tool", {
           "arg1": arg1,
           "arg2": arg2
       })
   ```

2. **Or use `call_tool()` directly:**
   ```python
   # Async
   result = await agent.call_tool("tool_name", {"param": "value"})
   
   # Sync
   result = agent.call_tool("tool_name", {"param": "value"})
   ```

3. **For synchronous wrapper, add to `MCPAgentSync` class:**
   ```python
   def my_new_tool(self, arg1: str, arg2: int) -> dict:
       if not self._agent:
           raise RuntimeError("Not connected. Call connect() first.")
       return asyncio.run(self._agent.my_new_tool(arg1, arg2))
   ```

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
