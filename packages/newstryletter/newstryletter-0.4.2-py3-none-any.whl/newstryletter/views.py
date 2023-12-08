import random
from django.core.mail import send_mail

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.conf import settings

try:
    from .settings import GOOGLE_RECAPTCHA_PUBLIC_KEY, GOOGLE_RECAPTCHA_SECRET_KEY, RECEIVE_EMAIL
except Exception as e:
    print(f'Error type is: {e}')

# from .models import Subscriber
from .forms import SubscriberForm
from .models import NewsLetter, Subscriber

# implement this utility -> @
from .decorators import newsletter_captcha

# Helper Functions
def random_digits():
    return "%0.12d" % random.randint(0, 999999999999)

def project_name():

    project_name = settings.SETTINGS_MODULE.split('.')[0]
    context = {'project_name': project_name}
    return context


#@csrf_exempt
@newsletter_captcha
def new(request):
    if request.method == 'POST':
        # RRFACTOR: may be can i sue directly the form  here?
        is_good_email = request.POST.get('email')
        try:
            validate_email(is_good_email)
        except ValidationError:
            messages.error(request, 'Inserisci un indirizzo email valido.')

        form = SubscriberForm(request.POST)
        recaptcha_response = request.POST.get('g-recaptcha-response')

        if form.is_valid() and request.recaptcha_is_valid:
            # Verifica @email
            email = request.POST.get('email')
            #if not is_email_unique(email):
            #    messages.error(request, 'This email address is already in use. Please use a different email address.')
            #    return render(request, 'newsletter/index.html',
            #                  {'form': form,
            #                   'public_captcha': GOOGLE_RECAPTCHA_PUBLIC_KEY})

            newsletter = Subscriber(email=request.POST['email'], conf_num=random_digits())
            newsletter.save()

            subject ='Newsletter Confirmation'
            msg =('Thank you for signing up for my email newsletter! ' \
                   'Please complete the process by ' \
                   '{}confirm/?email={}&conf_num={} clicking here to ' \
                   'confirm your registration.'.format(request.build_absolute_uri('/newsletter/'),
                                                        newsletter.email,
                                                        newsletter.conf_num))
            from_email = newsletter.email
            recipient_list = [RECEIVE_EMAIL]

            response = send_mail(subject,
                                 msg,
                                 from_email,
                                 [RECEIVE_EMAIL],
                                 #[from_email],
                                 fail_silently=False)

            return redirect('newsletter:new')

        else:
            form = SubscriberForm()
            return render(request, 'newsletter/index.html',
                          {'form': form,
                           'public_captcha': GOOGLE_RECAPTCHA_PUBLIC_KEY,
                           'error_message': 'Invalid reCAPTCHA. Please try againinnnn.'})

    form = SubscriberForm()
    context = project_name()
    return render(request,
                    'newsletter/index.html',
                    {'form': form,
                     'context': context,
                     'public_captcha': GOOGLE_RECAPTCHA_PUBLIC_KEY})

def confirm(request):
    newsletter = Subscriber.objects.get(email=request.GET['email'])
    if newsletter.conf_num == request.GET['conf_num']:
        newsletter.confirmed = True
        newsletter.save()

        return render(request,
                      'newsletter/index.html',
                      {'email': newsletter.email,
                      'public_captcha': GOOGLE_RECAPTCHA_PUBLIC_KEY,
                      'action':'confirmed'})
    else:
        return render(request,
                      'newsletter/index.html',
                      {'email': newsletter.email,
                       'action':'denied'})

def delete(request):
    newsletter = Subscriber.objects.get(email=request.GET['email'])
    if newsletter.conf_num == request.GET['conf_nun']:
        newsletter.delete()

        return render(request,
                      'newsletter/index.html',
                      {'email': newsletter.email,
                      'public_captcha': GOOGLE_RECAPTCHA_PUBLIC_KEY,
                      'action':'you are unsuvscribed!'})
    else:
        return render(request,
                      'newsletter/index.html',
                      {'email': newsletter.email,
                      'public_captcha': GOOGLE_RECAPTCHA_PUBLIC_KEY,
                      'action':'denied subscription'})

def is_email_unique(email):
    # Funzione per verificare se l'indirizzo email è unico nel database
    # Adatta la query in base al modello di dati e al campo email
    from .models import Subscriber
    try:
        subscriber = Subscriber.objects.get(email=email)
        return False  # L'indirizzo email esiste già nel database
    except Subscriber.DoesNotExist:
        return True  # L'indirizzo email è unico

def is_recaptcha_valid(response):
    import requests
    data = {
        'secret': GOOGLE_RECAPTCHA_SECRET_KEY,
        'response': response
    }
    r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
    result = r.json()
    return result.get('success', False)
