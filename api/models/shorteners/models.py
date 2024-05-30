from django.db import models

from core.models import TimeStampedModel


class ShortURL(TimeStampedModel):
    user = models.ForeignKey("users.User", related_name="user_url", on_delete=models.CASCADE)
    origin_url = models.URLField(verbose_name="원본 url")
    short_url = models.CharField(max_length=100, verbose_name="단축 url")
    request_count = models.IntegerField(default=0, verbose_name="요청 횟수")
    expiration_date = models.DateTimeField(null=True, blank=True, verbose_name="만료일")
    is_active = models.BooleanField(default=True, verbose_name="활성화 여부")

    class Meta:
        db_table = "short_url"
