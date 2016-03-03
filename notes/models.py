from datetime import datetime

from django.db import models

# Create your models here.
class Note(models.Model):
    """ Database table"""
    note_text = models.TextField()
    pub_date = models.DateTimeField(default=datetime.now())
