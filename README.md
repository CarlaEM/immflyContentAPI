Simple Django API that defines Channels and Contents representing a media service.

The APP containing most of the features is located in /immapi/.
I have also added a "init_test_instances" command to put some dummy data in the db.

The relevant URLs are:
  /channels/ -> fetches all channels
  /channels/<int:id> -> fetches channel with id=id
  /contents/<int:id> -> fetches content with id=id
  /groups/ -> fetches all groups
  /channels/filter/<int:id> -> fetches all contents in a group

You can run the tests with the command:
python manage.py test immapi

And the command for exporting the average rating of every channel is:
python manage.py export_ratings_to_csv

Carla Enrique.
