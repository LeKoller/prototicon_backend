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
        contents = Content.objects.create(**self.content_data)

        contents = Content.objects.first()

        self.assertEqual(contents.image, self.content_data['image'])
