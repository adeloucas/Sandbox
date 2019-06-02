import os

from collections import Counter
from cltk.corpus.akkadian.file_importer import FileImport
from cltk.corpus.akkadian.cdli_corpus import CDLICorpus
from cltk.corpus.akkadian.tokenizer import Tokenizer
from cltk.tokenize.word import WordTokenizer

PARENT = os.path.expanduser('~')
FILE = os.path.join(PARENT, 'cltk_data', 'akkadian',
                    'atf', 'cdli_corpus', 'cdliatf_unblocked.atf')
FI = FileImport(FILE)
CC = CDLICorpus()
FI.read_file()
CC.parse_file(FI.file_lines)
LT = Tokenizer(preserve_damage=False)
WT = WordTokenizer('akkadian')

SEN = CC.catalog['P462830']['transliteration']
SEN_LINES = LT.string_tokenizer('\n'.join(SEN))
SEN_WORDS = WT.tokenize('\n'.join(SEN_LINES))

T = [word[0] for word in SEN_WORDS]
STOP_LIST = ['i-na', 'sza', 'a-na', 'u3', 'la', 'a-di', 'qe2-reb', 'ul-tu', 'pa-an', 'ki-ma', 'u']
WC = Counter([w for w in T if not w in STOP_LIST])

for i, pair in enumerate(WC.most_common(25)):
    print("{number:>5}. {word:<20}      {count:<12}". \
          format(number=i+1, word=pair[0], count=pair[1]))
