import os

from collections import Counter
from cltk.corpus.akkadian.file_importer import FileImport
from cltk.corpus.akkadian.cdli_corpus import CDLICorpus
from cltk.corpus.akkadian.tokenizer import Tokenizer
from cltk.tokenize.word import WordTokenizer
from cltk.stem.akkadian.atf_converter import ATFConverter

PARENT = os.path.expanduser('~')
FILE = os.path.join(PARENT, 'cltk_data', 'akkadian',
                    'atf', 'cdli_corpus', 'cdliatf_unblocked.atf')
FI = FileImport(FILE)
CC = CDLICorpus()
FI.read_file()
CC.parse_file(FI.file_lines)

atf = ATFConverter()
tk = Tokenizer()
WT = WordTokenizer('akkadian')

SEN = CC.catalog['P462830']['transliteration']
LT = [tk.string_tokenizer(text, include_blanks=False) for text in atf.process(SEN)]
words = [WT.tokenize(line[0]) for line in LT]

toto_signs = []

for signs in words:
    individual_words = [WT.tokenize_sign(a) for a in signs]
    individual_signs = [c for b in individual_words for c in b]
    for count in individual_signs:
        toto_signs.append(count)

frequency_analysis = Counter(toto_signs).most_common(15)
print(frequency_analysis)
