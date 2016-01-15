import unittest

from midway.common.util.csv_helper import read_csv_and_return_as_dict_lists, extract_req_fields_from_dic_lists,insert_books_from_dictionary


class TestCSVHelper(unittest.TestCase):
 
	def setUp(self):
		pass

	def test_read_csv_and_return_as_dict_lists(self):
		csv_data = read_csv_and_return_as_dict_lists('/home/vinod/projects/books.csv')
		assert type(csv_data) is list

	def test_extract_req_fields_from_dic_lists(self):
		required_fields = ['publisher','authors','pages','edition_and_year',
			'image_id','Isbn_10','Isbn_13','title','category','sub_category']
		csv_data = read_csv_and_return_as_dict_lists('/home/vinod/projects/books.csv')
		required_data = extract_req_fields_from_dic_lists(required_fields,csv_data)
		assert type(required_data) is list

	def test_insert_books_from_dictionary(self):
		required_fields = ['publisher','authors','pages','price','binding','edition_and_year',
			'image_id','Isbn_10','Isbn_13','title','category','sub_category']
		csv_data = read_csv_and_return_as_dict_lists('/home/vinod/projects/books.csv')
		required_data = extract_req_fields_from_dic_lists(required_fields,csv_data)
		insert_books_from_dictionary(required_data)

if __name__ == '__main__':
    unittest.main()