import os

import itertools
import nltk
import tempfile

from genealogy import get_characters_map
from nl import tokenize
from readcombined import get_book_chapters
from utils import memoize, json_dump

tmpnltk_data = os.path.join(tempfile.gettempdir(), 'bob_nltk_data')
os.makedirs(tmpnltk_data, exist_ok=True)
required= ['maxent_ne_chunker',
           'words',
           'averaged_perceptron_tagger',
           'punkt']
for req in required:
    nltk.download(info_or_id=req, download_dir=tmpnltk_data)
nltk.data.path.append(tmpnltk_data)


@memoize()
def get_chapters_tokenized_sentences():
    chapters_books = get_book_chapters()

    chapters_tokenized_sentences = []

    for book_chapters in chapters_books:
        one_book = []
        for book_chapter in book_chapters:
            one_book.append(tokenize(book_chapter['content']))
        chapters_tokenized_sentences.append(one_book)
    return chapters_tokenized_sentences


@memoize()
def get_chapters_tagged_sentences():
    chapters_tokenized_sentences = get_chapters_tokenized_sentences()

    chapters_tagged_sentences=[]
    for one_book in chapters_tokenized_sentences:
        one_book_tagged = []
        for tokenized_sentences in one_book:
            chapters_tagged_sentences.append(nltk.pos_tag_sents(tokenized_sentences))

        chapters_tagged_sentences.append(one_book_tagged)

    return chapters_tagged_sentences


def get_characters_relationships(nb):
    chapters_tokenized_sentences = get_chapters_tokenized_sentences()
    characters = get_characters_map()

    book_characters_relationships = []

    for idxb, one_book in enumerate(chapters_tokenized_sentences):
        if nb is not None and (idxb+1!=nb):
            continue
        for one_chapter in one_book:
            link = []
            for tokenized_sentence in one_chapter:

                for character_pair in itertools.combinations(characters, 2):
                    if character_pair[0] in tokenized_sentence and character_pair[1] in tokenized_sentence:
                        link.extend(character_pair)
                        pass
            book_characters_relationships.append({'character_ids': list(set(link))})
    return book_characters_relationships


    content = []
    for (nb, nc), book_chapter in chapters_books.items():
        content.extend(book_chapter['content'])

                if hasattr(t, 'label') and t.label():
                    if t.label() == 'NE':
                        entity_names.append(' '.join([child[0] for child in t]))
                    else:
                        for child in t:
                            entity_names.extend(extract_entity_names(child))

                return entity_names

            entity_names = []

            chunked_sentences = nltk.ne_chunk_sents(one_chapter, binary=True)

            for tree in chunked_sentences:
                # Print results per sentence
                print(extract_entity_names(tree))

                entity_names.extend(extract_entity_names(tree))

            print(set(entity_names))


def write_characters_relationships():
    characters_relationships = get_characters_relationships()
    json_dump(characters_relationships, os.path.join('generated',"characters_relationships.json"))


if __name__ == '__main__':
    write_characters_relationships()
