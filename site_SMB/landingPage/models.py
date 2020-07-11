from django.db import models

# Create your models here.
class SubscriberEmailAddressModel(models.Model):
    emailField = models.EmailField(max_length=254, blank=False, unique=True,
                                   error_messages={'required': 'Please provide your email address.',
                                                   'unique': 'An account with this email exist.'}, )