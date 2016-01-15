import unittest
from rest_framework.test import APITestCase

class TestCategoryApi(APITestCase):
 
    def test_get_category(self):
		"""
        Ensure we can get category objects.
        """
		response = self.client.get('/api/publishers/6')
		self.assertEqual(response.data, {'id': 6})

