from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from dashboard.forms import FileUploadForm
from django.template import RequestContext
from dashboard.models import FileModel
from django.urls import reverse

def listFiles(request):
    if request.method == 'POST':
        # handle file upload
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():  # check if all fields are filled
            newDoc = FileModel(fileField=request.FILES['fileField'])
            newDoc.save()
            # re-direct to doc list
            return HttpResponseRedirect(reverse('dashboard'))
    else:
        form = FileUploadForm() # A empty, unbound form

    # load all uploaded files
    fileModels = FileModel.objects.all()

    # Render list page with docs and forms
    return render(request,
        'dashboard/fileList.html',
        {'fileModels': fileModels, 'form': form}
    )
