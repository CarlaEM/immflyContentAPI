from django.urls import path
from .views import *

urlpatterns = [
    path('channels/<int:id>', channel_by_id, name="channel_by_id"),
    path('channels/', all_channels, name="all_channels"),
    path('contents/<int:id>', content_by_id, name="content_by_id"),
    path('groups/', all_groups, name="all_groups"),
    path('channels/filter/<int:id>', channels_by_group, name="channels_in_group"),
]