import json
import os
import string
import nltk

from genealogy import get_genealogy, get_characters, get_characters_map
from readcombined import get_book_chapters


def extract_named_entities():
    chapters_books = json.load(open(os.path.join('generated', 'Combined.json')))

    content = []
    for nb, book_chapters in enumerate(chapters_books):
        for nc, book_chapter in enumerate(book_chapters):
            content.extend(book_chapter['content'])

    content = '\n'.join(content)

    sentences = nltk.sent_tokenize(content)

    tokenized_sentences = [nltk.word_tokenize(sentence) for sentence in sentences]
    tagged_sentences = [nltk.pos_tag(sentence) for sentence in tokenized_sentences]
    chunked_sentences = nltk.ne_chunk_sents(tagged_sentences, binary=True)

    def extract_entity_names(t):
        entity_names = []

        if hasattr(t, 'label') and t.label():
            if t.label() == 'NE':
                entity_names.append(' '.join([child[0] for child in t]))
            else:
                for child in t:
                    entity_names.extend(extract_entity_names(child))

        return entity_names

    entity_names = []

    for tree in chunked_sentences:
        # Print results per sentence
        print(extract_entity_names(tree))

        entity_names.extend(extract_entity_names(tree))

    print(set(entity_names))


def get_capitalized():
    characters_map = get_characters_map()

    chapters_books = get_book_chapters()

    content = []
    for nb, book_chapters in enumerate(chapters_books):
        for nc, book_chapter in enumerate(book_chapters):
            content.extend(book_chapter['content'])

    content = ' '.join(content)
    content = content.split()
    for i, w in enumerate(content):
        if w.strip() == '.':
            content[i + 1] = content[i + 1].lower()
    content = [el for el in content if el.strip() != '']
    new_content = []
    for el in content:
        new_content.append("".join(l for l in el if l not in string.punctuation))

    content = new_content
    content = [el for el in content if len(el) > 2]
    content = {el for el in content if el[0].upper() == el[0]}

    for character_id, character in characters_map.items():
        if character['name'] in content:
            content.remove(character['name'])
        if 'other_names' in character:
            for name in character['other_names']:
                if name in content:
                    content.remove(name)

    content = list(set(content))

    open(os.path.join('generated', 'capitalized'), 'w', encoding='utf-8').writelines(
        [el + '\n' for el in sorted(content)])
    pass


if __name__ == '__main__':
    extract_named_entities()
