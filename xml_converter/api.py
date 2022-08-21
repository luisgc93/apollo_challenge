from typing import Dict

from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
import xml.etree.ElementTree as ET

from xml_converter import converter


class ConverterViewSet(ViewSet):
    # Note this is not a restful API
    # We still use DRF to assess how well you know the framework
    parser_classes = [MultiPartParser]

    @action(methods=["POST"], detail=False, url_path="convert")
    def convert(self, request, **kwargs):
        xml_file = request.FILES["file"]
        xml_elements = ET.fromstring(xml_file.read())
        formatted_version = converter.xml_to_json(xml_elements)
        # from pprint import pprint
        # pprint(formatted_version, sort_dicts=False)
        return Response({k: v if v is not None else "" for k, v in formatted_version.items()})
