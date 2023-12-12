# Django PowCaptcha

Django PowCaptcha form field/widget integration app.

## Installation

1. Install with `pip install django-powcaptcha`.

2. Add `'django_powcaptcha'` to your `INSTALLED_APPS` setting.

```python
INSTALLED_APPS = [
    ...,
    'django_powcaptcha',
    ...
]
```

3. Add settings.

For example:

```python
POWCAPTCHA_API_URL = 'https://captcha.yourdomain.com'
POWCAPTCHA_API_KEY = 'MyPOWCAPTCHAPrivateKey456'
```

## Usage

### Fields

The quickest way to add PowCaptcha to a form is to use the included
`PowCaptchaField` field class. For example:

```python
from django import forms
from django_powcaptcha.fields import PowCaptchaField

class FormWithCaptcha(forms.Form):
    captcha = PowCaptchaField()
```
