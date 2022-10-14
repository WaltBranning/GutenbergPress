# GutenbergPress
Simple Python script to source a local E-Book library from the Project Gutenberg catalog.

This project currently has two main functionality goals in mind: a simple command line script to allow for the creation of a local e-book library and as a module.

Currently its pre-alpha concept phase takes the csv Project Gutenberg catalog found at https://www.gutenberg.org/cache/epub/feeds/pg_catalog.csv.
initializes the DownloadBook class with the catalog and optional destination directory (defaults to current working directory).

`book = DownloadBook('pg_catalog.csv', dest_dir)`

To download a create a local library it uses the `buildLibrary()` method. In this current state takes a list of catalog id numbers and iterates over the list writing the files to the destination directory and creating a `library.manifest` of downloaded items.

Alternatively you can use the download method to fetch an e-book individually and write the file to destination directory

`book.download(bookid)`


## Future Implementations

* Find or write a fast and easily searched library manifest format
* Create search function to search the catalog for robust downloading
* Way to manage metadata to improve, addto, and clean up the current data
