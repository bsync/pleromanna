from django.db import models as djmods
from wagtail.admin.edit_handlers import FieldPanel
from wagtailmedia.models import AbstractMedia
from wagtail.core.fields import RichTextField
from django.utils.timezone import now

import os


class Series(djmods.Model):
    collection = djmods.ForeignKey(
                'wagtailcore.collection',
                null=True, blank=True,
                on_delete=djmods.SET_NULL)
    title = djmods.CharField(max_length=250)
    start_date = djmods.DateField(default=now)
    stop_date = djmods.DateField(null=True, blank=True)
    description = RichTextField(blank=True)

    panels = [
        FieldPanel('title'),
        FieldPanel('start_date'),
        FieldPanel('stop_date'),
        FieldPanel('description'),
    ]


class SubSeries(djmods.Model):
    series = djmods.ForeignKey(
                'Series',
                null=True, blank=True,
                on_delete=djmods.SET_NULL)
    title = djmods.CharField(max_length=250)
    start_date = djmods.DateField(default=now)
    stop_date = djmods.DateField(null=True, blank=True)
    description = RichTextField(blank=True)


class PleroMedia(AbstractMedia):

    duration = djmods.PositiveIntegerField(null=True,
                                           blank=True,
                                           verbose_name='duration',
                                           help_text='Duration in seconds')
    series = djmods.ForeignKey(
        'Series', null=True, blank=True,
        on_delete=djmods.SET_NULL,
        related_name='+')

    subseries = djmods.ForeignKey(
        'SubSeries', null=True, blank=True,
        on_delete=djmods.SET_NULL,
        related_name='+')

    def process(self, name):
        return os.path.join(self.series.collection.name, self.series, name)
    file = djmods.FileField(upload_to=process, verbose_name='file')

    admin_form_fields = (
        'title',
        'file',
        'series',
        'tags',)

    def clean(self):
        cleaned_data = super().clean()
        # Make sure that the event starts before it ends
        # start_date = cleaned_data['start_date']
        # end_date = cleaned_data['end_date']
        # if start_date and end_date and start_date > end_date:
        # self.add_error('end_date', 'The end date must be after start # date')
        return cleaned_data

    def save(self, *args, **kwargs):

        # Update the duration field
        # import cv2
        # import pdb; pdb.set_trace()
        # cap = cv2.VideoCapture(self.file)
        # self.count = cap.get(cv2.CV_CAP_PROP_FRAME_COUNT)
        # self.fps = cap.get(cv2.CV_CAP_PROP_FPS)
        # self.duration = self.count/self.fps
        # self.width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        # self.height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        # cap.release()

        return super().save(*args, **kwargs)

