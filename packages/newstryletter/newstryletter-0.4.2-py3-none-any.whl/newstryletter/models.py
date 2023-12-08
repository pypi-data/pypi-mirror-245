from django.db import models
from django.conf import settings
from django.core.mail import send_mail

# Create your models here.
class Subscriber(models.Model):
    email = models.EmailField(unique=True, default='')
    conf_num = models.CharField(max_length=15, default='')
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.email +(" not " if not self.confirmed else "") + "confirmed)"

class NewsLetter(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    subject = models.CharField(max_length=150)
    contents = models.FileField(upload_to='uploaded_newsletters/')

    def __str__(self):
        return self.subject +" "+ self.created_at.strftime("%B %d, %Y")

    def send(self, request):
        contents = self.contents.read().decode('utf-8')
        subscribers = Subscriber.objects.filter(confirmed=True)

        for sub in subscribers:
            #message = (
            #    subject=self.subject,
            #    contents + (
            #        '<br><a href={}/delete/?email={}&conf_num={}">Unsubscribe</a>.'
            #    ).format(
            #        request.build_absolute_uri('/delete/'),
            #        sub.email,
            #        sub.conf_num),
            #    sub.email,
            #    [settings.FROM_EMAIL])

            send_mail(
                subject=self.subject,
                message=contents + (
                    '<br><a href={}/delete/?email={}&conf_num={}">Unsubscribe</a>.'
                    ).format(
                        request.build_absolute_uri('/delete/'),
                        sub.email,
                        sub.conf_num),
                from_email=settings.FROM_EMAIL,
                recipient_list=[sub.email])
