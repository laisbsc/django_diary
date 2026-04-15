from django.db import models


class GeneratedImage(models.Model):
    PENDING = 'pending'
    COMPLETE = 'complete'
    FAILED = 'failed'
    STATUS_CHOICES = [(PENDING, 'Pending'), (COMPLETE, 'Complete'), (FAILED, 'Failed')]

    prompt = models.TextField()
    image = models.ImageField(upload_to='ai_images/', blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)
    error = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.prompt[:60]} ({self.created_at:%Y-%m-%d})"
