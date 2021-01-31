from django.db import models
from django.utils import timezone
from django.db.models.signals import pre_save
from .utils import unique_slug_generator
from django.utils.html import format_html
from django.urls import reverse
from account.models import *


class Category(models.Model):
    sub_category = models.ForeignKey('self', on_delete=models.CASCADE, related_name='s_category', null=True, blank=True)
    is_sub = models.BooleanField(default=False)
    title = models.CharField(max_length=177)
    slug = models.SlugField(unique=True, null=True, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('core:category', args=[self.slug])


class Article(models.Model):
    STATUC_CHOICES = (
        ('Draft', 'draft'),
        ('Published', 'published')
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='articles')
    title = models.CharField(max_length=177)
    slug = models.SlugField(unique=True, null=True, blank=True)
    description = models.TextField()
    image = models.ImageField(default='1.jpg')
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=177, choices=STATUC_CHOICES)
    category = models.ManyToManyField(Category, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('core:detail', args=[self.slug, self.id])

    def image_tag(self):
        return format_html('<img src="{}" width=99>'.format(self.image.url))

    def category_to_str(self):
        return ', '.join([category.title for category in self.category.all()])


def slug_blog_save(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(slug_blog_save, sender=Article)