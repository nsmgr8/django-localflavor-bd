"""
Bangladesh-specific Form helpers
"""

from django.core.validators import EMPTY_VALUES
from django.forms import ValidationError
from django.forms.fields import Field, RegexField, Select
from django.utils.encoding import smart_unicode
from django.utils.translation import ugettext_lazy as _
import re


class BDPostCodeField(RegexField):
    """Bangladesh post code field."""
    default_error_messages = {
        'invalid': _('Enter a 4 digit post code.'),
    }

    def __init__(self, *args, **kwargs):
        super(BDPostCodeField, self).__init__(r'^\d{4}$',
            max_length=None, min_length=None, *args, **kwargs)

class BDPhoneNumberField(Field):
    """Bangladesh phone number field."""
    PHONE_DIGITS_RE = re.compile(r'^(\d{8,13})$')

    default_error_messages = {
        'invalid': _(u'Phone numbers must be between 8 to 13 digits.'),
    }

    def clean(self, value):
        """
        Validate a phone number. Strips parentheses, whitespace and hyphens.
        """
        super(BDPhoneNumberField, self).clean(value)
        if value in EMPTY_VALUES:
            return u''
        value = re.sub('(\(|\)|\s+|-)', '', smart_unicode(value))
        phone_match = self.PHONE_DIGITS_RE.search(value)
        if phone_match:
            return u'%s' % phone_match.group(1)
        raise ValidationError(self.error_messages['invalid'])

class BDDivisionSelect(Select):
    """
    A Select widget that uses a list of Bangladesh divisions as its choices.
    """
    def __init__(self, attrs=None):
        from bd_divisions import DIVISION_CHOICES
        super(BDDivisionSelect, self).__init__(attrs, choices=DIVISION_CHOICES)

class BDDistrictSelect(Select):
    """
    A Select widget that uses a list of Bangladesh districts as its choices
    """
    def __init__(self, attrs=None):
        from bd_divisions import DISTRICT_CHOICES
        super(BDDistrictSelect, self).__init__(attrs, choices=DISTRICT_CHOICES)

class BDUpazilaSelect(Select):
    """
    A Select widget that uses a list of Bangladesh upazilas as its choices.
    """
    def __init__(self, attrs=None):
        from bd_divisions import UPAZILLA_CHOICES
        super(BDUpazilaSelect, self).__init__(attrs, choices=UPAZILLA_CHOICES)

