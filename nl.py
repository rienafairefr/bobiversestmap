import os

import nltk
import tempfile

tmpnltk_data = os.path.join(tempfile.gettempdir(), 'bob_nltk_data')
os.makedirs(tmpnltk_data, exist_ok=True)
required= ['maxent_ne_chunker',
           'words',
           'averaged_perceptron_tagger',
           'punkt']
for req in required:
    nltk.download(info_or_id=req, download_dir=tmpnltk_data)
nltk.data.path.append(tmpnltk_data)


def tokenize(lines):
    content = '\n'.join(lines)

    sentences = nltk.sent_tokenize(content)

    tokenized_sentences = [nltk.word_tokenize(sentence) for sentence in sentences]
    return tokenized_sentences
