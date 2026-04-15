from django.db import models


class GeneratedImage(models.Model):
    prompt = models.TextField()
    image = models.ImageField(upload_to='ai_images/')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.prompt[:60]} ({self.created_at:%Y-%m-%d})"
