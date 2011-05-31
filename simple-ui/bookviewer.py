#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import zipfile
import tempfile
from epub import EPub, TIterator, EIterator
from PySide.QtCore import QUrl
from PySide.QtGui import QApplication, QVBoxLayout, QWidget, QToolBar, QFileDialog
from PySide.QtWebKit import QWebView, QWebPage, QWebSettings


class BookView(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.book = None

        layout = QVBoxLayout(self)

        toolbar = QToolBar()
        toolbar.addAction('Open', self.openClicked)
        toolbar.addAction('ToC', self.tocClicked)
        toolbar.addAction('Quit', self.quitClicked)
        layout.addWidget(toolbar)

        self.view = QWebView(self)
        layout.addWidget(self.view)

        self.setLayout(layout)

    def loadPage(self, contents):
        pageTempDir = tempfile.mkdtemp()
        self.view.setHtml(contents)
        page = self.view.page()

        epubFile = zipfile.ZipFile(self.book.filepath, 'r')
        epubFiles = epubFile.namelist()

        for element in page.mainFrame().findAllElements('img'):
            image = element.attribute('src')
            if not image.startswith('/') or not images.startswith('file://'):
                imageFile = None
                if image in epubFiles:
                    imageFile = image
                elif os.path.join('OEBPS', image) in epubFiles:
                    imageFile = os.path.join('OEBPS', image)
                elif os.path.join('OPS', image) in epubFiles:
                    imageFile = os.path.join('OPS', image)
                else:
                    continue
                epubFile.extract(imageFile, pageTempDir)
                element.setAttribute('src', 'file://%s/%s' % (pageTempDir, imageFile))

        epubFile.close()

        page.setLinkDelegationPolicy(QWebPage.DelegateAllLinks)
        page.linkClicked[QUrl].connect(self.linkClicked)

    def loadBook(self, ebookfile):
        self.book = EPub.open(ebookfile)
        setattr(self.book, 'filepath', ebookfile)

        self.loadToC()

        # Load contents
        it = self.book.get_iterator(EIterator.SPINE)
        self.contents = {}
        for item in it:
            self.contents[item.curr_url()] = item.curr()
        title = self.book.get_metadata(EPub.TITLE)[0]
        self.setWindowTitle(title)

    def loadToC(self):
        # Load meta data
        title = self.book.get_metadata(EPub.TITLE)
        creator = self.book.get_metadata(EPub.CREATOR)
        subject = self.book.get_metadata(EPub.SUBJECT)
        publisher = self.book.get_metadata(EPub.PUBLISHER)
        date = self.book.get_metadata(EPub.DATE)
        rights = self.book.get_metadata(EPub.RIGHTS)

        if title:
            contents = u'<h1>%s</h1>' % u'<br/>'.join(title)
        if creator:
            contents += u'<p>%s</p>' % u', '.join(creator)
        if subject:
            contents += u'<p>subject: %s</p>' % u', '.join(subject)
        if publisher:
            contents += u'<p>Published by %s</p>' % u', '.join(publisher)
        if date:
            contents += u'<p>%s</p>' % u', '.join(date)
        if rights:
            contents += u'<p>%s</p>' % u', '.join(rights)

        # Load Table of Contents
        contents += u'<h1>Table of Contents</h1>'

        it = self.book.get_titerator(TIterator.NAVMAP)
        if not it:
            it = self.book.get_titerator(TIterator.GUIDE)
        for item in it:
            if item.isValid():
                contents += u'<p><a href="%s">%s</a></p>' % (item.link(), item.label())
        contents = u'<html><title>%s</title><body>%s</body></html>' % (u' - '.join(title), contents)

        self.loadPage(contents)

    def linkClicked(self, url):
        if url.path() in self.contents.keys():
            self.loadPage(self.contents[url.path()])
        elif url.path().startswith('http://') or url.path().startswith('www.'):
            print 'pass the address to the system browser'

    def openClicked(self):
        epubFile = QFileDialog.getOpenFileName(self, 'Open Image', '.', '*.epub')[0]
        if epubFile:
            self.loadBook(str(epubFile))

    def tocClicked(self):
        self.loadToC()

    def quitClicked(self):
        QApplication.instance().quit()


def main():
    if len(sys.argv) < 2:
        print 'Usage: %s <epub-file>' % sys.argv[0]
        sys.exit(1)

    epub_file = sys.argv[1]

    if not os.path.isfile(epub_file):
        print 'ePub file "%s" does not exist.' % epub_file
        sys.exit(1)

    app = QApplication(sys.argv)
    win = BookView()
    win.loadBook(epub_file)
    #win.resize(600, 1024)
    win.resize(480, 800)
    win.show()
    return app.exec_()


if __name__ == '__main__':
    sys.exit(main())

