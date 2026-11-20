
import base64
import os
from groq import Groq


def describe_image(image_bytes, mime_type, question=""):
    """Analyze an image and answer questions using Groq."""

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError("GROQ_API_KEY is missing.")

    if mime_type not in {"image/png", "image/jpeg", "image/webp"}:
        raise ValueError("Unsupported image format.")

    encoded_image = base64.b64encode(image_bytes).decode("utf-8")

    data_url = f"data:{mime_type};base64,{encoded_image}"

    user_prompt = question or """
    Describe this image in 2 to 3 short bullet points.
    Use simple language.
    Mention only visible details.
    """

    client = Groq(api_key=api_key)

    completion = client.chat.completions.create(
        model=os.getenv(
            "GROQ_VISION_MODEL",
            "meta-llama/llama-4-scout-17b-16e-instruct"
        ),
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": user_prompt
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": data_url
                        }
                    }
                ]
            }
        ],
        temperature=0.3,
        max_completion_tokens=300
    )

    return completion.choices[0].message.content or "No description returned."
