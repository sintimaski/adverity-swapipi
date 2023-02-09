from django.db import models


class FileMeta(models.Model):
    name = models.UUIDField(primary_key=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
