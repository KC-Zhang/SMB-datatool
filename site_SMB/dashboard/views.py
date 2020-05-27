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
    'input_': input_,
    'sort_': sort_,
    'output_': output_
}

# django functions
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

def runGraph(request):
    userConfigs = json.loads(request.body.decode('utf8').replace("'", '"'))
    blockIO = {'pd': None, 'fName': None, 'res': None}
    for item in userConfigs:
        graphFunction = graphFuncMap[item['func']]
        args = json.loads(item['args'])
        blockIO = graphFunction(args, blockIO)

    return blockIO['res']