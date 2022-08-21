from django.http import JsonResponse
from django.shortcuts import render

from xml_converter import converter
from xml_converter.forms import UploadFileForm
import xml.etree.ElementTree as ET


def upload_page(request):
    # https://docs.djangoproject.com/en/4.1/topics/http/file-uploads/
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            xml_file = request.FILES["file"]
            xml_elements = ET.fromstring(xml_file.read())
            formatted_version = converter.xml_to_json(xml_elements)
            return JsonResponse({k: v if v is not None else "" for k, v in formatted_version.items()})
        else:
            form = UploadFileForm()
        return render(request, 'upload_page.html', {'form': form})
    form = UploadFileForm()
    return render(request, 'upload_page.html', {'form': form})
