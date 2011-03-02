#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import epub

def quit(code):
    epub.cleanup()
    sys.exit(code)

def usage(code):
    print "Usage: einfo <filename>"
    sys.exit(code)


def main():
    filename = sys.argv[1]
    ep = epub.EPub.open(filename)
    if not ep:
        sys.exit(1)

    ep.dump()

    it = ep.get_iterator(epub.EITERATOR_LINEAR)
    #it = ep.get_iterator(epub.EITERATOR_SPINE)

    print 'xxx'
    print it.curr()
    print 'xxx'
    while it.next():
        print it.curr()
    del it

    sys.exit(ep.close())

if __name__ == '__main__':
    main()

