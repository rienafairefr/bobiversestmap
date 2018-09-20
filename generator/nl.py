import os

import nltk
import tempfile

from dogpile.cache import make_region

from generator.utils import memoize


def download_ntlk():
    tmpnltk_data = os.path.join(tempfile.gettempdir(), 'bob_nltk_data')
    os.makedirs(tmpnltk_data, exist_ok=True)
    required= ['maxent_ne_chunker',
               'words',
               'averaged_perceptron_tagger',
               'punkt']
    for req in required:
        nltk.download(info_or_id=req, download_dir=tmpnltk_data)
    nltk.data.path.append(tmpnltk_data)


def word_tokenize(sentence):
    return nltk.word_tokenize(sentence)


def word_tokenize_sentences(sentences):
    return [word_tokenize(sentence) for sentence in sentences]


def sent_tokenize(content):
    return nltk.sent_tokenize(content)


def sentences_tokenize(lines):
    content = '\n'.join(lines)

    return sent_tokenize(content)
