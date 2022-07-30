from pyexpat import model
from rest_framework import serializers
from app.models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post

        fields = ['title', 'content',  'like_count', 'created_on']