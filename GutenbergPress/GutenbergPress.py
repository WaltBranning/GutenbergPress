#!/usr/bin/env Python3
import os
from wget import download
from csv import DictReader, DictWriter


class DownloadBook:
    library_file ='library.manifest'   
    cwd = os.getcwd()+'/'
    def __init__(self, cat_file, dir=cwd):
        self.dir = dir
        self.cat_file = cat_file
        self.lib = os.path.abspath(cat_file)
        self.catalog = None
        self.library = []
        self.source = 'https://www.gutenberg.org/ebooks/'
        self.default_ebook = '.epub.images'
        self.loadCatalog()
    
    def loadCatalog(self, file=None):
        file = self.lib if not file else file
        index = {}
        with open(file) as f:
            index = {row['Text#']:row for row in DictReader(f, delimiter=',')}
            self.catalog = index
        return index
    
    def buildFileName(self, book_id):
        title = self.catalog[str(book_id)]["Title"].replace(' ', '_')+'.epub'
        if len(title) > 100 : return title[:100]

        return title

    def buildLibrary(self, id_list, destination=None):
        destination = self.dir if not destination else destination
        manifest = []
        if not os.path.exists(destination):
            os.mkdir(destination)
        for id in id_list:
            book_retrieve = self.download(id, destination)
            if book_retrieve : manifest.append(self.catalog[str(id)])
            
        with open(destination + self.library_file, 'w') as f:
            fd = manifest[0].keys()
            writer = DictWriter(f, fieldnames=fd)
            writer.writeheader()
            writer.writerows(manifest)
    
    def download(self,book_id, dest=cwd):
        if self.catalog:
            f_name = self.buildFileName(book_id)
            getBook = lambda url: download(url, out=dest+f_name)
        else:
            getBook = getBook = lambda url: download(url,dest+book_id)
        
        url = ''.join([self.source, str(book_id), self.default_ebook])
        getBook(url)
        print(f"Downloaded {f_name} from {url}")
        return True