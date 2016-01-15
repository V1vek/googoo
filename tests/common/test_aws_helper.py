import unittest

from midway.common import upload_image_and_return_url


class TestAWSHelper(unittest.TestCase):
 
    def setUp(self):
        pass
 
    def test_upload_image_and_return_url(self):
		image_url = upload_image_and_return_url('img')
		assert image_url is not None

if __name__ == '__main__':
    unittest.main()