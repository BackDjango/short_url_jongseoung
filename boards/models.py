from django.db import models

from core.models import TimeStampedModel
from users.models import User


class Board(TimeStampedModel):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = "boards"
