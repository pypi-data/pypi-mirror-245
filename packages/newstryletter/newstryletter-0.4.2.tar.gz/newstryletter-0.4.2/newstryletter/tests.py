import unittest
from django.test import TestCase
from django.urls import reverse

# Create your tests here.
from .models import NewsLetter, Subscriber
from .views import delete, confirm
from .forms import SubscriberForm

#class NewsLetterTest(unittest.TestCase):
#    def setUp(self):
#        # Prepara gli oggetti necessari per i test
#        self.newsletter = NewsLetter()
#        self.subscriber = Subscriber('example@example.com')

#    def test_subscribe(self):
#        # Testa la funzione di iscrizione
#        self.newsletter.subscribe(self.subscriber)
#        self.assertIn(self.subscriber, self.newsletter.subscribers)

#    def test_unsubscribe(self):
#        # Testa la funzione di disiscrizione
#        self.newsletter.subscribe(self.subscriber)
#        self.newsletter.unsubscribe(self.subscriber)
#        self.assertNotIn(self.subscriber, self.newsletter.subscribers)

#    def test_send_newsletter(self):
#        # Testa l'invio della newsletter
#        self.newsletter.subscribe(self.subscriber)
#        self.assertTrue(self.newsletter.send_newsletter())

class MyViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_my_view(self):
        # Chiamata alla view 'my_view'
        response = self.client.get(reverse('my_view'))

        # Verifica che la view restituisca lo stato 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Verifica che il nome del progetto sia correttamente passato al template
        project_name = settings.SETTINGS_MODULE.split('.')[0]
        self.assertContains(response, f"Benvenuto su {project_name}")

class SubscriberFormTest(TestCase):
    def test_valid_email(self):
        # Crea un form con un indirizzo email valido
        form_data = {'email': 'test@example.com'}
        form = SubscriberForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_email(self):
        # Crea un form con un indirizzo email non valido
        form_data = {'email': 'email-non-valida'}
        form = SubscriberForm(data=form_data)
        self.assertFalse(form.is_valid())

class NewsLetterDeleteViewTest(TestCase):
    def test_delete_view(self):
        # Crea un oggetto Newsletter di prova
        newsletter = NewsLetter.objects.create(email='test@example.com')

        # Esegui una richiesta HTTP POST per cancellare l'iscrizione
        response = self.delete(reverse('newsletter:delete', args=[newsletter.id]))

        # Verifica che la risposta sia una reindirizzamento alla pagina di elenco delle newsletter
        self.assertRedirects(response, reverse('newsletter:index'))

        # Verifica che l'oggetto Newsletter sia stato effettivamente eliminato dal database
        self.assertFalse(NewsLetter.objects.filter(id=newsletter.id).exists())

class NewsLetterConfirmViewTest(TestCase):
    def test_confirm_view(self):
        # Crea un oggetto Newsletter di prova
        newsletter = NewsLetter.objects.create(email='test@example.com')

        # Esegui una richiesta HTTP GET per confermare l'iscrizione
        response = self.confirm(reverse('newsletter:confirm', args=[newsletter.id]))

        # Verifica che la risposta sia una pagina HTML con lo status code 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Verifica che l'oggetto Newsletter passato al template sia lo stesso dell'oggetto di prova
        self.assertEqual(response.context['newsletter'], newsletter)


