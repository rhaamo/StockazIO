from rest_framework import serializers

from controllers.oauth import models


class ApplicationSerializer(serializers.ModelSerializer):
    """
    Coin coin
    """

    scopes = serializers.CharField(source="scope")

    class Meta:
        model = models.Application
        fields = ["client_id", "name", "scopes", "created", "updated"]


class CreateApplicationSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, max_length=255)
    scopes = serializers.CharField(source="scope", default="read")

    def create(self, validated_data):
        # Due to django-oauth-toolkit change https://github.com/jazzband/django-oauth-toolkit/releases/tag/2.1.0
        # we need to grab the client_secret before it is saved (and then hashed)
        app = models.Application(**validated_data)
        secret = app.client_secret
        scopes = app.scope
        app.save()
        return {
            "client_id": app.client_id,
            "client_secret": secret,
            "redirect_uris": app.redirect_uris,
            "name": app.name,
            "scopes": scopes,
            "created": app.created,
            "updated": app.updated,
        }

    class Meta:
        model = models.Application
        fields = [
            "client_id",
            "name",
            "scopes",
            "client_secret",
            "created",
            "updated",
            "redirect_uris",
        ]
        read_only_fields = ["client_id", "client_secret", "created", "updated"]
