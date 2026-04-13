from asgiref.sync import sync_to_async
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.shortcuts import render

from .agent import generate_and_save_image


@login_required
async def generate_image_view(request):
    image_url = None
    error = None
    prompt = ""

    if request.method == 'POST':
        prompt = request.POST.get('prompt', '').strip()
        if prompt:
            try:
                saved_name = await generate_and_save_image(prompt)
                image_url = await sync_to_async(default_storage.url)(saved_name)
            except Exception as e:
                error = str(e)

    return render(request, 'ai_tools/generate_image.html', {
        'image_url': image_url,
        'error': error,
        'prompt': prompt,
    })
