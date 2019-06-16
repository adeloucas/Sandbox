"""
JSON File Reader Trial
"""

from oracc_importer import FileImport
# from oracc_importer import ORACCUnzip
from jsonreader import Reader
import os


## Runs  unzip function.
#
parent_directory = os.path.expanduser('~')
#folder = os.path.join(parent_directory, 'Python', 'json-master', 'json-master')
#target = os.path.join(parent_directory)
#FI = ORACCUnzip(folder, parent_directory)
#FI.unzip()


## Directs program to look at wherever your json files are stored. Imports catalogue
#  directed toward, reads, and loads it.
#
file = os.path.join(parent_directory, 'ORACC-Files',     # location of files (from unzip)
                    'cams', 'gkab',                   # corpus
                    'catalogue.json')                    # target catalogue


## Loads corpus, looks for text file errors
#
FI = FileImport(file)
print()
FI.read_catalogue()
FI.load_corpus()
print()
#FI.print_catalogue() # essentially useless function outside debugging


## Ingests texts on a corpus or single level basis from FileImport
#
RE = Reader(FI.filedata)
RE.ingest_corpus()
RE.print_toc()

RE.text_information('P424508')
RE.print_single_text('P424508')

