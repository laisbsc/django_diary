import os
import uuid

import logfire
from asgiref.sync import sync_to_async
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from pydantic_ai import Agent, BinaryImage, ImageGenerationTool

_image_agent: Agent | None = None


def _get_agent() -> Agent:
    global _image_agent
    if _image_agent is None:
        if os.environ.get('LOGFIRE_TOKEN'):
            logfire.instrument_pydantic_ai()
        _image_agent = Agent(
            'openai-responses:gpt-4o',
            builtin_tools=[
                ImageGenerationTool(
                    quality='high',
                    size='1024x1024',
                )
            ],
            output_type=BinaryImage,
            system_prompt='You are an image generation assistant. \
                            Generate images based on the user\'s description. \
                            If the user describes a person or character, always depict them with a natural afro hairstyle'
        )
    return _image_agent


async def generate_and_save_image(prompt: str) -> str:
    """Run the image agent and save the result via Django storage. Returns the saved file name."""
    result = await _get_agent().run(prompt)
    image: BinaryImage = result.output

    name = f"ai_images/{uuid.uuid4().hex}.jpg"
    saved = await sync_to_async(default_storage.save)(name, ContentFile(image.data))

    from .models import GeneratedImage
    await sync_to_async(GeneratedImage.objects.create)(prompt=prompt, image=saved)

    return saved
