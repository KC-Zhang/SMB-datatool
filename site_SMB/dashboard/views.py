from django.shortcuts import render
from django.http import HttpResponse, FileResponse, HttpResponseRedirect, Http404, StreamingHttpResponse
from dashboard.forms import FileUploadForm
from django.template import RequestContext
from dashboard.models import FileModel
from django.urls import reverse
from django.core.files import File
from django.conf import settings
import os
import json
import pandas
from io import BytesIO
from datetime import datetime

# graph-tool Functions
def input_(args, blockIO):
    path = FileModel.objects.filter(fileField__endswith=args['fName'])[0].fileField.path
    blockIO['pd'] = pandas.read_excel(path)
    blockIO['fName'] = args['fName']
    return blockIO
def sort_(args, blockIO):
    blockIO['pd']= blockIO['pd'].sort_values(by=blockIO['pd'].columns[int(args['colNum'])-1], ascending={'ascending':True, 'descending':False}[args['sortOrder']])
    return blockIO
def output_(args,blockIO):
    sio = BytesIO()
    PandasWriter = pandas.ExcelWriter(sio, engine='xlsxwriter')
    pd = blockIO['pd']
    pd.to_excel(PandasWriter, sheet_name='sheet1')
    PandasWriter.save()
    PandasWriter.close()
    workbook = sio.getvalue()
    sio.seek(0)

    response = HttpResponse(workbook,
                                     content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=%s' % datetime.now().strftime("%Y%m%d_%H%M")[2:] +"_"+ blockIO['fName']
    blockIO['res']=response
    return blockIO

graphFuncMap = {
    'inputConfig': input_,
    'sort_': sort_,
    'output_': output_
}

#helper functions
def loadUploadedFiles(request):
    if FileModel.objects.all(): # having existing file
        if request.user.is_authenticated: # logged in user
            fileModels = FileModel.objects.filter(user=request.user)
        else:
            fileModels = FileModel.objects.filter(user=None, session_key=request.session.session_key)
    else:
        fileModels= FileModel.objects.all()
    return fileModels

def checkUserLogin(request):
    # check whether the user is logged in
    loggedIn = False
    if request.user.is_authenticated:
        loggedIn = True
    return loggedIn

def listFiles(request, form=None):
    loggedIn = checkUserLogin(request)
    # load all uploaded files
    fileModels = loadUploadedFiles(request)
    # Render list page with docs and forms
    return render(request,
                  'toolConfigs/input.html',
                  {'fileModels': fileModels, 'loggedIn': int(loggedIn),  'form': form}
                  )

# graph functions:
def runGraph(request):
    userConfigs = json.loads(request.body.decode('utf8').replace("'", '"'))
    blockIO = {'pd': None, 'fName': None, 'res': None}
    for item in userConfigs:
        graphFunction = graphFuncMap[item['func']]
        args = json.loads(item['args'])
        blockIO = graphFunction(args, blockIO)

    return blockIO['res']


# django view
def dashboard(request):
    loggedIn = checkUserLogin(request)
    # load all uploaded files
    fileModels = loadUploadedFiles(request)
    form = FileUploadForm() # A empty, unbound form
    return render(request,
                  'dashboard/dashboard.html',
                  {'fileModels': fileModels, 'form':form, 'loggedIn': int(loggedIn)}
                  )

def uploadFile(request):
    if request.method == 'POST':
        # handle file upload
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():  # check if all fields are filled
            newDoc = FileModel(fileField=request.FILES['fileField'])
            if request.user.is_authenticated:
                newDoc.user=request.user
            else:
                if not request.session.session_key:
                    request.session.save()
                newDoc.session_key=request.session.session_key
            newDoc.save()
        form = FileUploadForm()  # A empty, unbound form

    return listFiles(request)

def deleteFile(request):
    if request.method=='POST':
        # check whether the user is logged in
        if request.user.is_authenticated:  # logged in user
            assert (FileModel.objects.get(pk=request.POST['fileID']).user==request.user)
        else:
            assert (FileModel.objects.get(pk=request.POST['fileID']).user==None)

        FileModel.objects.get(pk=request.POST['fileID']).delete()

    return listFiles(request)
