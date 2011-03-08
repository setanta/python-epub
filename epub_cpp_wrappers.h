#ifndef EPUB_CPP_WRAPPER_H
#define EPUB_CPP_WRAPPER_H

#include <epub.h>

class EPub;

class EIterator {
public:
    enum type {
        SPINE = int(EITERATOR_SPINE),
        LINEAR = int(EITERATOR_LINEAR),
        NONLINEAR = int(EITERATOR_NONLINEAR)
    };
    ~EIterator() { epub_free_iterator(m_iter); }
    inline bool next() {
        if (m_isFirst) {
            m_isFirst = false;
            return true;
        }
        return epub_it_get_next(m_iter);
    }
    inline char* curr() { return epub_it_get_curr(m_iter); }
    inline char* curr_url() { return epub_it_get_curr_url(m_iter); }
private:
    friend class EPub;
    explicit EIterator(struct eiterator* iter) : m_iter(iter), m_isFirst(true) {}
    struct eiterator* m_iter;
    bool m_isFirst;
};

class TIterator {
public:
    enum type {
        NAVMAP = int(TITERATOR_NAVMAP),
        GUIDE = int(TITERATOR_GUIDE),
        PAGES = int(TITERATOR_PAGES)
    };
    ~TIterator() { epub_free_titerator(m_iter); }
    inline bool isValid() { return epub_tit_curr_valid(m_iter); }
    inline int depth() { return epub_tit_get_curr_depth(m_iter); }
    inline char* link() { return epub_tit_get_curr_link(m_iter); }
    inline char* label() { return epub_tit_get_curr_label(m_iter); }
    inline bool next() {
        if (m_isFirst) {
            m_isFirst = false;
            return true;
        }
        return epub_tit_next(m_iter);
    }
private:
    friend class EPub;
    explicit TIterator(struct titerator* iter) : m_iter(iter), m_isFirst(true) {}
    struct titerator* m_iter;
    bool m_isFirst;
};

class EPub {
public:
    enum metadata {
        ID = int(EPUB_ID),
        TITLE = int(EPUB_TITLE),
        CREATOR = int(EPUB_CREATOR),
        CONTRIB = int(EPUB_CONTRIB),
        SUBJECT = int(EPUB_SUBJECT),
        PUBLISHER = int(EPUB_PUBLISHER),
        DESCRIPTION = int(EPUB_DESCRIPTION),
        DATE = int(EPUB_DATE),
        TYPE = int(EPUB_TYPE),
        FORMAT = int(EPUB_FORMAT),
        SOURCE = int(EPUB_SOURCE),
        LANG = int(EPUB_LANG),
        RELATION = int(EPUB_RELATION),
        COVERAGE = int(EPUB_COVERAGE),
        RIGHTS = int(EPUB_RIGHTS),
        META = int(EPUB_META)
    };

    ~EPub() {
        epub_close(m_epub);
    }

    static inline EPub* open(const char* filename, int debug = 0) {
        struct epub* book = epub_open(filename, debug);
        if (book)
            return new EPub(book);
        return 0;
    }
    inline void set_debug(int debug) { epub_set_debug(m_epub, debug); }
    inline int get_ocf_file(const char* filename, char** data) {
        return epub_get_ocf_file(m_epub, filename, data);
    }
    inline void dump() { epub_dump(m_epub); }
    inline unsigned char** get_metadata(metadata type, int* size) {
        return epub_get_metadata(m_epub, epub_metadata(type), size);
    }
    inline int get_data(const char* name, char** data) { return epub_get_data(m_epub, name, data); }
    inline EIterator* get_iterator(EIterator::type type, int opt = 0) {
        struct eiterator* it = epub_get_iterator(m_epub, eiterator_type(type), opt);
        if (it)
            return new EIterator(it);
        return 0;
    }
    inline TIterator* get_titerator(TIterator::type type, int opt = 0) {
        struct titerator* it = epub_get_titerator(m_epub, titerator_type(type), opt);
        if (it)
            return new TIterator(it);
        return 0;
    }
private:
    explicit EPub(struct epub* ptr) : m_epub(ptr) {}
    EPub(const EPub& other) {}
    EPub& operator=(const EPub& other) {}
    struct epub* m_epub;
};

#endif

