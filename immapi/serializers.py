from rest_framework import serializers
from .models import Channel, Content, Group

class ChannelSerializer(serializers.ModelSerializer):
    # Send only ids for sub_channels and contents
    sub_channels = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    contents = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Channel
        fields = ['id', 'title', 'language', 'cover', 'sub_channels', 'contents']
    
class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = ['id', 'title', 'metadata', 'rating', 'media']

class GroupSerializer(serializers.ModelSerializer):
    channels = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    
    class Meta:
        model = Group
        fields = ['id', 'title', 'channels']