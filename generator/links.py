import contextlib
import itertools
import os

from app import db
from generator.book_chapters import get_book_chapters
from generator.common import get_keys
from generator.models import ChapterLink
from generator.models.chapter_characters_travel import CharacterTravel
from generator.models.chapters import BookChapter
from generator.models.links import Link


def import_links(book_chapters=None):
    if book_chapters is None:
        book_chapters = get_book_chapters()

    for book_chapter in book_chapters:
        treat_one_chapter_link(book_chapter)

    db.session.commit()


def treat_one_chapter_link(book_chapter):
    if len(book_chapter.characters) < 2:
        return

    for isent, tokenized_sentence in enumerate(book_chapter.tokenized_content):
        ns = isent + 1
        for character_pair in itertools.combinations(book_chapter.characters, 2):
            character_a = character_pair[0]
            character_b = character_pair[1]

            if character_b.id > character_a.id:

                character_a_names = character_a.all_names
                if character_a == book_chapter.bob_character:
                    character_a_names.append('I')

                character_b_names = character_b.all_names
                if character_b == book_chapter.bob_character:
                    character_b_names.append('I')

                for name0 in character_a_names:
                    for name1 in character_b_names:
                        if name0 in tokenized_sentence \
                                and name1 in tokenized_sentence:
                            link = Link(characterA_id=character_a.id,
                                        characterB_id=character_b.id,
                                        ns=ns,
                                        sentence=' '.join(book_chapter.tokenized_content[isent]))
                            chapters_link = ChapterLink(chapter_nb=book_chapter.nb,
                                                        chapter_nc=book_chapter.nc,
                                                        link=link)
                            db.session.add(chapters_link)
                            db.session.add(link)


def postprocess_scut_links():
    def get_location(characterid, nb, nc):
        travel = db.session.query(CharacterTravel).get((characterid, nb, nc))
        if travel is not None:
            return travel.location
        else:
            pass

    for chapter_link in db.session.query(ChapterLink).all():
        link = chapter_link.link

        locationA = get_location(link.characterA.id, chapter_link.chapter_nb, chapter_link.chapter_nc)
        locationB = get_location(link.characterB.id, chapter_link.chapter_nb, chapter_link.chapter_nc)

        link.is_scut = locationA is not None and locationB is not None and locationA != locationB

    db.session.commit()


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

