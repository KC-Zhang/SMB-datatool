from django.shortcuts import redirect, render
from django.http import HttpResponse, FileResponse, HttpResponseRedirect, Http404, StreamingHttpResponse
from django.urls import reverse

def englishRedirect(request):
    return HttpResponseRedirect(reverse('landingPageEn'))


def landingPage(request):
    return render(request, 'landingPage/landingPage.html')
def landingPageCN(request):
    return render(request, 'landingPage/landingPageCN.html')
