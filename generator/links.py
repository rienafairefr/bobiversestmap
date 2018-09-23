import contextlib
import itertools
import os

from app import db
from generator.book_chapters import get_book_chapters
from generator.common import get_keys
from generator.models import ChaptersLink
from generator.models.chapter_characters_travel import CharacterTravel
from generator.models.chapters import BookChapter
from generator.models.links import Link


def import_links(book_chapters=None):
    if book_chapters is None:
        book_chapters = get_book_chapters()

    with db.session.no_autoflush:
        for book_chapter in book_chapters:
            treat_one_chapter_link(book_chapter)

    db.session.commit()
    return get_links()


def treat_one_chapter_link(book_chapter):
    if len(book_chapter.characters) < 2:
        return

    for isent, tokenized_sentence in enumerate(book_chapter.tokenized_content):
        ns = isent + 1
        for character_pair in itertools.combinations(book_chapter.characters, 2):
            characterA = character_pair[0]
            characterB = character_pair[1]

            for name0 in characterA.all_names:
                for name1 in characterB.all_names:
                    if characterB.id > characterA.id \
                            and name0 in tokenized_sentence \
                            and name1 in tokenized_sentence:
                        link = Link(characterA=characterA,
                                    characterB=characterB,
                                    ns=ns,
                                    sentence=' '.join(book_chapter.tokenized_content[isent]))
                        book_chapter.links.append(link)
                        db.session.add(link)


def postprocess_scut_links():
    def get_location(characterid, nb, nc):
        return db.session.query(CharacterTravel).get((characterid, nb, nc)).location

    for chapter_link in db.session.query(ChaptersLink).all():
        link = chapter_link.link

        locationA = get_location(link.characterA.id, chapter_link.chapter_nb, chapter_link.chapter_nc)
        locationB = get_location(link.characterB.id, chapter_link.chapter_nb, chapter_link.chapter_nc)

        link.is_scut = locationA != {} and locationB != {} and locationA != locationB

    db.session.commit()


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
