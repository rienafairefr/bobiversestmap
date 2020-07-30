import ebooklib
from ebooklib import epub


from BeautifulSoup import BeautifulSoup

books = [0,0,0]

books[0] = epub.read_epub('Book 1.epub')
books[1] = epub.read_epub('Book 2.epub')
books[2] = epub.read_epub('Book 3.epub')


titles = [[el.title for el in book.toc] for book in books]

pass