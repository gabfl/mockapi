from .base import BaseTest
from .. import api_handler


class Test(BaseTest):

    multiline_json = """
{
    "success": true,
    "info": "This is a sample API response."
}
    """
    inline_json = '{"a": true}'
    multiline_xml = """
    <slideshow>
<title>Demo slideshow</title>
<slide>
    <title>Slide title</title>
    <point>This is a demo</point>
    <point>Of a program for processing slides</point>
</slide>
</slideshow>
"""
    inline_xml = '<slideshow><title>Demo slideshow</title></slideshow>'
    inline_string = 'hello world'

    def test_detect_payload_type(self):

        assert api_handler.detect_payload_type(self.inline_json) == 'json'
        assert api_handler.detect_payload_type(self.multiline_json) == 'json'
        assert api_handler.detect_payload_type(self.multiline_xml) == 'xml'
        assert api_handler.detect_payload_type(self.inline_xml) == 'xml'
        assert api_handler.detect_payload_type(self.inline_string) == 'text'

    def test_is_json(self):

        assert api_handler.is_json(self.inline_json) is True
        assert api_handler.is_json(self.multiline_json) is True
        assert api_handler.is_json(self.multiline_xml) is False
        assert api_handler.is_json(self.inline_xml) is False
        assert api_handler.is_json(self.inline_string) is False

    def test_is_xml(self):

        assert api_handler.is_xml(self.inline_json) is False
        assert api_handler.is_xml(self.multiline_json) is False
        assert api_handler.is_xml(self.multiline_xml) is True
        assert api_handler.is_xml(self.inline_xml) is True
        assert api_handler.is_xml(self.inline_string) is False
