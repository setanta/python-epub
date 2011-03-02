#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest
import epub

class BasicTest(unittest.TestCase):

    def testModuleItems(self):
        expected = set(['EPub', 'TIterator', 'EIterator', 'cleanup'])
        items = set(dir(epub))
        self.assert_(items.issuperset(expected))

    def testEPubItems(self):
        expected = set(['open', 'close', 'dump', 'get_data',
                        'get_iterator', 'get_titerator', 'get_metadata',
                        'get_ocf_file', 'metadata', 'set_debug'])
        items = set(dir(epub.EPub))
        self.assert_(items.issuperset(expected))

    def testTIteratorItems(self):
        expected = set(['GUIDE', 'NAVMAP', 'PAGES',
                        'depth', 'isValid', 'label',
                        'link', 'next', 'type'])
        items = set(dir(epub.TIterator))
        self.assert_(items.issuperset(expected))

    def testEIteratorItems(self):
        expected = set(['LINEAR', 'NONLINEAR', 'SPINE',
                        'curr', 'curr_url', 'next', 'type'])
        items = set(dir(epub.EIterator))
        self.assert_(items.issuperset(expected))


if __name__ == '__main__':
    unittest.main()


'''
print dir(epub)
print dir(epub.EPub)

epub_file = os.path.join(os.path.dirname(__file__), 'beyond-the-wall-of-sleep.epub')
ep = epub.EPub.open(epub_file)
print ep
print ep.dump()

tit = ep.get_titerator(epub.TITERATOR_NAVMAP)
print tit
print dir(tit)

print tit.depth()
#print tit.label()
print tit.isValid()
print tit.next()
print tit.depth()
#print tit.label()
print tit.isValid()
print tit.next()
'''

