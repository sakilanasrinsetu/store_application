from .models import Store
from rest_framework import serializers


class StoreSerializer(serializers.ModelSerializer):
    slug = serializers.CharField(read_only = True)

    class Meta:
        model = Store
        fields = "__all__"
