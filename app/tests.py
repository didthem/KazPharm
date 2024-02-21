from django.test import TestCase

class TestIndex(TestCase):
    def test_index(self):
        response = self.client.get('//')
        self.assertEqual(response.status_code, 200)
        
    def test_text(self):
        response = self.client.get('//')
        self.assertIn('Index', response.content.decode())
