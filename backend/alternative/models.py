from django.db import models
import uuid


class Alternative(models.Model):
    id = models.UUIDField(
        primary_key=True,
        unique=True,
        default=uuid.uuid4,
        editable=False
    )
    description = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)
