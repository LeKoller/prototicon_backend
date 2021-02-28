from django.test import TestCase

from ..models import Content


class TestContentModel(TestCase):
    def setUp(self):
        self.content_data = {
            'title': 'a title',
            'text': 'a text',
            'image': 'an image'
        }
    
    def test_create_a_content(self):
        content = Content.objects.create(**self.content_data)

        content = Content.objects.first()
        
        self.assertEqual(content.image, self.content_data['image'])