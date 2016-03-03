from datetime import datetime

from django.db import models

# Create your models here.
class Note(models.Model):
    """ Database table"""
    note_text = models.TextField()
    note_title = models.CharField(max_length=100)
    pub_date = models.DateTimeField(default=datetime.now())

    def __str__(self):
        return self.note_text