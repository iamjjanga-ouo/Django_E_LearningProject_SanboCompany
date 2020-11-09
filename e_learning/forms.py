import datetime

from django import forms
from .models import LectureInstance
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

class RenewLectureForm(forms.Form):
    renewal_date = forms.DateField(help_text="Enter a date between now and 2 weeks (default 3).")

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']

        # Check if a date is not in the past.
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))

        # Check if a date is in the allowed range (+2 weeks from today).
        if data > datetime.date.today() + datetime.timedelta(weeks=2):
            raise ValidationError(_('Invalid date - renewal more than 2 weeks ahead'))

        # Remember to always return the cleaned data.
        return data