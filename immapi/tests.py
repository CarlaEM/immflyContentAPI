import os
import csv
import json
from django.conf import settings
from django.core.management import call_command
from django.test.utils import override_settings
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from .models import Content, Channel, Group

# Create your tests here.

def set_up_test_data(context):
    context.channel1 = Channel.objects.create(title="Main")
    context.channel2 = Channel.objects.create(title="Sub1")
    context.channel3 = Channel.objects.create(title="Sub2")

    content_sub11 = Content.objects.create(id=11, title="Content11", metadata={}, rating="3.0")
    content_sub12 = Content.objects.create(id=12, title="Content12", metadata={}, rating="4.0")
    context.channel2.contents.add(content_sub11, content_sub12)

    content_sub21 = Content.objects.create(id=21, title="Content21", metadata={}, rating="7.0")
    content_sub22 = Content.objects.create(id=22, title="Content22", metadata={"author": "Jane Doe"}, rating="8.0")
    content_sub23 = Content.objects.create(id=23, title="Content23", metadata={}, rating="9.0")
    context.channel3.contents.add(content_sub21, content_sub22, content_sub23)

    context.channel1.sub_channels.add(context.channel2, context.channel3)

    context.group1 = Group.objects.create(title="Group1")
    context.group2 = Group.objects.create(title="Group2")
    context.group1.channels.add(context.channel1, context.channel2)
    context.group2.channels.add(context.channel1)

class ChannelExportTestCase(TestCase):
    def setUp(self):
        set_up_test_data(self)

    @override_settings(BASE_DIR=os.path.dirname(__file__))
    def test_csv_export(self):
        filename = os.path.join(settings.BASE_DIR, 'channels_export.csv')
        call_command('export_ratings_to_csv')

        # Check if CSV file was created
        self.assertTrue(os.path.exists(filename))

        expected_sorted_ratings = {
            self.channel3.title: 8.0,
            self.channel1.title: 5.75,
            self.channel2.title: 3.5,
        }

        # Read and validate the CSV content
        with open(filename, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            header = next(reader)
            self.assertEqual(header, ['Title', 'Rating'])

            data = list(reader)
            self.assertEqual(len(data), 3)

            # Check each channel entry
            for row in data:
                title, rating = row
                title = str(title)
                rating = float(rating)
                
                self.assertAlmostEqual(rating, expected_sorted_ratings[title], places=2)

        os.remove(filename)

class AllChannelsEndpointTestCase(TestCase):
    # Test /channels/ URL
    def setUp(self):
        set_up_test_data(self)

    def test_all_channel_endpoint(self):
        url = reverse('all_channels')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        json_data = json.loads(response.content)
        self.assertEqual(len(json_data), 3)
        
        # Validate the structure and content of all the channels
        channel_data = json_data[0]
        self.assertEqual(channel_data['title'], "Main")
        self.assertEqual(channel_data['sub_channels'], [2, 3])

        channel_data = json_data[1]
        self.assertEqual(channel_data['title'], "Sub1")
        self.assertEqual(channel_data['contents'], [11, 12])

        channel_data = json_data[2]
        self.assertEqual(channel_data['title'], "Sub2")
        self.assertEqual(channel_data['contents'], [21, 22, 23])

class ChannelByIdEndpointTestCase(TestCase):
    # Test /channels/<id> URL
    def setUp(self):
        set_up_test_data(self)

    def test_channel_endpoint(self):
        url = reverse('channel_by_id', kwargs={'id':2})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        json_data = json.loads(response.content)
        
        # Validate the structure and content of the fetched channel
        channel_data = json_data
        self.assertEqual(json_data['title'], "Sub1")
        self.assertEqual(json_data['contents'], [11, 12])

class ContentByIdEndpointTestCase(TestCase):
    # Test /contents/<id> URL
    def setUp(self):
        set_up_test_data(self)

    def test_content_endpoint(self):
        url = reverse('content_by_id', kwargs={'id':22})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        json_data = json.loads(response.content)
        
        # Validate the structure and content of the fetched channel
        channel_data = json_data
        self.assertEqual(json_data['title'], "Content22")
        self.assertEqual(json_data['rating'], "8.00")
        self.assertEqual(json_data['metadata']['author'], "Jane Doe")

class AllGroupsEndpointTestCase(TestCase):
    # Test /groups/ URL
    def setUp(self):
        set_up_test_data(self)

    def test_all_channel_endpoint(self):
        url = reverse('all_groups')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        json_data = json.loads(response.content)
        self.assertEqual(len(json_data), 2)
        
        # Validate the structure and content of all the groups
        group_data = json_data[0]
        self.assertEqual(group_data['title'], "Group1")
        self.assertEqual(group_data['channels'], [1, 2])

        group_data = json_data[1]
        self.assertEqual(group_data['title'], "Group2")
        self.assertEqual(group_data['channels'], [1])

class ChannelsByGroupEndpointTestCase(TestCase):
    # Test /channels/filter/<int:id> URL
    def setUp(self):
        set_up_test_data(self)

    def test_all_channel_endpoint(self):
        url = reverse('channels_in_group', kwargs={'id':1})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        json_data = json.loads(response.content)
        
        # Validate the structure and content of the group
        channel_data = json_data[0]
        self.assertEqual(channel_data['title'], "Main")
        self.assertEqual(channel_data['sub_channels'], [2, 3])

        channel_data = json_data[1]
        self.assertEqual(channel_data['title'], "Sub1")
        self.assertEqual(channel_data['contents'], [11, 12])