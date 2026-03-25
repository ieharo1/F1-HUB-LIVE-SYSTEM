from django.db import models


class ApiSnapshot(models.Model):
    source = models.CharField(max_length=60, unique=True)
    payload = models.JSONField(default=dict)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f'{self.source} @ {self.updated_at}'
