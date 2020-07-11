from django.shortcuts import redirect, render
from django.http import HttpResponse, FileResponse, HttpResponseRedirect, Http404, StreamingHttpResponse
from django.urls import reverse
from django.db.utils import IntegrityError
from landingPage.forms import SubscriberEmailAddressForm
from landingPage.models import SubscriberEmailAddressModel

def englishRedirect(request):
    return HttpResponseRedirect(reverse('landingPageEn'))
def landingPage(request):
    emailAddressForm = SubscriberEmailAddressForm
    return render(request, 'landingPage/landingPage.html',{'emailAddressForm':emailAddressForm})
def landingPageCN(request):
    emailAddressForm = SubscriberEmailAddressForm
    return render(request, 'landingPage/landingPageCN.html', {'emailAddressForm':emailAddressForm})
def subscribe(request):
    if request.method == 'POST':
        form = SubscriberEmailAddressForm(request.POST)
        if form.is_valid():
            emailAddress = form.cleaned_data['subscriberEmailAddressField']
            emailAddressModel = SubscriberEmailAddressModel(emailField=emailAddress)
            try:
                emailAddressModel.save()
                return HttpResponse("Thank you signing up!")
            except IntegrityError:
                return HttpResponse("Email already signed up. Thank you!")

        return HttpResponse(form.errors['subscriberEmailAddressField'][0])

