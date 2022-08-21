from typing import Dict

import xml.etree.ElementTree as ET


def xml_to_json(node: ET.Element) -> Dict:
    result = {}
    if len(node) == 0:
        # node is leaf (no more children)
        result[node.tag] = node.text if node.text else ""
        return result
    child = node[0]
    if len(child) == 0:
        # node has only one child
        result[node.tag] = [xml_to_json(child)]
    else:
        # node has multiple children
        result[node.tag] = [{child.tag: [xml_to_json(sub_child) for sub_child in child]} for child in node]
    return result
