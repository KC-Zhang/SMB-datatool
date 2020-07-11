from django import forms

class SubscriberEmailAddressForm(forms.Form):
    subscriberEmailAddressField = forms.EmailField(
        help_text='E-mail',
        error_messages={'required': 'Please provide your email address.',
                        'unique': 'An account with this email exist.'},
    )