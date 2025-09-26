
import asyncio
from agents import Agent, Runner
from agents.mcp.server import MCPServerStdio

from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file


async def main():
    server = MCPServerStdio(
        name="Playwright MCP",
        params={
            "command": "npx",
            "args": ["@playwright/mcp@latest"],
        }
    )
    await server.connect()
    agent = Agent(
        name="Playwright REPL Agent",
        instructions="You are a helpful assistant with access to Playwright MCP tools.",
        mcp_servers=[server],
    )
    print("Type 'exit' or 'quit' to end the session.")
    while True:
        user_input = input("You: ")
        if user_input.strip().lower() in {"exit", "quit"}:
            print("Exiting REPL.")
            break
        result = await Runner.run(agent, user_input)
        print("Agent:", result.final_output)
    # Clean up MCP server to avoid shutdown exceptions
    await server.cleanup()

if __name__ == "__main__":
    asyncio.run(main())
