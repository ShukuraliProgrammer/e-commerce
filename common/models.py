from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator, URLValidator, RegexValidator
from django.core.exceptions import ValidationError

class Media(models.Model):
    class MediaType(models.TextChoices):
        IMAGE = "image", _("Image")
        FILE = "file", _("File")
        MUSIC = "music", _("Music")
        VIDEO = "video", _("video")

    file = models.FileField(_("File"), upload_to="files/", validators=[
        FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif', 'mp4', 'mp3', 'flac', 'doc', 'pdf'])], null=True, blank=True)
    type = models.CharField(_("Type"), max_length=60, choices=MediaType.choices)

    def __str__(self):
        return str(self.id) + " " + str(self.file.name.split("/")[-1])

    def clean(self):
        if self.type == self.MediaType.IMAGE:
            if not self.file.name.endswith(('.jpg', '.jpeg', '.png')):
                raise ValidationError("File type is not image")
        elif self.type == self.MediaType.FILE:
            if not self.file.name.endswith(('.doc', '.pdf')):
                raise ValidationError("File type is not document")
        elif self.type == self.MediaType.MUSIC:
            if not self.file.name.endswith(('.mp3', '.flac')):
                raise ValidationError("File type is not music")
        elif self.type == self.MediaType.VIDEO:
            if not self.file.name.startwith('.mp4'):
                raise ValidationError("File type is not video")
        else:
            raise ValidationError("File type is not valid")

class Settings(models.Model):
    home_image = models.ForeignKey(Media, on_delete=models.SET_NULL, null=True, blank=True)
    home_title = models.CharField(_("Title"), max_length=120)
    home_subtitle = models.CharField(_("Subtitle"), max_length=120)

    def __str__(self):
        return self.home_title


class Country(models.Model):
    name = models.CharField(_("Name"), max_length=120)
    code = models.CharField(_("Code"), max_length=2)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Country")
        verbose_name_plural = _("Countries")


class Region(models.Model):
    name = models.CharField(_("Name"), max_length=120)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="regions")

    def __str__(self):
        return self.name


class OurInstagramStory(models.Model):
    image = models.ForeignKey(Media, on_delete=models.CASCADE, related_name="instagram_stories")
    story_link = models.URLField(_("Story Link"), validators=[URLValidator()])  # TODO: WRITE VALIDATOR FOR INSTAGRAM URL

    def __str__(self):
        return f"Id: {self.id}|Link: {self.story_link}"


class CustomerFeedback(models.Model):
    description = models.TextField(_("Review"))
    rank = models.IntegerField(_("Rank"))
    customer_name = models.CharField(_("Customer Name"), max_length=80)
    customer_position = models.CharField(_("Customer Position"), max_length=60)
    customer_image = models.ForeignKey(Media, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.customer_name
