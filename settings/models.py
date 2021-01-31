from django.db import models


class Setting(models.Model):
    title = models.CharField(max_length=177, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=14, null=True, blank=True)
    image = models.ImageField(default='1.jpg', null=True, blank=True)

    def __str__(self):
        return str(self.title)