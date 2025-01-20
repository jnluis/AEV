import magic
from django.conf import settings
import defusedxml.ElementTree as DefusedTree
from lxml import etree as ET

from io import BytesIO, StringIO


# Define an image validation custom exception
class InvalidImageFile(Exception):
    def __init__(self, message):
        self.message = message

def validate_image(image):
    if image.size > settings.IMAGE_MAX_SIZE:
        raise InvalidImageFile("Image too large")
    
    # Content type check
    print("========= IMAGE CONTENT TYPE: ", image.content_type)

    if image.content_type not in settings.ALLOWED_IMAGE_CONTENT_TYPES:
        raise InvalidImageFile("Invalid image file")
    
    # MIME type check

    raw_image = image.file.read()

    mime_type = magic.from_buffer(raw_image, mime=True)
    print("============= IMAGE MIME TYPE: ", mime_type)
    if mime_type not in settings.ALLOWED_IMAGE_CONTENT_TYPES and mime_type != image.content_type:
        raise InvalidImageFile("Invalid image file")
    
    if mime_type == "image/svg+xml":
        # Sanitize SVG
        return sanitize_svg(raw_image)

    return raw_image

def sanitize_svg(svg):
    # Validate against attacks
    DefusedTree.parse(StringIO(svg.decode("utf-8")))

    print("====TTTTTTTTTTTTT=========")

    root = ET.parse(BytesIO(svg)).getroot()

    # print(ET.tostring(root))

    # Check if it's an SVG
    if root.tag != "{http://www.w3.org/2000/svg}svg":
        raise ValueError("Not an SVG")
    
    # Eliminate script tags
    prefind = root.findall('.//{*}script')
    for child in prefind:
        child.getparent().remove(child)

    # Eliminate entities
    for child in root.findall('.//{*}!ENTITY'):
        child.getparent().remove(child)

    sanitized = ET.tostring(root, encoding="utf-8")

    # Add SVG xml declaration and document type to root
    svg_xml_declaration = '<?xml version="1.0" encoding="utf-8"?>'
    svg_doctype = '<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">'
    sanitized = f"{svg_xml_declaration}\n{svg_doctype}\n{sanitized.decode('utf-8')}".encode("utf-8")

    # print("=============")
    # print(sanitized.decode("utf-8"))
    # print("=============")

    return sanitized
        