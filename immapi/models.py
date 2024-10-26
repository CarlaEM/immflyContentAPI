from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class Content(models.Model):
    title = models.CharField(max_length=255)
    metadata = models.JSONField()
    rating = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    media = models.FileField()

    def __str__(self):
        return self.title

class Channel(models.Model):
    title = models.CharField(max_length=255)
    language = models.CharField(max_length=255)
    cover = models.ImageField()
    sub_channels = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='parents',
        blank=True
    )
    contents = models.ManyToManyField(
        Content,
        symmetrical=False,
        related_name='parent_channels',
        blank=True
    )

    def clean(self):
        if not self.id:
            return 
        
        if (self.contents.exists() and self.sub_channels.exists()) or ((not self.contents.exists()) and (not self.sub_channels.exists())):
            raise ValidationError("A channel can contain either contents or sub_channels, but not both. And one of them must be not empty")

    def save(self, *args, **kwargs):
        # Enforce clean
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    
class Group(models.Model):
    title = models.CharField(max_length=255)
    channels = models.ManyToManyField(Channel, related_name='groups', blank=False)

    def clean(self):
        if not self.id:
            return 
        
        #if (self.channels.exists()):
        #    raise ValidationError("A group must contain at least one channel")
        
    def save(self, *args, **kwargs):
        # Enforce clean
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
