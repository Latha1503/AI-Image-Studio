
import os
from openai import OpenAI


def generate_image(prompt: str) -> str:
    """Generate an image using Grok API."""

    api_key = os.getenv("XAI_API_KEY")

    if not api_key:
        raise ValueError("XAI_API_KEY is missing. Check your .env file.")

    client = OpenAI(
        api_key=api_key,
        base_url="https://api.x.ai/v1"
    )

    response = client.images.generate(
        model="grok-imagine-image-2.0",
        prompt=prompt
    )

    if not response.data or not response.data[0].url:
        raise RuntimeError("No image URL returned.")

    return response.data[0].url
