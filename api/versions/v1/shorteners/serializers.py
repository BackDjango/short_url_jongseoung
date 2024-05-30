import hashlib
from datetime import datetime

from django.contrib.auth.models import AnonymousUser
from django.shortcuts import redirect
from rest_framework import serializers

from api.models.shorteners.models import ShortURL
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

            validated_data["short_url"] = "localhost:8000/api/v1/" + short_url

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


class ShortenerRedirectSerializer(serializers.Serializer):
    short_url = serializers.CharField(max_length=7, required=True, label="Short URL")

    def validate_short_url(self, value):
        try:
            short_url_instance = ShortURL.objects.get(short_url="localhost:8000/api/v1/" + value)
            if short_url_instance.expiration_date < datetime.now():
                if short_url_instance.is_active:
                    self.save(is_active=False)
                raise URLIsNotAuthorized
            short_url_instance.request_count += 1
            short_url_instance.save()
            return short_url_instance.origin_url
        except ShortURL.DoesNotExist:
            raise URLNotFound

    def perform_redirect(self):
        origin_url = self.validated_data["short_url"]
        return redirect(origin_url)
