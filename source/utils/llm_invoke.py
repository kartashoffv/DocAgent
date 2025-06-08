from openai import AsyncOpenAI
from pydantic import BaseModel
from source.config import config


client = AsyncOpenAI(api_key=config.OPENAI_API_KEY)

async def llm_invoke_structured_output(system_prompt: str, user_input: str, text_format_output: BaseModel):
    completion = await client.responses.parse(
            model="gpt-4.1-nano-2025-04-14",
            temperature=0.1,
            input=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ],
            text_format=text_format_output
        )
    return completion.output_parsed
