"""
MCP Agent - Built using OpenAI Agents SDK with Gemini API.
Supports Email and PDF Operations MCP Servers.

This agent uses Google Gemini's OpenAI-compatible API to power an intelligent
assistant that can interact with MCP servers for email and PDF operations.

Environment Variables:
    GEMINI_API_KEY: Your Google Gemini API key (required)
    EMAIL_MCP_URL: URL for Email MCP server (default: http://localhost:8000/mcp)
    PDF_MCP_URL: URL for PDF Operations MCP server (default: http://localhost:8001/mcp)
    GEMINI_MODEL: Gemini model to use (default: gemini-2.0-flash)
"""
import asyncio
import os
from typing import List, Optional

from dotenv import load_dotenv
from openai import AsyncOpenAI
from agents import Agent, Runner
from agents.models.openai_chatcompletions import OpenAIChatCompletionsModel
from agents.mcp import MCPServerStreamableHttp

# Load environment variables
load_dotenv()

# Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

# MCP Server URLs
EMAIL_MCP_URL = os.getenv("EMAIL_MCP_URL", "http://localhost:8000/mcp")
PDF_MCP_URL = os.getenv("PDF_MCP_URL", "http://localhost:8001/mcp")


def create_gemini_model() -> OpenAIChatCompletionsModel:
    """
    Create an OpenAI-compatible model client for Gemini API.
    
    Returns:
        OpenAIChatCompletionsModel configured for Gemini
        
    Raises:
        ValueError: If GEMINI_API_KEY is not set
    """
    if GEMINI_API_KEY is None:
        raise ValueError(
            "GEMINI_API_KEY environment variable is required. "
            "Please set it in your .env file or environment."
        )
    
    client = AsyncOpenAI(
        api_key=GEMINI_API_KEY,
        base_url=GEMINI_BASE_URL,
    )
    
    return OpenAIChatCompletionsModel(
        model=GEMINI_MODEL,
        openai_client=client,
    )


def create_mcp_servers() -> List[MCPServerStreamableHttp]:
    """
    Create MCP server connections for email and PDF operations.
    
    Returns:
        List of MCPServerStreamableHttp instances
    """
    servers = []
    
    # Email MCP Server
    email_server = MCPServerStreamableHttp(
        params={"url": EMAIL_MCP_URL},
        name="Email MCP Server",
    )
    servers.append(email_server)
    
    # PDF Operations MCP Server
    pdf_server = MCPServerStreamableHttp(
        params={"url": PDF_MCP_URL},
        name="PDF Operations MCP Server",
    )
    servers.append(pdf_server)
    
    return servers


def create_agent(
    mcp_servers: Optional[List[MCPServerStreamableHttp]] = None,
    model: Optional[OpenAIChatCompletionsModel] = None,
) -> Agent:
    """
    Create an MCP Agent with Gemini model and MCP server connections.
    
    Args:
        mcp_servers: Optional list of MCP servers. If not provided, uses default servers.
        model: Optional model instance. If not provided, creates Gemini model.
        
    Returns:
        Configured Agent instance
    """
    if model is None:
        model = create_gemini_model()
    
    if mcp_servers is None:
        mcp_servers = create_mcp_servers()
    
    instructions = """You are a helpful assistant with access to email and PDF operations tools.

You can help users with:

**Email Operations:**
- Send emails using the send_email tool

**PDF Operations:**
- Get PDF information (page count, metadata, file size)
- Extract text from PDF files
- Merge multiple PDF files into one
- Split PDFs into individual pages
- Convert PDF pages to images
- Rotate PDF pages
- Extract specific pages from a PDF

When a user asks you to perform an operation:
1. Understand what they want to accomplish
2. Use the appropriate tool(s) from the MCP servers
3. Provide clear feedback about the results

Always be helpful and explain what you're doing step by step."""

    return Agent(
        name="MCP Assistant",
        instructions=instructions,
        model=model,
        mcp_servers=mcp_servers,
    )


async def run_agent_loop(agent: Agent):
    """
    Run an interactive chat loop with the agent.
    
    Args:
        agent: The configured Agent instance
    """
    print("\n🤖 MCP Agent powered by Gemini is ready!")
    print("Type your message and press Enter. Type 'quit' or 'exit' to stop.\n")
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ('quit', 'exit', 'q'):
                print("\n👋 Goodbye!")
                break
            
            # Run the agent with the user's input
            result = await Runner.run(
                agent,
                input=user_input,
            )
            
            print(f"\nAssistant: {result.final_output}\n")
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}\n")


async def main_async():
    """Main async entry point."""
    import sys
    
    # Early check for API key with helpful error message
    if GEMINI_API_KEY is None:
        print("❌ Error: GEMINI_API_KEY environment variable is not set.")
        print("\nPlease set your Gemini API key:")
        print("  1. Create a .env file with: GEMINI_API_KEY=your_api_key_here")
        print("  2. Or export it: export GEMINI_API_KEY=your_api_key_here")
        print("\nYou can get an API key from: https://aistudio.google.com/apikey")
        sys.exit(1)
    
    print("🚀 Starting MCP Agent with Gemini...")
    print(f"   Model: {GEMINI_MODEL}")
    print(f"   Email MCP Server: {EMAIL_MCP_URL}")
    print(f"   PDF MCP Server: {PDF_MCP_URL}")
    
    # Create and run the agent
    agent = create_agent()
    
    # Use context manager for proper MCP server lifecycle
    async with agent:
        await run_agent_loop(agent)


if __name__ == "__main__":
    asyncio.run(main_async())
