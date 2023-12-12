from django.conf import settings
from django.forms import widgets

from django_powcaptcha.client import get_challenge


class PowCaptchaWidget(widgets.Widget):
    input_type = 'hidden'
    template_name = 'django_recaptcha/widget.html'

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context.update(
            {
                'captcha_url': settings.POWCAPTCHA_API_URL,
                'captcha_challenge': get_challenge(),
                'captcha_callback': 'myCaptchaCallback',
            }
        )
        return context

    # def build_attrs(self, base_attrs, extra_attrs=None):
    #     attrs = super().build_attrs(base_attrs, extra_attrs)
    #     attrs['data-sqr-captcha-url'] = settings.POWCAPTCHA_API_URL
    #     attrs['data-sqr-captcha-challenge'] = self.get_challenge()
    #     attrs['data-sqr-captcha-callback'] = 'myCaptchaCallback'
    #     return attrs
