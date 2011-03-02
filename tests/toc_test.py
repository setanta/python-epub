#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import epub
import os


class ReadTableOfContentsTest(unittest.TestCase):

    def setUp(self):
        self.epub_file = os.path.join(os.path.dirname(__file__),
                                      'beyond-the-wall-of-sleep.epub')
        self.expected = { u'main0.xml'   : u'Beyond the Wall of Sleep',
                          u'title.xml'   : u'Title',
                          u'similar.xml' : u'Recommendations',
                          u'about.xml'   : u'About' }

    def tearDown(self):
        del self.epub_file
        del self.expected

    def testReadTocWithIteratorProtocol(self):
        book = epub.EPub.open(self.epub_file)
        it = book.get_titerator(epub.TIterator.NAVMAP)
        if not it:
            it = book.get_titerator(epub.TIterator.GUIDE)

        self.assert_(it)

        toc = {}
        for item in it:
            if item.isValid():
                toc[item.link()] = item.label()

        self.assertEqual(toc, self.expected)


    def testReadTocWithNext(self):
        book = epub.EPub.open(self.epub_file)
        it = book.get_titerator(epub.TIterator.NAVMAP)
        if not it:
            it = book.get_titerator(epub.TIterator.GUIDE)

        self.assert_(it)

        toc = {}
        next(it)
        while it.isValid():
            toc[it.link()] = it.label()
            try:
                next(it)
            except:
                break

        self.assertEqual(toc, self.expected)


if __name__ == '__main__':
    unittest.main()

