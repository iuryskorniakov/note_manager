from datetime import datetime
from django.contrib.auth.models import User

from django.db import models

# Create your models here.
class Note(models.Model):
    """ Database table"""

    title = models.CharField(max_length=255)
    body = models.TextField()
    date = models.DateTimeField(default=datetime.now())
    category = models.ForeignKey('Category')
    favorites = models.BooleanField(default=False)
    uuid = models.CharField(max_length=255, default='', editable=False)
    user = models.ForeignKey(User)
    public = models.BooleanField(default=False)

    def __str__(self):
        return self.note_text

class Category(models.Model):
    category_name = models.CharField(max_length=255)

    def __str__(self):
        return self.category_name