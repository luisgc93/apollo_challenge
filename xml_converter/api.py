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
        file = request.FILES["file"]
        if file.content_type != "application/xml":
            return Response(data={"error": "File type must be xml"}, status=422)
        xml_elements = ET.fromstring(file.read())
        json_data = converter.xml_to_json(xml_elements)
        # from pprint import pprint
        # pprint(formatted_version, sort_dicts=False)
        return Response(json_data)
