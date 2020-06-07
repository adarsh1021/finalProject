from rest_framework import serializers

from django.contrib.auth.models import User

from .models import Facebook, Twitter


class FacebookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Facebook
        fields = "__all__"
