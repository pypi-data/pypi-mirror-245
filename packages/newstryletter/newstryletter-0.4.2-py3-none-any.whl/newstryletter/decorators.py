import requests
from functools import wraps

try:
    from .settings import GOOGLE_RECAPTCHA_SECRET_KEY
except Exception as e:
    print(f'Error type is: {e}')

from django.contrib import messages

def newsletter_captcha(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        request.recaptcha_is_valid = None
        if request.method == 'POST':
            recaptcha_response = request.POST.get('g-recaptcha-response')
            data = {
                'secret': GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
            result = r.json()
            if result['success']:
                request.recaptcha_is_valid = True
                # utilizzo error message per non colorare avviso
                messages.error(request, 'Richiesta inviata correttamente.')
            else:
                request.recaptcha_is_valid = False
                messages.error(request, 'Invalid reCAPTCHAAAAA. Please try again.')

        return view_func(request, *args, **kwargs)
    return _wrapped_view
