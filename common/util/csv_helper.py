from __future__ import unicode_literals
import logging
import re

import django

django.setup()
from django.db import transaction
from midway.app.books.models import Book
from midway.app import Category
from midway.app.sub_categories import SubCategory
from midway.app.publishers.models import Publisher
from midway.app import Author
import xlrd
import csv

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)
import codecs,cStringIO


class UTF8Recoder:
    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)
    def __iter__(self):
        return self
    def next(self):
        return self.reader.next().encode("utf-8")


class UnicodeReader:
    def __init__(self, f, dialect=csv.excel, encoding="utf-8-sig", **kwds):
        f = UTF8Recoder(f, encoding)
        self.reader = csv.reader(f, dialect=dialect, **kwds)
    def next(self):
        '''next() -> unicode
        This function reads and returns the next line as a Unicode string.
        '''
        row = self.reader.next()
        return [unicode(s, "utf-8", errors='ignore') for s in row]
    def __iter__(self):
        return self

class UnicodeWriter:
    def __init__(self, f, dialect=csv.excel, encoding="utf-8-sig", **kwds):
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()
    def writerow(self, row):
        '''writerow(unicode) -> None
        This function takes a Unicode string and encodes it to the output.
        '''
        self.writer.writerow([s.encode("utf-8") for s in row])
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        data = self.encoder.encode(data)
        self.stream.write(data)
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)

def convert_excel_into_csv(file_path, file_name, ext):


    wb = xlrd.open_workbook(file_path+file_name+'.'+ext)
    sh = wb.sheet_by_name('Sheet1')
    csv_file = open(file_path+file_name+'.csv', 'wb')
    wr = csv.writer(csv_file, quoting=csv.QUOTE_ALL)

    for row_num in xrange(sh.nrows):
        wr.writerow(sh.row_values(row_num))

    csv_file.close()

    return file_path+file_name+'.csv'


def convert_csv_data_into_unicode(old_file, new_file):
    with open(old_file, 'r') as fin, open(new_file, "wb") as fo:
        reader = csv.reader(fin)
        writer = csv.writer(fo)
        for row in reader:
                temp = list(row)
                writer.writerow([unicode(s, errors='ignore') for s in temp])


def read_csv_and_return_as_dict_lists(file):

    columns = []
    try:
        with open(file, 'rb') as fp:
            data_dicts = csv.DictReader(fp)
            for data in data_dicts:
                columns.append(data)

    except Exception, err:
        logging.exception("Error Message {0}".format(err))
        columns = None

    return columns


def extract_req_fields_from_dic_lists(required_fields, data_lists):
    required_data = []

    for data in data_lists:
        new_dict = {}
        for req_field in required_fields: 
            new_dict[req_field] = data[req_field]

        required_data.append(new_dict)

    return required_data


def insert_seller_books_from_dictionary(required_data):
        i=0
        # Transaction atomic to reduce the commits for each each query
        # ToDo : Optimize this function to handle import books from csv
        # Function needs to moved into books module
        with transaction.atomic():
            for data in required_data:
                # log.info("pages : {0}".format(data['pages']))
                try:
                    book_id = insert_books_from_dictionary(data)
                except:
                    print i
                    i+=1
                    pass


def insert_books_from_dictionary(data):
        
    category, created = Category.objects.update_or_create(name=data['category'])
    sub_category = None

    if data['sub_category'].decode('utf-8') != '':
        sub_category, created = SubCategory.objects.update_or_create(
            name=data['sub_category'], category=category)

    publisher, created = Publisher.objects.update_or_create(name=data['publishers'])
    # convert strings to float

    # ToDo : Fix constraints and create a function
    # to handle data check and conversion
    try:
        price = float(data['mrp_price'])
    except ValueError:
        price = 0.0
        pass

    try:
        pages = float(data['pages'])
    except ValueError:
        pages = None
        pass

    binding = 1 if data['binding'] == 'Hardboard' else 2
    book, created = Book.objects.update_or_create(title=data['title'],
        description=data['description'], pages=pages, binding=binding, price=price, category=category,
        sub_category=sub_category, edition_and_year=data['edition_and_year'],
        isbn_10=data['isbn_10'], isbn_13=data['isbn_13'], image_url=data['image_url'])

    book.publishers.add(publisher)

    authors = re.split(",|and|&|  ", data['authors'].decode('utf-8'))
    for author in authors:
        author, created = Author.objects.update_or_create(name=author.strip())

        book.authors.add(author)

    return dict(book_id=book.id)