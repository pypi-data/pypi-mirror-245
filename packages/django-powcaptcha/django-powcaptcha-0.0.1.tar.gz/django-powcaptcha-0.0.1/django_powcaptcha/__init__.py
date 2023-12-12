import django
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

SETTINGS_TYPES = {
    'POWCAPTCHA_API_URL': str,
    'POWCAPTCHA_API_KEY': str,
}

# Validate settings types.
for variable, instance_type in SETTINGS_TYPES.items():
    if hasattr(settings, variable) and not isinstance(
        getattr(settings, variable), instance_type
    ):
        raise ImproperlyConfigured(
            'Setting %s is not of type' % variable, instance_type
        )

if django.VERSION < (3, 2):
    default_app_config = 'django_recaptcha.apps.DjangoRecaptchaConfig'
