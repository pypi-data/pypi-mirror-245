import logging

from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from django_powcaptcha import client
from django_powcaptcha.client import PowCaptchaValidationException
from django_powcaptcha.widgets import PowCaptchaWidget

logger = logging.getLogger(__name__)


class PowCaptchaField(forms.CharField):
    widget = PowCaptchaWidget
    default_error_messages = {
        'captcha_invalid': _('Error verifying reCAPTCHA, please try again.'),
        'captcha_error': _('Error verifying reCAPTCHA, please try again.'),
    }

    def __init__(self, api_key=None, api_url=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.required = True

        # Setup instance variables.
        self.api_key = api_key or getattr(settings, 'POWCAPTCHA_API_KEY')
        self.api_url = api_url or getattr(settings, 'POWCAPTCHA_API_URL')

    def validate(self, value):
        super().validate(value)

        try:
            client.validate_captcha(
                challenge='',
                nonce='',
            )
        except PowCaptchaValidationException:
            raise ValidationError(
                self.error_messages['captcha_error'], code='captcha_error'
            )
