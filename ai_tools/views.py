import logfire
from asgiref.sync import sync_to_async
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django_q.tasks import async_task
from opentelemetry import propagate

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
        image = await sync_to_async(get_object_or_404)(GeneratedImage, pk=pk)
    return render(request, 'ai_tools/image_detail.html', {'image': image})


@login_required
def generate_image_view(request):
    if request.method == 'POST':
        prompt = request.POST.get('prompt', '').strip()
        if prompt:
            with logfire.span('enqueue image generation', prompt=prompt):
                image = GeneratedImage.objects.create(prompt=prompt)
                # Propagate the current trace context into the background task
                # so its spans appear nested under this request's trace in Logfire.
                carrier: dict = {}
                propagate.inject(carrier)
                async_task('ai_tools.tasks.generate_image_task', image.pk, trace_context=carrier)
                logfire.info('image task enqueued', image_id=image.pk, prompt=prompt)
            return redirect('image_pending', pk=image.pk)

    return render(request, 'ai_tools/generate_image.html')


@login_required
def image_pending_view(request, pk):
    image = get_object_or_404(GeneratedImage, pk=pk)
    return render(request, 'ai_tools/image_pending.html', {'image': image})


@login_required
@require_POST
def image_delete_view(request, pk):
    image = get_object_or_404(GeneratedImage, pk=pk)
    if image.image:
        default_storage.delete(image.image.name)
    image.delete()
    return redirect('image_gallery')


@login_required
def image_status_view(request, pk):
    image = get_object_or_404(GeneratedImage, pk=pk)
    data = {'status': image.status}
    if image.status == GeneratedImage.COMPLETE:
        data['url'] = default_storage.url(image.image.name)
    elif image.status == GeneratedImage.FAILED:
        data['error'] = image.error
    return JsonResponse(data)
