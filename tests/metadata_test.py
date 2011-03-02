#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import epub
import os


class MetadataTest(unittest.TestCase):

    def setUp(self):
        self.epub_file = os.path.join(os.path.dirname(__file__),
                                      'beyond-the-wall-of-sleep.epub')

    def tearDown(self):
        del self.epub_file

    def testMetadata(self):
        book = epub.EPub.open(self.epub_file)
        #book.dump()

        self.assertEqual(book.get_metadata(epub.EPUB_TITLE)[0],
                         u'Beyond the Wall of Sleep')
        self.assertEqual(book.get_metadata(epub.EPUB_CREATOR)[0],
                         u'aut: Howard Phillips Lovecraft(Lovecraft, Howard Phillips)')
        self.assertEqual(book.get_metadata(epub.EPUB_SUBJECT),
                         (u'Fiction', u'Short Stories'))
        self.assertEqual(book.get_metadata(epub.EPUB_PUBLISHER)[0], u'Feedbooks')
        self.assertEqual(book.get_metadata(epub.EPUB_DESCRIPTION)[0], u'')
        self.assertEqual(book.get_metadata(epub.EPUB_DATE),
                         (u'original-publication: 1919', u'ops-publication: 2007-01-23'))
        self.assertEqual(book.get_metadata(epub.EPUB_RIGHTS)[0],
                         u'This work is available for countries where copyright is Life+70 and in the USA.')


if __name__ == '__main__':
    unittest.main()

