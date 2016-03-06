import uuid
from django.contrib.auth.models import User
from django.db import models


class Notes(models.Model):
    REFERENCE = 'Reference'
    NOTICE = 'Notice'
    REMINDER = 'Reminder'
    TODO = 'TODO'
    CATEGORY_CHOICES = (
        (REFERENCE, 'Reference'),
        (NOTICE, 'Notice'),
        (REMINDER, 'Reminder'),
        (TODO, 'TODO'),
    )
    user = models.ForeignKey(User)
    title = models.CharField(max_length=255)
    text = models.TextField(default='')
    date_time = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=15, choices=CATEGORY_CHOICES,
                                default=NOTICE)
    favorites = models.BooleanField(default=False)
    publish = models.BooleanField(default=False)
    uu_id = models.CharField(primary_key=True, default=uuid.uuid1,
                             editable=False, max_length=100)

    def __str__(self):
        return self.title


class Category(models.Model):
    cat_name = models.CharField(max_length=100)

    def __str__(self):
        return self.cat_name
