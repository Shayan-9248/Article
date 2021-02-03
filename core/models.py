from django.db import models
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericRelation
from django.db.models.signals import pre_save
from django.utils.html import format_html
from .utils import unique_slug_generator
from comment.models import Comment
from django.urls import reverse
from account.models import *


class ArticleManager(models.Manager):
    def published(self):
        return Article.objects.filter(status='p')


class IPAddress(models.Model):
    ip_address = models.GenericIPAddressField()

    def __str__(self):
        return self.ip_address


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
        ('d', 'draft'),
        ('p', 'published'),
        ('i', 'pending'),
        ('r', 'returned'),
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='articles')
    title = models.CharField(max_length=177)
    slug = models.SlugField(unique=True, null=True, blank=True)
    description = models.TextField()
    image = models.ImageField(default='1.jpg')
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_special = models.BooleanField(default=False)
    status = models.CharField(max_length=177, choices=STATUC_CHOICES)
    category = models.ManyToManyField(Category, blank=True)
    comments = GenericRelation(Comment)
    visit_count = models.ManyToManyField(IPAddress, through='ArticleVisit', blank=True, related_name='visit_count')
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE, null=True, blank=True)
    favourite = models.ManyToManyField(User, blank=True)

    objects = ArticleManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('core:detail', args=[self.slug, self.id])

    def image_tag(self):
        return format_html('<img src="{}" width=99>'.format(self.image.url))

    def category_to_str(self):
        return ', '.join([category.title for category in self.category.all()])

    def is_special_article(self):
        is_special_article.boolean = True
        return True

    def get_visit_count(self):
        return self.visit_count.count()


def slug_blog_save(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(slug_blog_save, sender=Article)



class ArticleVisit(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    ip_address = models.ForeignKey(IPAddress, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.article.title


class Brand(models.Model):
    title = models.CharField(max_length=177)

    def __str__(self):
        return self.title