import hashlib
from datetime import datetime, timedelta

from django.contrib.auth.models import AnonymousUser
from django.shortcuts import redirect
from django.utils import timezone
from rest_framework import serializers

from api.models.shorteners.models import DailyCount, ShortURL
from core.exceptions.service_exceptions import *


class ShortenerCreateSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    request_count = serializers.ReadOnlyField()
    short_url = serializers.ReadOnlyField()
    is_active = serializers.ReadOnlyField()

    class Meta:
        model = ShortURL
        fields = ["id", "user", "origin_url", "short_url", "request_count", "expiration_date", "is_active"]

    def save(self, **kwargs):
        user = self.context.get("request").user
        if isinstance(user, AnonymousUser):
            raise UserNotFound

        return super().save(**kwargs, user=user)

    def create(self, validated_data):
        origin_url = validated_data.get("origin_url")

        try:
            instance = ShortURL.objects.get(origin_url=origin_url)
            if instance.expiration_date < datetime.now():
                instance.is_active = True
                instance.expiration_date = validated_data["expiration_date"]
                instance.save()
            return instance
        except ShortURL.DoesNotExist:
            index = self.url_to_index(url=origin_url)
            short_url = self.base62(index)

            if len(short_url) > 7:
                short_url = short_url[:7]

            validated_data["short_url"] = short_url

            return super().create(validated_data)

    def url_to_index(self, url):
        hash_object = hashlib.sha256(url.encode())
        hash_int = int(hash_object.hexdigest(), 16)
        return hash_int

    def base62(self, index):
        characters = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
        result = ""
        while index > 0:
            result = characters[index % 62] + result
            index = index // 62

        return result

    def get_weekly_count(self, instance):
        today = timezone.now().date()
        seven_days_ago = today - timedelta(days=7)
        counts = DailyCount.objects.filter(short_url=instance, date__gte=seven_days_ago)

        weekly_count = sum(count.count for count in counts)
        return weekly_count

    def get_daily_count(self, instance):
        today = timezone.now().date()
        seven_days_ago = today - timedelta(days=7)
        counts = DailyCount.objects.filter(short_url=instance, date__gte=seven_days_ago)

        result = {count.date.isoformat(): count.count for count in counts}
        return result


class ShortenerRedirectSerializer(serializers.Serializer):
    short_url = serializers.CharField(max_length=7, required=True, label="Short URL")

    def validate_short_url(self, value):
        try:
            short_url_instance = ShortURL.objects.get(short_url=value)
            if short_url_instance.expiration_date < datetime.now():
                if short_url_instance.is_active:
                    short_url_instance.is_active = False
                    short_url_instance.save()
                    raise URLIsNotAuthorized
            short_url_instance.request_count += 1
            short_url_instance.save()
            self.plus_daily_count(short_url_instance)
            return short_url_instance.origin_url
        except ShortURL.DoesNotExist:
            raise URLNotFound

    def plus_daily_count(self, instance):
        today = timezone.now().date()
        try:
            daily_count = DailyCount.objects.get(short_url=instance, date=today)
            daily_count.count += 1
            daily_count.save()
        except DailyCount.DoesNotExist:
            DailyCount.objects.create(short_url=instance, date=today)

    def perform_redirect(self):
        origin_url = self.validated_data["short_url"]
        return redirect(origin_url)
