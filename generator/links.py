import contextlib
import itertools
import os

from generator.books import get_book_chapters, get_keys
from generator.chapter_characters import get_chapter_characters
from generator.travels import get_travels_book
from generator.utils import memoize


class Link(object):
    def __init__(self, char0, char1, scut, sentence):
        self.character0_id = char0.id
        self.character1_id = char1.id
        self.is_scut = scut
        self.sentence = sentence


@memoize()
def get_links(nb=None):
    chapters_books = get_book_chapters()
    travels = get_travels_book(nb)

    links = {}
    for k, book_chapter in chapters_books.items():
        nb, nc = k
        chapter_characters = get_chapter_characters(k)

        for isent, tokenized_sentence in enumerate(book_chapter.tokenized_content):
            ns = isent + 1
            for character_pair in itertools.combinations(chapter_characters, 2):
                character0 = character_pair[0]
                character1 = character_pair[1]
                location0 = travels.get((character0.id, nb, nc))
                location1 = travels.get((character1.id, nb, nc))

                for name0 in character0.all_names:
                    for name1 in character1.all_names:
                        if character1.id > character0.id \
                                and name0 in tokenized_sentence \
                                and name1 in tokenized_sentence:
                            is_scut = location0 != {} and location1 != {} and location0 != location1
                            links[nb, nc, ns] = Link(character0, character1, is_scut,
                                                     book_chapter.sentences[isent])
                            pass

    links = postprocess(links)
    write_links(links)

    return links


def postprocess(links):
    def remove(nb, nc, ns):
        try:
            del links[nb, nc, ns]
            del links[nb, nc, ns]
        except KeyError:
            pass

    def fix(nb, nc, ns, c0_id, c1_id):
        link = links.get((nb,nc,ns))
        if link is not None:
            link.character0_id = c0_id
            link.character1_id = c1_id

    # Tom Hanks
    remove(1, 13, 88)

    # '"And with Archimedes gone, well…" "Will we be okay?"'
    remove(3, 69, 53)

    fix(1, 60, 96, 'Fred', 'Bill')
    fix(1, 60, 177, 'Fred', 'Bill')

    return links


def write_links(links):
    keep = {}
    file_name = lambda nb, nc: os.path.join('generated', 'links', str(nb), '%d %d' % (nb, nc))
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
            to_write = '{:^10s} {:^10s} {:3d} {:3d} {:3d} {:s}\n'.format(link.character0_id, link.character1_id, nb, nc,
                                                                         ns, link.sentence)
            links_file.write(to_write)
            print(to_write)

    for k in get_keys():
        if not keep.get(k):
            os.remove(file_name(*k))


if __name__ == '__main__':
    write_links(get_links())
