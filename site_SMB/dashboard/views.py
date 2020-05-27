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

# graph-tool Functions
def input_(args, pdFile):
    path = FileModel.objects.filter(fileField__endswith=args['fName'])[0].fileField.path
    pdFile = pandas.read_excel(path)
    pdFile.fileName = args['fName']
    return pdFile
def sort_(args, pdFile):
    pdFile.sort_values(by=pdFile.columns[int(args['colNum'])-1], ascending={'ascending':True, 'descending':False}[args['sortOrder']])
    return pdFile
def output_(args,pdFile):
    sio = BytesIO()
    PandasWriter = pandas.ExcelWriter(sio, engine='xlsxwriter')
    pdFile.to_excel(PandasWriter, sheet_name='sheet1')
    PandasWriter.save()
    PandasWriter.close()
    workbook = sio.getvalue()
    sio.seek(0)

    response = FileResponse(workbook,
                                     content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=%s' % pdFile.fileName
    return response
    # saveName='modified_'+pdFile.fileName
    # file_path = os.path.join(settings.MEDIA_ROOT, saveName)
    # pdFile.to_excel(file_path)
    # if os.path.exists(file_path):
    #     with open(file_path, 'rb') as f:
    #         # allow download
    #         response = HttpResponse(f.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    #         response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
    #         return response
    # raise Http404()

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
    userConfigs = json.loads(request.POST['userConfigs'])
    pdFile=None
    for item in userConfigs:
        graphFunction = graphFuncMap[item['func']]
        args = json.loads(item['args'])
        pdFile = graphFunction(args, pdFile)

    return pdFile