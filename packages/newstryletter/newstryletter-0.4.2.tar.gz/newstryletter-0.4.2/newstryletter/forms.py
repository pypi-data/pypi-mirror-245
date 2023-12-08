#from django import forms

#class SubscriberForm(forms.Form):
#    email = forms.EmailField(label='Your email',
#                             max_length=100,
#                             widget=forms.EmailInput(attrs={'class': 'form-control'}))


from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from .models import Subscriber  # Se hai un modello per gli iscritti

class SubscriberForm(forms.Form):
    email = forms.EmailField(label='Your email', max_length=100, widget=forms.EmailInput(attrs={'class': 'form-control'}))

    def clean_email(self):
        email = self.cleaned_data['email']

        # Verifica se l'indirizzo email è univoco nel tuo database
        if Subscriber.objects.filter(email=email).exists():
            raise ValidationError('This email address is already in use. Please use a different email address.')

        # Verifica se l'indirizzo email è valido utilizzando il modulo validate_email di Django
        try:
            validate_email(email)
        except ValidationError:
            raise ValidationError('Please enter a valid email address.')

        # Puoi aggiungere altre regole specifiche qui, ad esempio:
        # if not email.endswith('example.com'):
        #     raise ValidationError('Only email addresses from example.com domain are allowed.')

        return email

