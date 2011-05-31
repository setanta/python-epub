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
        self.toc = None
        self.current = None

        layout = QVBoxLayout(self)

        toolbar = QToolBar()
        toolbar.addAction('Open', self.openClicked)
        toolbar.addAction('Cover', self.coverClicked)
        toolbar.addAction('ToC', self.tocClicked)
        toolbar.addAction('Back', self.goBackClicked)
        toolbar.addAction('Forward', self.goForwardClicked)
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

    @staticmethod
    def findCoverImageFile(epubFilePath):
        epubFile = zipfile.ZipFile(epubFilePath, 'r')
        possible_cover_files = ['cover.png', 'cover.jpg', 'cover.jpeg']
        coverFile = None
        for fileinfo in epubFile.filelist:
            if os.path.basename(fileinfo.filename).lower() in possible_cover_files:
                coverFile = fileinfo
                break
        return coverFile.filename if coverFile else None

    def loadBook(self, ebookfile):
        self.book = EPub.open(ebookfile)
        setattr(self.book, 'filepath', ebookfile)
        self.toc = []

        self.showCover()

        # Load contents
        it = self.book.get_iterator(EIterator.SPINE)
        self.contents = {}
        for item in it:
            self.contents[item.curr_url()] = item.curr()
        title = self.book.get_metadata(EPub.TITLE)[0]
        self.setWindowTitle(title)

    def showCover(self):
        if hasattr(self.book, 'coverpage'):
            contents = self.book.coverpage
        else:
            # Load meta data
            title = self.book.get_metadata(EPub.TITLE)
            #creator = self.book.get_metadata(EPub.CREATOR)
            #subject = self.book.get_metadata(EPub.SUBJECT)
            #publisher = self.book.get_metadata(EPub.PUBLISHER)
            #date = self.book.get_metadata(EPub.DATE)
            #rights = self.book.get_metadata(EPub.RIGHTS)

            coverFile = BookView.findCoverImageFile(self.book.filepath)
            contents = ''
            if coverFile:
                alt = 'alt="%s"' % title if title else ''
                contents += u'<div align="center"><img src="%s" style="max-width: 400px;"/></div>' % coverFile
            #if title:
                #contents += u'<h1 align="center">%s</h1>' % u'<br/>'.join(title)
            #if creator:
                #def processAuthor(author):
                    #aut = author[author.find(':')+1:]
                    #pos = len(aut)
                    #parenthesis = 0
                    #while pos != 0:
                        #pos -= 1
                        #if aut[pos] == ')':
                            #parenthesis += 1
                        #elif aut[pos] == '(':
                            #parenthesis -= 1
                            #if parenthesis == 0:
                                #aut = aut[:pos]
                                #break
                    #return aut.strip()
                #authors = [processAuthor(author) for author in creator]
                #contents += u'<p align="center">by<br/>%s</p>' % u',<br/>'.join(authors)
            #if publisher:
                #contents += u'<p align="center">Published by %s</p>' % u', '.join(publisher)
            #if rights:
                #contents += u'<p align="center">%s</p>' % u', '.join(rights)
            #if date:
                #contents += u'<p align="center">%s</p>' % u', '.join(date)
            #if subject:
                #contents += u'<p align="center">(%s)</p>' % u', '.join(subject)
            contents = u'<html><title>%s</title><body>%s</body></html>' % (u' - '.join(title), contents)
            setattr(self.book, 'coverpage', contents)
        self.loadPage(contents)
        self.current_position = 'coverpage'

    def showToC(self):
        if hasattr(self.book, 'tocpage'):
            contents = self.book.tocpage
        else:
            # Load Table of Contents
            title = self.book.get_metadata(EPub.TITLE)
            if title:
                contents = u'<h1 align="center">%s</h1>' % u'<br/>'.join(title)
            contents += u'<h2>Table of Contents</h2>'
            it = self.book.get_titerator(TIterator.NAVMAP)
            if not it:
                it = self.book.get_titerator(TIterator.GUIDE)
            for item in it:
                if item.isValid():
                    contents += u'<p><a href="%s">%s</a></p>' % (item.link(), item.label())
                self.toc.append(item.link())
            contents = u'<html><title>%s</title><body>%s</body></html>' % (u' - '.join(title), contents)
            setattr(self.book, 'tocpage', contents)
        self.loadPage(contents)
        self.current_position = 'tocpage'

    def linkClicked(self, url):
        if url.path() in self.contents.keys():
            self.current_position = url.path()
            self.loadPage(self.contents[url.path()])
        elif url.path().startswith('http://') or url.path().startswith('www.'):
            print 'pass the address to the system browser'

    def coverClicked(self):
        self.showCover()

    def openClicked(self):
        epubFile = QFileDialog.getOpenFileName(self, 'Open Image', '.', '*.epub')[0]
        if epubFile:
            self.loadBook(str(epubFile))

    def tocClicked(self):
        self.showToC()

    def goBackClicked(self):
        if self.current_position == 'coverpage':
            return
        if self.current_position == 'tocpage':
            self.showCover()
        elif self.toc[0] == self.current_position:
            self.showToC()
        elif self.current_position != 'coverpage':
            self.current_position = self.toc[self.toc.index(self.current_position)-1]
            self.loadPage(self.contents[self.current_position])

    def goForwardClicked(self):
        if self.current_position == 'coverpage':
            self.showToC()
        elif self.current_position == 'tocpage':
            self.current_position = self.toc[0]
            self.loadPage(self.contents[self.current_position])
        elif self.current_position != self.toc[-1]:
            self.current_position = self.toc[self.toc.index(self.current_position)+1]
            self.loadPage(self.contents[self.current_position])

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

