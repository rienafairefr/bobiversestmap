import contextlib
import itertools
import os

from app import db
from generator.books import get_book_chapters, get_keys
from generator.chapter_characters import get_chapter_characters
from generator.models import ChaptersLink
from generator.models.books import Book
from generator.models.chapters import BookChapter
from generator.models.links import Link
from generator.travels import get_travels
from generator.utils import memoize


def import_links(book_chapters=None):
    if book_chapters is None:
        book_chapters = get_book_chapters()

    links = {}
    for k, book_chapter in book_chapters.items():
        nb, nc = k
        chapter_characters = get_chapter_characters(k)

        for isent, tokenized_sentence in enumerate(book_chapter.tokenized_content):
            ns = isent + 1
            for character_pair in itertools.combinations(chapter_characters, 2):
                characterA = character_pair[0]
                characterB = character_pair[1]

                for name0 in characterA.all_names:
                    for name1 in characterB.all_names:
                        if characterB.id > characterA.id \
                                and name0 in tokenized_sentence \
                                and name1 in tokenized_sentence:
                            link = Link(characterA=characterA,
                                         characterB=characterB,
                                        ns = ns,
                                         sentence=book_chapter.sentences[isent])
                            book_chapter.links.append(link)

    # write_links(links)
    db.session.commit()
    postprocess_links()

    return get_links()


def treat_scut_links(travels=None):
    if travels is None:
        travels = get_travels()
    for chapter_link in db.session.query(ChaptersLink).all():
        link = chapter_link.link

        locationA = travels.get((link.characterA.id, chapter_link.chapter_nb, chapter_link.chapter_nc))
        locationB = travels.get((link.characterB.id, chapter_link.chapter_nb, chapter_link.chapter_nc))

        link.is_scut = locationA != {} and locationB != {} and locationA != locationB


@memoize()
def get_links(nb=None):
    q = db.session.query(BookChapter, BookChapter.links)
    if nb is not None:
        q = q.filter(BookChapter.nb == nb)

    return q.all()


def postprocess_links():
    def remove(nb, nc, ns):
        book_chapter = db.session.query(BookChapter).get((nb,nc))
        for link in book_chapter.links:
            if link.ns == ns:
                db.session.remove(link)

    def fix(nb, nc, ns, cA_id, cB_id):
        book_chapter = db.session.query(BookChapter).get((nb, nc))
        for link in book_chapter.links:
            if link.ns == ns:
                link.characterA_id = cA_id
                link.characterB_id = cB_id

    # Tom Hanks
    remove(1, 13, 88)

    # '"And with Archimedes gone, well…" "Will we be okay?"'
    remove(3, 69, 53)

    fix(1, 60, 96, 'Fred', 'Bill')
    fix(1, 60, 177, 'Fred', 'Bill')

    db.session.commit()


def write_links(links):
    keep = {}

    def file_name(nb, nc):
        return os.path.join('generated', 'links', str(nb), '%d %d' % (nb, nc))

    with contextlib.ExitStack() as stack:
        links_files = {}
        for nb, nc in get_keys():
            os.makedirs(os.path.join('generated', 'links', str(nb)), exist_ok=True)
            links_files[nb, nc] = stack.enter_context(
                open(file_name(nb, nc), 'w',
                     encoding='utf-8'))

        for (nb, nc, ns), link in links.items():
            if link.is_scut:
                continue
            links_file = links_files[nb, nc]
            keep[nb, nc] = True
            to_write = '{:^10s} {:^10s} {:3d} {:3d} {:3d} {:s}\n'.format(link.characterA_id, link.characterB_id, nb, nc,
                                                                         ns, link.sentence)
            links_file.write(to_write)
            print(to_write)

    for k in get_keys():
        if not keep.get(k):
            os.remove(file_name(*k))


if __name__ == '__main__':
    write_links(get_links())
