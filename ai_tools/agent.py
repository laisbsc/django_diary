import uuid

import logfire
from asgiref.sync import sync_to_async
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from pydantic_ai import Agent, BinaryImage, ImageGenerationTool

_image_agent: Agent | None = None


def _get_agent() -> Agent:
    """Lazy initializer for the Pydantic AI agent with an image generation tool."""
    global _image_agent
    if _image_agent is None:
        _image_agent = Agent(
            'openai-responses:gpt-4o',
            builtin_tools=[
                ImageGenerationTool(
                    quality='medium',
                    size='auto',
                )
            ],
            output_type=BinaryImage,
            system_prompt='Generate images based on the user\'s input and add an afro hairstyle to it.'
        )
    return _image_agent


async def generate_and_save_image(prompt: str) -> str:
    """Run the image agent and save the result via Django storage. Returns the saved file name."""
    with logfire.span('agent run', prompt=prompt):
        result = await _get_agent().run(prompt)
    image: BinaryImage = result.output

    name = f"ai_images/{uuid.uuid4().hex}.jpg"
    with logfire.span('save image to storage', storage_path=name, image_bytes=len(image.data)):
        saved = await sync_to_async(default_storage.save)(name, ContentFile(image.data))

    return saved
