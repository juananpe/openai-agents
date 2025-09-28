from __future__ import annotations

import asyncio
import os

from agents import Agent, ModelSettings, Runner, function_tool
from agents.extensions.models.litellm_model import LitellmModel
from litellm import api_key

from dotenv import load_dotenv

@function_tool
def get_weather(city: str):
    print(f"[debug] getting weather for {city}")
    return f"The weather in {city} is sunny."


async def main(model: str, api_key: str):
    agent = Agent(
        name="Assistant",
        instructions="You only respond in haikus.",
        model=LitellmModel(model=model, api_key=api_key),
        tools=[get_weather],
    )

    result = await Runner.run(agent, "What's the weather in Tokyo?")
    print(result.final_output)
    print(result.context_wrapper.usage)


if __name__ == "__main__":
    # Load environment variables from .env if present
    load_dotenv()

    # Strict: only read these .env keys.
    model = os.getenv("MODEL")
    # Accept only provider-specific canonical keys
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

    if not model:
        raise SystemExit("Missing MODEL in .env")
    
    asyncio.run(main(model, api_key))
