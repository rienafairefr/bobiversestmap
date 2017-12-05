import re
import os
import json

with open(os.path.join('data','Combined.txt'), encoding='utf-8') as combined:
    content = combined.readlines()

books = []
book = []

for line in content:
    if line.startswith('##'):
        if len(book)>0:
            books.append(book)
        book = []
    else:
        book.append(line.strip())

books.append(book)
book_chapters=[]
for book in books:
    chapter = []
    chapters = []
    for line in book:
        if len(line.strip()) == 0:
            continue
        if re.match('^\d*\.', line):
            if len(chapter)>0:
                chapters.append(chapter)
            chapter = []
        chapter.append(line)
    chapters.append(chapter)

    def process_chapter(chap):
        matched = re.match('^(\d*)\.(.*)$', chap[0])
        chapter = {
            'n':int(matched.groups()[0].strip()),
            'title':matched.groups()[1].strip(),
            'bob':chap[1],
            'date':chap[2],
            'location':chap[3],
            'content':chap[4:]
        }
        return chapter

    chapters = [process_chapter(chap) for chap in chapters]

    book_chapters.append(chapters)

json.dump(book_chapters, open(os.path.join('generated', 'Combined.json'), 'w'))
