#!/usr/bin/env Python3
import os
from wget import download
from csv import DictReader, DictWriter


class DownloadBook:
    """
    Class object: DownloadBook(catalog_file, destination_directory)
    DownloadBook is initalized with a local catalog_file and an
    optional destination directory. If directory not provided it will
    default to the current working directory.        
    """
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
        self.load_catalog()
    
    def load_catalog(self, file=None):
        """
        Class Method: load_catalog(file)
        load_catalog is called during DownloadBook at init to load
        the catalog file provided from DownloadBook and return a
        dictionary object with the Text# as the keys. This method can be
        called after instantiation with file=new_directory argument to 
        load a different catalog or if no catalog was initialy provided.
        """
        file = self.lib if not file else file
        index = {}
        with open(file) as f:
            index = {row['Text#']:row for row in DictReader(f, delimiter=',')}
            self.catalog = index
        return index
    
    def build_filename(self, book_id):
        """
        Class Method: build_filename(book_id)
        build_filename simply creates a concise filename from book title.
        """
        title = self.catalog[str(book_id)]["Title"].replace(' ', '_')+'.epub'
        if len(title) > 100 : return title[:100]
        return title

    def build_library(self, id_list, destination=None):
        """
        Class Method: build_library(book_list, desination=optional)
        build_library is called to construct the library - it takes a 
        list of id numbers from the input then downloads those with wget
        to the destination dir provided when instantiated. Can also take
        an optional destination argument to use different destination.
        Writes books then creates a manifest of books with metadata from 
        Project Gutenberg's catalog.
        """
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
            print(f'Wrote Manifest to {self.library_file}')
        return f"Finished Building Library {destination}"

    def download(self,book_id, dest=cwd):
        """
        Class Method: download(book_id, dest=optional)
        download is used by the build_library method to fetch ebooks and
        dowload to destination directory. It can also be called independantly
        to download books individually.
        """
        if self.catalog:
            f_name = self.build_filename(book_id)
            get_book = lambda url: download(url, out=dest+f_name)
        else:
            get_book = get_book = lambda url: download(url,dest+book_id)
        
        url = ''.join([self.source, str(book_id), self.default_ebook])
        get_book(url)
        print(f"\nDownloaded {f_name} from {url}")
        return True



