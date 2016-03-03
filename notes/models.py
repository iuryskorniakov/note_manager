from django.contrib.auth.models import User
from django.utils import timezone

from django.db import models


class Category(models.Model):
    category_name = models.CharField(max_length=255, default='')

    def __str__(self):
        return self.category_name


# Create your models here.
class Note(models.Model):
    """ Database table"""
    uuid = models.CharField(max_length=255, default='', editable=False, primary_key=True)
    title = models.CharField(max_length=255, default='')
    author = models.ForeignKey(User, default=None)
    body = models.TextField(default='')
    created_date = models.DateTimeField(
            default=timezone.now())
    published_date = models.DateTimeField(
            blank=True, null=True)
    category = models.ForeignKey('Category', default=None)
    favorites = models.BooleanField(default=False)
    public = models.BooleanField(default=False)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
