from rest_framework import serializers

from app.models import Ad, Achievement, Note


class AdSerializer(serializers.ModelSerializer):
    post_type = serializers.SerializerMethodField()

    class Meta:
        model = Ad
        fields = ("post_type", "created", "title", "description", "foreign_url", "published")

    def get_post_type(self, obj):
        return Ad.POST_TYPE


class AchievementSerializer(serializers.ModelSerializer):
    post_type = serializers.SerializerMethodField()

    class Meta:
        model = Achievement
        fields = ("post_type", "title", "conditions", "created")

    def get_post_type(self, obj):
        return Achievement.POST_TYPE


class NoteSerializer(serializers.ModelSerializer):
    post_type = serializers.SerializerMethodField()

    class Meta:
        model = Note
        fields = ("post_type", "title", "body", "created", "author")

    def get_post_type(self, obj):
        return Note.POST_TYPE
