import contextlib
import itertools

import os
import shutil

from generator.books import get_book_chapters, get_keys
from generator.chapter_characters import get_chapter_characters
from generator.characters import get_characters_map
from generator.travels import get_travels_book
from generator.utils import memoize


class Link(object):
    def __init__(self, char0, char1, scut, sentence):
        self.character0 = char0
        self.character1 = char1
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
                        if name0 > name1 and name0 in tokenized_sentence and name1 in tokenized_sentence:
                            is_scut = location0 != {} and location1 != {} and location0 != location1
                            links[nb, nc, ns, character0.id, character1.id] = Link(character0, character1, is_scut,
                                                                                   book_chapter.sentences[isent])
                            pass

    links = postprocess(links)

    return links


def postprocess(links):
    def remove(nb, nc, ns, c0, c1):
        try:
            del links[nb, nc, ns, c0, c1]
            del links[nb, nc, ns, c1, c0]
        except KeyError:
            pass

    # '"And with Archimedes gone, well…" "Will we be okay?"'
    remove(3, 69, 53, 'Riker', 'Archimedes')

    return links


def write_links(links):
    keep = {}
    file_name = lambda nb,nc: os.path.join('generated', 'links', str(nb), '%d %d' % (nb, nc))
    with contextlib.ExitStack() as stack:

        links_files = {}
        for nb, nc in get_keys():
            os.makedirs(os.path.join('generated', 'links', str(nb)), exist_ok=True)
            links_files[nb, nc] = stack.enter_context(
                open(file_name(nb, nc), 'w',
                     encoding='utf-8'))

        for (nb, nc, ns, c0id, c1id), link in links.items():
            if link.is_scut:
                continue
            links_file = links_files[nb, nc]
            keep[nb, nc] = True
            to_write = '{:^10s} {:^10s} {:3d} {:3d} {:3d} {:s}\n'.format(c0id, c1id, nb, nc, ns, link.sentence)
            links_file.write(to_write)
            print(to_write)

    for k in get_keys():
        if not keep.get(k):
            os.remove(file_name(*k))



if __name__ == '__main__':
    write_links(get_links())
