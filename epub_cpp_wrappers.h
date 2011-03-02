#ifndef EPUB_CPP_WRAPPER_H
#define EPUB_CPP_WRAPPER_H

#include <epub.h>

class EPub;

class EIterator {
public:
    ~EIterator() {
        if (m_iter)
            epub_free_iterator(m_iter);
    }
    inline char* next() { return epub_it_get_next(m_iter); }
    inline char* curr() { return epub_it_get_curr(m_iter); }
    inline char* curr_url() { return epub_it_get_curr_url(m_iter); }
private:
    friend class EPub;
    explicit EIterator(struct eiterator* iter) : m_iter(iter) {}
    struct eiterator* m_iter;
};

class TIterator {
public:
    ~TIterator() {
        if (m_iter)
            epub_free_titerator(m_iter);
    }
    inline bool isValid() { return epub_tit_curr_valid(m_iter); }
    inline int depth() { return epub_tit_get_curr_depth(m_iter); }
    inline char* link() { return epub_tit_get_curr_link(m_iter); }
    inline char* label() { return epub_tit_get_curr_label(m_iter); }
    inline bool next() { return epub_tit_next(m_iter); }
private:
    friend class EPub;
    explicit TIterator(struct titerator* iter) : m_iter(iter) {}
    struct titerator* m_iter;
};

class EPub {
public:
    static inline EPub* open(const char* filename, int debug = 0) {
        return new EPub(epub_open(filename, debug));
    }
    inline void set_debug(int debug) { epub_set_debug(m_epub, debug); }
    inline int get_ocf_file(const char* filename, char** data) {
        return epub_get_ocf_file(m_epub, filename, data);
    }
    inline bool close() { return epub_close(m_epub); }
    inline void dump() { epub_dump(m_epub); }
    inline unsigned char** get_metadata(enum epub_metadata type, int* size) {
        return epub_get_metadata(m_epub, type, size);
    }
    inline int get_data(const char* name, char** data) { return epub_get_data(m_epub, name, data); }
    inline EIterator* get_iterator(enum eiterator_type type, int opt = 0) {
        return new EIterator(epub_get_iterator(m_epub, type, opt));
    }
    inline TIterator* get_titerator(enum titerator_type type, int opt = 0) {
        return new TIterator(epub_get_titerator(m_epub, type, opt));
    }
private:
    explicit EPub(struct epub* ptr) : m_epub(ptr) {}
    struct epub* m_epub;
};

#endif
