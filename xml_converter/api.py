from typing import Dict

from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
import xml.etree.ElementTree as ET


def _convert_to_json(node: ET.Element) -> Dict:
    result = {}
    if len(node) == 0:
        # node is leaf (no more children)
        result[node.tag] = node.text
        return result
    child = node[0]
    if len(child) == 0:
        result[node.tag] = [_convert_to_json(child)]
    else:
        result[node.tag] = [{child.tag: [_convert_to_json(sub_child) for sub_child in child]} for child in node]
    return result


class ConverterViewSet(ViewSet):
    # Note this is not a restful API
    # We still use DRF to assess how well you know the framework
    parser_classes = [MultiPartParser]

    @action(methods=["POST"], detail=False, url_path="convert")
    def convert(self, request, **kwargs):
        xml_file = request.FILES["file"]
        xml_elements = ET.fromstring(xml_file.read())
        # from pprint import pprint
        # pprint(_format(json_version)["Root"], sort_dicts=False)
        formatted_version = _convert_to_json(xml_elements)
        return Response({k: v if v is not None else "" for k, v in formatted_version.items()})
