#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import epub
import os


class ReadContentsTest(unittest.TestCase):

    def setUp(self):
        self.epub_file = os.path.join(os.path.dirname(__file__),
                                      'beyond-the-wall-of-sleep.epub')
        self.expected_links = [u'about.xml',
                               u'cover.xml',
                               u'feedbooks.xml',
                               u'main0.xml',
                               u'similar.xml',
                               u'title.xml']

    def tearDown(self):
        del self.epub_file

    def testReadSpineWithNext(self):
        book = epub.EPub.open(self.epub_file)
        it = book.get_iterator(epub.EIterator.SPINE)

        contents = {}
        next(it)
        while True:
            contents[it.curr_url()] = it.curr()
            try:
                next(it)
            except:
                break

        links = contents.keys()
        links.sort()
        self.assertEqual(self.expected_links, links)
        self.assertEqual(len(contents), 6)

    def testReadSpineWithIteratorProtocol(self):
        book = epub.EPub.open(self.epub_file)
        it = book.get_iterator(epub.EIterator.SPINE)

        contents = {}
        for item in it:
            contents[item.curr_url()] = item.curr()

        links = contents.keys()
        links.sort()
        self.assertEqual(self.expected_links, links)
        self.assertEqual(len(contents), 6)



if __name__ == '__main__':
    unittest.main()

