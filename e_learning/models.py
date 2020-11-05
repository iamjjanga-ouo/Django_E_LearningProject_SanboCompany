from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
import uuid
from datetime import date

class Major(models.Model):
    name = models.CharField(
        max_length = 100,
        help_text="Enter a major (e.g. Computer Science, Electronic Science, etc.)"
    )

    def __str__(self):
        return self.name

class Language(models.Model):
    name = models.CharField(max_length=200, help_text="Enter the lecture's language (e.g. English, Korean, Japanese etc.)")

    def __str__(self):
        return self.name

class Lecture(models.Model):
    title = models.CharField(max_length=200)
    professor = models.ForeignKey('Professor', on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=1000, help_text="Enter a brief descriptiuon of the book")
    major = models.ForeignKey('Major', on_delete=models.SET_NULL, null=True)
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)

    def get_absolute_url(self):
        return reverse('lecture-detail', args=[str(self.id)])

    def __str__(self):
        return self.name

class Assignment(models.Model):
    name = models.CharField(max_length=200)
    due_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name


class OpenLecture(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                             help_text="Unique ID for this particular lecture across whole website")
    lecture = models.ForeignKey('Lecture', on_delete=models.SET_NULL, null=True)
    assignment = models.ForeignKey('Assignment', on_delete=models.SET_NULL, null=True)
    remain_time = models.DateField(null=True, blank=True)
    enroll_student = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def is_overdue(self):
        if self.remain_time and date.today() > self.remain_time:
            return True
        return False

    LECTURE_STATUS = (
        ('o', 'Opened'),
        ('c', 'Closed'),
        ('s', 'Streaming'),
        ('e', 'Exam'),
    )

    status = models.CharField(
        max_length=1,
        choices=LECTURE_STATUS,
        blank=True,
        default='o',
        help_text='Lecture is Opened now. You can take VOD Service.'
    )

    class Meta:
        ordering = ['remain_time']
        permissions = (("can_modified_remain_time", "Set remain time"),)

    def __str__(self):
        return '{0} ({1})'.format(self.id, self.lecture.title)

class Professor(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    major = models.ForeignKey('Major', on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        return reverse('professor-detail', args=[str(self.id)])

    def __str__(self):
        return '{0}, {1}'.format(self.last_name, self.first_name)