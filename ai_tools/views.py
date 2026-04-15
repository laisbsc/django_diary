import logfire
from asgiref.sync import sync_to_async
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.shortcuts import render, get_object_or_404

from .agent import generate_and_save_image
from .models import GeneratedImage


@login_required
async def image_gallery_view(request):
    with logfire.span('image gallery'):
        with logfire.span('fetch all generated images'):
            images = await sync_to_async(list)(GeneratedImage.objects.all())
        logfire.info('gallery loaded', image_count=len(images))
    return render(request, 'ai_tools/image_gallery.html', {'images': images})


@login_required
async def image_detail_view(request, pk):
    with logfire.span('image detail', pk=pk):
        with logfire.span('fetch generated image', pk=pk):
            image = await sync_to_async(get_object_or_404)(GeneratedImage, pk=pk)
    return render(request, 'ai_tools/image_detail.html', {'image': image})


@login_required
async def generate_image_view(request):
    image_url = None
    error = None
    prompt = ""

    if request.method == 'POST':
        prompt = request.POST.get('prompt', '').strip()
        if prompt:
            try:
                with logfire.span('generate image', prompt=prompt):
                    saved_name = await generate_and_save_image(prompt)
                    image_url = await sync_to_async(default_storage.url)(saved_name)
            except Exception as e:
                error = str(e)

    return render(request, 'ai_tools/generate_image.html', {
        'image_url': image_url,
        'error': error,
        'prompt': prompt,
    })
