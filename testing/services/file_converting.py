# from django import forms
# from django.forms import ModelForm
# from django.db import models
#
#
# class TextOfFile(models.Model):
#     content = models.TextField()
#
#
# class FileConvertHelper(ModelForm):
#     content = models.TextField()
#
#     class Meta:
#         model = TextOfFile
#
#     def __init__(self, *args, **kwargs):
#         self.content = ''
#         for line in kwargs.pop('content'):
#             self.content += line
#
#
#
#
# class FileUploadForm(forms.Form):
#     file = forms.FileField()
#
#     def clean_file(self):
#         data = self.cleaned_data["file"]
#         print(data)
#         exit()
#         form = FileConvertHelper(content=data_dict)
#         if form.is_valid():
#             self.instance = form.save(commit=False)
#         else:
#             # You can use more specific error message here
#             raise forms.ValidationError(u"The file contains invalid data.")
#         return data
#
#     def save(self):
#         # We are not overriding the `save` method here because `form.Form` does not have it.
#         # We just add it for convenience.
#         instance = getattr(self, "instance", None)
#         if instance:
#             instance.save()
#         return instance
#
#
# def convert_file(request):
#     form = FileUploadForm(request.POST, request.FILES)
#     if form.is_valid():
#         form.save()
#     else:
#         print('error')
