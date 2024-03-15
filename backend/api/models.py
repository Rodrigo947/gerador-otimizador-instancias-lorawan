from django.db import models


class Logs(models.Model):
  used_at = models.DateTimeField(auto_now=True)
