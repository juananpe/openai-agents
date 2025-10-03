
import asyncio
from pathlib import Path
from agents import Agent, Runner
from agents.mcp.server import MCPServerStdio

from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file


async def main():
    serverPlaywright = MCPServerStdio(
        name="Playwright MCP",
        params={
            "command": "npx",
            "args": ["@playwright/mcp@latest"],
        }
    )
    serverFilesystem = MCPServerStdio(
        name="Filesystem MCP",
        params={
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-filesystem", str(Path(__file__).parent)],
        }
    )
    await serverPlaywright.connect()
    await serverFilesystem.connect()

    agent = Agent(
        name="Playwright REPL Agent",
        instructions="You are a helpful assistant with access to Playwright MCP tools.",
        mcp_servers=[serverPlaywright, serverFilesystem]
    )
    print("Type 'exit' or 'quit' to end the session.")
    while True:
        user_input = input("You: ")
        if user_input.strip().lower() in {"exit", "quit"}:
            print("Exiting REPL.")
            break
        result = await Runner.run(agent, user_input, max_turns=20)
        print("Agent:", result.final_output)
    # Clean up MCP server to avoid shutdown exceptions
    await serverPlaywright.cleanup()
    await serverFilesystem.cleanup()

if __name__ == "__main__":
    asyncio.run(main())
