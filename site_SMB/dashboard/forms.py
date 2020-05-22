from django import forms

class FileUploadForm(forms.Form):
    fileField = forms.FileField(
        label='Upload a xlsx file',
        help_text='max. 42 mb'
    )