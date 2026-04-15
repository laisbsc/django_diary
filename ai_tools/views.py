import logfire
from asgiref.sync import sync_to_async
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django_q.tasks import async_task

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
def generate_image_view(request):
    if request.method == 'POST':
        prompt = request.POST.get('prompt', '').strip()
        if prompt:
            image = GeneratedImage.objects.create(prompt=prompt)
            async_task('ai_tools.tasks.generate_image_task', image.pk)
            return redirect('image_pending', pk=image.pk)

    return render(request, 'ai_tools/generate_image.html')


@login_required
def image_pending_view(request, pk):
    image = get_object_or_404(GeneratedImage, pk=pk)
    return render(request, 'ai_tools/image_pending.html', {'image': image})


@login_required
def image_status_view(request, pk):
    image = get_object_or_404(GeneratedImage, pk=pk)
    data = {'status': image.status}
    if image.status == GeneratedImage.COMPLETE:
        data['url'] = default_storage.url(image.image.name)
    elif image.status == GeneratedImage.FAILED:
        data['error'] = image.error
    return JsonResponse(data)
