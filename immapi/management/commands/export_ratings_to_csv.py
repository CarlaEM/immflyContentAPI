import csv
import os
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.models import Avg
from immapi.models import Channel, Content

class Command(BaseCommand):
    help = 'Export a CSV with every channel and the average rating of all its content'

    def handle(self, *args, **options):
        # Get all channels and preparece Contents
        channels = Channel.objects.prefetch_related('contents', 'sub_channels')

        if not channels.exists():
            self.stdout.write(self.style.WARNING('No channels found'))
            return

        # Create a dictionary using the channel's id as keys and it's rating as value
        ch_dict_ratings = {}

        def calculate_channel_rating(c):
            if c.id in ch_dict_ratings:
                return ch_dict_ratings[c.id]

            contents = c.contents.all()
            sub_channels = c.sub_channels.all()

            rating = 0
            if contents.exists():
                # Get average ratings of all child Content
                rating = contents.aggregate(avg_rating=Avg('rating'))['avg_rating'] or 0
            elif sub_channels.exists():
                # Get average ratings of all sub Channels
                # use a dictionary and recursion to only compute once for channel
                for sub_channel in sub_channels:
                    if not sub_channel.id in ch_dict_ratings:
                        ch_dict_ratings[sub_channel.id] = calculate_channel_rating(sub_channel)
                    rating = rating + ch_dict_ratings[sub_channel.id]
                rating = rating / len(sub_channels)

            ch_dict_ratings[c.id] = rating
            return rating

        # Fill the dictionary
        for channel in channels:
            if not channel.id in ch_dict_ratings:
                calculate_channel_rating(channel)
        
        # Sort the dictionary by rating
        channels = sorted(channels, key= lambda c: ch_dict_ratings[c.id], reverse= True)
        
        # Export to CSV
        filename = os.path.join(settings.BASE_DIR, 'channels_export.csv')
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Title', 'Rating'])

            # Write row by row
            for channel in channels:               
                writer.writerow([channel.title, f"{ch_dict_ratings[channel.id]:.2f}"])