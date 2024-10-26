from django.core.management.base import BaseCommand
from immapi.models import Channel, Content, Group

class Command(BaseCommand):
    help = 'Create test instances'

    def handle(self, *args, **options):
        Channel.objects.all().delete()
        Content.objects.all().delete()
        Group.objects.all().delete()

        movies_ch = Channel.objects.create(
            title="Movies",
            language="English"
        )
        shows_ch = Channel.objects.create(
            title="Shows",
            language="English"
        )
        tgp_ch = Channel.objects.create(
            title="The Good Place",
            language="English"
        )
        house_ch = Channel.objects.create(
            title="House",
            language="English"
        )
        hillhouse_ch = Channel.objects.create(
            title="The Haunting of Hill House",
            language="English"
        )

        alien_c = Content.objects.create(
            title="Alien",
            metadata={
                "Authors": ["Ridley Scott"],
                "Genre": "Horror",
                "Description": "After investigating a mysterious transmission of unknown origin, the crew of a commercial spacecraft encounters a deadly lifeform."
            },
            rating=8.5
        )

        scream_c = Content.objects.create(
            title="Scream",
            metadata={
                "Authors": ["Wes Craven", "Kevin Williamson"],
                "Genre": "Horror",
                "Description": "A year after the murder of her mother, a teenage girl is terrorized by a masked killer who targets her and her friends by using scary movies as part of a deadly game."
            },
            rating=7.4
        )

        tgp_chapter_1 = Content.objects.create(
            title="The Good Place 1",
            metadata={
                "Authors": ["Michael Schur"],
                "Genre": "Comedy",
                "Description": "Four people and their otherworldly frienemy struggle in the afterlife to define what it means to be good."
            },
            rating=7.9
        )

        tgp_chapter_2 = Content.objects.create(
            title="The Good Place 2",
            metadata={
                "Authors": ["Michael Schur"],
                "Genre": "Comedy",
                "Description": "Four people and their otherworldly frienemy struggle in the afterlife to define what it means to be good."
            },
            rating=7.4
        )

        house_chapter_1 = Content.objects.create(
            title="House 1",
            metadata={
                "Authors": ["David Shore"],
                "Genre": "Medical Drama",
                "Description": "Using a crack team of doctors and his wits, an antisocial maverick doctor specializing in diagnostic medicine does whatever it takes to solve puzzling cases that come his way."
            },
            rating=8.4
        )

        house_chapter_2 = Content.objects.create(
            title="House 2",
            metadata={
                "Authors": ["David Shore"],
                "Genre": "Medical Drama",
                "Description": "Using a crack team of doctors and his wits, an antisocial maverick doctor specializing in diagnostic medicine does whatever it takes to solve puzzling cases that come his way."
            },
            rating=8.1
        )

        house_chapter_3 = Content.objects.create(
            title="House 3",
            metadata={
                "Authors": ["David Shore"],
                "Genre": "Medical Drama",
                "Description": "Using a crack team of doctors and his wits, an antisocial maverick doctor specializing in diagnostic medicine does whatever it takes to solve puzzling cases that come his way."
            },
            rating=8.1
        )

        hhh_chapter_1 = Content.objects.create(
            title="The Haunting of Hill House 1",
            metadata={
                "Authors": ["David Shore"],
                "Genre": "Medical Drama",
                "Description": "Using a crack team of doctors and his wits, an antisocial maverick doctor specializing in diagnostic medicine does whatever it takes to solve puzzling cases that come his way."
            },
            rating=8.1
        )

        group_1 = Group.objects.create(title="Recommended")
        group_1.channels.add(house_ch, tgp_ch)
        
        group_2 = Group.objects.create(title="Generic")
        group_2.channels.add(movies_ch, house_ch, hillhouse_ch)

        contents = [alien_c, scream_c, tgp_chapter_2, tgp_chapter_1, house_chapter_1, house_chapter_2, house_chapter_3]
        for content in contents:
            content.save()

        movies_ch.contents.add(scream_c, alien_c)
        shows_ch.sub_channels.add(tgp_ch, house_ch)
        tgp_ch.contents.add(tgp_chapter_1, tgp_chapter_2)
        house_ch.contents.add(house_chapter_1, house_chapter_2, house_chapter_3)
        hillhouse_ch.contents.add(hhh_chapter_1)

        channels = [movies_ch, shows_ch, tgp_ch, house_ch, hillhouse_ch]
        for channel in channels:
            channel.save()

        groups = [group_1, group_2]
        for group in groups:
            group.save()