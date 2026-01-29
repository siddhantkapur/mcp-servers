"""
MCP Agent - Built using FastMCP Client SDK.
Supports Email and PDF Operations MCP Servers.
"""
import asyncio
from typing import Dict, Any, Optional, List
from fastmcp import Client


class MCPAgent:
    """Agent that connects to an MCP server and uses its tools via FastMCP Client SDK."""
    
    def __init__(self, mcp_url: str = "http://localhost:8000/mcp"):
        """
        Initialize the MCP Agent.
        
        Args:
            mcp_url: URL of the MCP server endpoint
        """
        self.mcp_url = mcp_url
        self.client: Optional[Client] = None
        self._connected = False
    
    async def connect(self) -> bool:
        """
        Establish a connection/session with the MCP server.
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            self.client = Client(self.mcp_url)
            await self.client.__aenter__()
            self._connected = True
            print(f"✅ Connected to MCP server at {self.mcp_url}")
            return True
        except Exception as e:
            print(f"❌ Failed to connect to MCP server: {e}")
            return False
    
    async def disconnect(self):
        """Close the connection to the MCP server."""
        if self.client and self._connected:
            await self.client.__aexit__(None, None, None)
            self._connected = False
            print("Disconnected from MCP server")
    
    async def list_tools(self) -> List[Dict[str, Any]]:
        """
        List all available tools from the MCP server.
        
        Returns:
            List of available tools
        """
        if not self._connected or not self.client:
            raise RuntimeError("Not connected to MCP server. Call connect() first.")
        
        try:
            tools_result = await self.client.list_tools()
            return tools_result.tools if hasattr(tools_result, 'tools') else []
        except Exception as e:
            print(f"Error listing tools: {e}")
            return []
    
    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Call a tool on the MCP server.
        
        Args:
            tool_name: Name of the tool to call
            arguments: Arguments to pass to the tool
            
        Returns:
            Tool execution result with 'success' and 'result' or 'error' keys
        """
        if not self._connected or not self.client:
            raise RuntimeError("Not connected to MCP server. Call connect() first.")
        
        try:
            result = await self.client.call_tool(tool_name, arguments)
            
            # Extract the result from the tool response
            if hasattr(result, 'content') and result.content:
                # Get text content
                text_content = result.content[0].text if result.content else ""
                
                # Get structured content if available
                structured_content = {}
                if hasattr(result, 'structuredContent') and result.structuredContent:
                    structured_content = result.structuredContent
                
                return {
                    "success": True,
                    "result": {
                        "content": [{"type": "text", "text": text_content}],
                        "structuredContent": structured_content
                    }
                }
            else:
                return {
                    "success": True,
                    "result": {"content": []}
                }
        except Exception as e:
            return {
                "success": False,
                "error": {"message": str(e)}
            }
    
    # Email Tool
    async def send_email(self, **kwargs) -> bool:
        """
        Send an email using the send_email tool.
        """
        result = await self.call_tool("send_email", kwargs)
        return result.get("success", False)
    
    # PDF Tools
    async def extract_text_from_pdf(self, path: str) -> str:
        """
        Extract text from a PDF file.
        """
        result = await self.call_tool("extract_text_from_pdf", {"path": path})
        if result["success"]:
            return result["result"]["content"][0]["text"]
        return f"Error: {result['error']['message']}"
    
    async def merge_pdfs(self, files: List[str], output: str) -> str:
        """
        Merge multiple PDF files into one.
        """
        result = await self.call_tool("merge_pdfs", {"files": files, "output": output})
        if result["success"]:
            return result["result"]["content"][0]["text"]
        return f"Error: {result['error']['message']}"
    
    async def split_pdf(self, path: str, pages: List[int]) -> List[str]:
        """
        Split a PDF into individual pages.
        """
        result = await self.call_tool("split_pdf", {"path": path, "pages": pages})
        if result["success"]:
            return result["result"]["structuredContent"]["files"]
        return f"Error: {result['error']['message']}"
    
    async def pdf_to_images(self, path: str) -> List[str]:
        """
        Convert PDF pages to images.
        """
        result = await self.call_tool("pdf_to_images", {"path": path})
        if result["success"]:
            return result["result"]["structuredContent"]["images"]
        return f"Error: {result['error']['message']}"
    
    async def __aenter__(self):
        """Async context manager entry."""
        await self.connect()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.disconnect()


# Example usage and CLI interface
async def main_async():
    """Async main function."""
    import sys
    
    # Use async context manager
    async with MCPAgent() as agent:
        # List available tools
        print("\n📋 Available tools:")
        tools = await agent.list_tools()
        for tool in tools:
            print(f"  - {tool['name']}")
        
        # Example: Extract text from a PDF
        if len(sys.argv) > 1 and sys.argv[1] == "extract_text":
            pdf_path = input("Enter the path to the PDF file: ").strip()
            text = await agent.extract_text_from_pdf(pdf_path)
            print("\nExtracted Text:")
            print(text)
        
        # Example: Merge PDFs
        elif len(sys.argv) > 1 and sys.argv[1] == "merge_pdfs":
            files = input("Enter the paths to the PDF files (comma-separated): ").split(",")
            output = input("Enter the output file path: ").strip()
            result = await agent.merge_pdfs(files, output)
            print(f"\nMerge Result: {result}")
        
        # Example: Split PDF
        elif len(sys.argv) > 1 and sys.argv[1] == "split_pdf":
            pdf_path = input("Enter the path to the PDF file: ").strip()
            pages = input("Enter the page numbers to split (comma-separated): ").split(",")
            pages = [int(page.strip()) for page in pages]
            result = await agent.split_pdf(pdf_path, pages)
            print(f"\nSplit Result: {result}")
        
        # Example: Convert PDF to Images
        elif len(sys.argv) > 1 and sys.argv[1] == "pdf_to_images":
            pdf_path = input("Enter the path to the PDF file: ").strip()
            result = await agent.pdf_to_images(pdf_path)
            print(f"\nImages Generated: {result}")
        
        else:
            print("\n💡 Usage examples:")
            print("  python agent.py extract_text")
            print("  python agent.py merge_pdfs")
            print("  python agent.py split_pdf")
            print("  python agent.py pdf_to_images")


if __name__ == "__main__":
    asyncio.run(main_async())
