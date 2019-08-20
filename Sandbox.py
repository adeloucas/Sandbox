"""
JSON File Reader Trial
"""

from oracc_importer import FileImport
from oracc_importer import ORACCUnzip
from jsonreader import Reader
import os

## Runs  unzip function.
#
parent_directory = os.path.expanduser('~')
folder = os.path.join( \
    parent_directory, 'Python', 'json-master', 'json-master')
target = os.path.join(parent_directory)
FI = ORACCUnzip(folder, parent_directory)
FI.unzip()
#
## Directs program to look at wherever your json files are stored.
# Imports catalogue directed toward, reads, and loads it.
#
file = os.path.join( \
    parent_directory, 'ORACC-Files', 'rinap', 'rinap3', 'catalogue.json')                    # target catalogue
#
## Loads corpus, looks for text file errors
#
FI = FileImport(file)
print()
FI.read_catalogue()
FI.load_corpus()
#FI.print_catalogue() # essentially useless function outside debugging

## Ingests texts on a corpus or single level basis from FileImport
#
RE = Reader(FI.filedata)
RE.ingest_corpus()
#RE.print_toc()
RE.print_single_text_sentences('Q003497', 'normalization')
print()
#RE.print_single_text('Q003497')
# Toying with ability to use tokenizers on text...


from collections import Counter
from cltk.corpus.akkadian.tokenizer import Tokenizer
line_tokenizer = Tokenizer(preserve_damage=False)
from cltk.tokenize.word import WordTokenizer
word_tokenizer = WordTokenizer('akkadian')
from nltk import Text

sennacherib = line_tokenizer.string_tokenizer(RE.lines)
sennacherib_tokens = word_tokenizer.tokenize('\n'.join(sennacherib))
s_tokens = [word[0] for word in sennacherib_tokens]
word_count = Counter(s_tokens)

running = 0
print("Top 25 words in the Taylor's Prism:\n")
print("{number:>5}  {word:<20}     {count:<12}{percent:<12}{running:<12}". \
      format(number="", word="TOKEN", count="COUNT", percent="TOKEN %", running = "RUNNING %"))
for i, pair in enumerate(word_count.most_common(25)):
    running += pair[1]
    print("{number:>5}. {word:<20}      {count:<12}{percent:<12}{running:<12}". \
          format(number=i+1, word=pair[0], count=pair[1], \
                 percent=str(round(pair[1] / len(s_tokens)*100, 2))+"%", running = str(round(running / len(s_tokens)*100, 2))+"%"))
print()
Sennacherib_Text = Text(s_tokens) # Note that Text takes a list of tokens as its input
Sennacherib_Text.concordance('Aššur')
