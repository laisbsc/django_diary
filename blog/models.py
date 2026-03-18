from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.text import slugify

from map.models import Location


class Category(models.Model):
    COLOR_CHOICES = [
        ('cobalt', 'Cobalt'),
        ('amber', 'Amber'),
        ('sienna', 'Sienna'),
    ]
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    color = models.CharField(max_length=20, choices=COLOR_CHOICES, default='cobalt')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'categories'


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    title = models.CharField(max_length=250)
    slug = models.SlugField(unique=True, max_length=250, blank=True)
    body = models.TextField()
    excerpt = models.TextField(blank=True)
    cover_image = models.ImageField(upload_to='blog/covers/', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='posts')
    location = models.ForeignKey(Location, on_delete=models.PROTECT, related_name='place', blank=True, null=True)
    read_time = models.PositiveIntegerField(default=1, editable=False)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('post_detail', kwargs={'slug': self.slug})

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Post.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1
            self.slug = slug
        self.read_time = max(1, round(len(self.body.split()) / 200))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class About(models.Model):
    body = models.TextField(help_text='Markdown supported.')
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.pk = 1  # Singleton — only one About page
        super().save(*args, **kwargs)

    def __str__(self):
        return f'About (updated {self.updated_at:%Y-%m-%d})'

    class Meta:
        verbose_name_plural = 'about'
