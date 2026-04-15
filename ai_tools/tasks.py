import asyncio
import logfire
from opentelemetry import propagate, context as otel_context

from .agent import generate_and_save_image


def generate_image_task(image_id: int, trace_context: dict | None = None) -> None:
    from .models import GeneratedImage

    # Restore the trace context from the originating web request so all spans
    # in this task appear nested under the same trace in Logfire.
    ctx = propagate.extract(trace_context or {})
    token = otel_context.attach(ctx)

    image = GeneratedImage.objects.get(pk=image_id)
    try:
        with logfire.span('generate image task', image_id=image_id, prompt=image.prompt):
            saved_name = asyncio.run(generate_and_save_image(image.prompt))
        image.image = saved_name
        image.status = GeneratedImage.COMPLETE
        logfire.info('image generation complete', image_id=image_id, saved_path=saved_name)
    except Exception as e:
        logfire.exception('image generation failed', image_id=image_id)
        image.status = GeneratedImage.FAILED
        image.error = str(e)
    finally:
        image.save()
        otel_context.detach(token)
