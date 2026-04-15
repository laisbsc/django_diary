import asyncio
import logfire

from .agent import generate_and_save_image


def generate_image_task(image_id: int) -> None:
    from .models import GeneratedImage

    image = GeneratedImage.objects.get(pk=image_id)
    try:
        with logfire.span('generate image task', image_id=image_id, prompt=image.prompt):
            saved_name = asyncio.run(generate_and_save_image(image.prompt))
        image.image = saved_name
        image.status = GeneratedImage.COMPLETE
    except Exception as e:
        logfire.exception('image generation failed', image_id=image_id)
        image.status = GeneratedImage.FAILED
        image.error = str(e)
    image.save()
