from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from rest_framework.decorators import api_view
from .models import Content, Channel, Group
from .serializers import *

@api_view(['GET'])
def channel_by_id(request, id):
    # Get a single channel by id as JSON
    try:
        channel = Channel.objects.get(id=id)
    except:
        return JsonResponse({'error' : 'Channel not found'}, status=404)

    serializer = ChannelSerializer(channel) 
    return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def all_channels(request):
    # Get all channels as JSON
    channels = Channel.objects.all()
    serializer = ChannelSerializer(channels, many=True)
    return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def content_by_id(request, id):
    # Get a single content by id as JSON
    try:
        content = Content.objects.get(id=id)
    except:
        return JsonResponse({'error' : 'Content not found'}, status=404)

    serializer = ContentSerializer(content) 
    return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def channels_by_group(request, id):
    # Get all channels present in a group
    try:
        group = Group.objects.get(id=id)
    except:
        return JsonResponse({'error' : 'Group not found'}, status=404)

    serializer = ChannelSerializer(group.channels.all(), many=True)
    return JsonResponse(serializer.data, safe=False)

def all_groups(request):
    #Get all groups
    groups = Group.objects.all()
    serializer = GroupSerializer(groups, many=True)
    return JsonResponse(serializer.data, safe=False)