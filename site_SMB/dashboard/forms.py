from django import forms

class FileUploadForm(forms.Form):
    fileField = forms.FileField(
        label='Select a file to upload',
        help_text='Max 42 MB',
    )