#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import epub
import os


class ReadContentsTest(unittest.TestCase):

    def setUp(self):
        self.epub_file = os.path.join(os.path.dirname(__file__),
                                      'beyond-the-wall-of-sleep.epub')

    def tearDown(self):
        del self.epub_file

    def testReadToc(self):
        book = epub.EPub.open(self.epub_file)
        it = book.get_titerator(epub.TIterator.NAVMAP)
        if not it:
            it = book.get_titerator(epub.TIterator.GUIDE)

        toc = {}
        if it:
            def add(it):
                if it.isValid():
                    toc[it.link()] = it.label()
            add(it)
            while it.next():
                add(it)

        expected = { u'main0.xml'   : u'Beyond the Wall of Sleep',
                     u'title.xml'   : u'Title',
                     u'similar.xml' : u'Recommendations',
                     u'about.xml'   : u'About' }
        self.assertEqual(toc, expected)

    def testReadSpine(self):
        book = epub.EPub.open(self.epub_file)
        it = book.get_iterator(epub.EIterator.SPINE)

        contents = {}
        if it:
            def add(it):
                contents[it.curr_url()] = it.curr()
            add(it)
            while it.next():
                add(it)

        expected_links = [u'about.xml',
                          u'cover.xml',
                          u'feedbooks.xml',
                          u'main0.xml',
                          u'similar.xml',
                          u'title.xml']
        links = contents.keys()
        links.sort()
        self.assertEqual(expected_links, links)
        self.assertEqual(len(contents), 6)


if __name__ == '__main__':
    unittest.main()

