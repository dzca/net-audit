#!/usr/bin/python

class Pager:
    def __init__(self, size, count, page):
        self.size = size
        self.count = count
        self.pages = self._init_pages()
        self.page = page
        
    def _init_pages(self):
        pages = self.count/self.size
        mod_of_pages = self.count%self.size
        if mod_of_pages == 0:
            return pages
        else:
            return pages + 1
        
    @property
    def current(self):
        return self.page
    
    @property
    def pages(self):
        return self.pages
    
    @property
    def previous(self):
        if self.page > 1:
            return self.page - 1
        else:
            return 0
    @property
    def next(self):
        if self.page == self.pages:
            return 0
        else:
            return self.page + 1
        
    @property
    def size(self):
        return self.size