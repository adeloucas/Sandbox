"""
JSON File Reader Trial
"""

from jsonimporter import FileImport
from jsonreader import Reader
import os

## The following directs the program to look at wherever your json files are stored.

parent_directory = os.path.expanduser('~')
file = os.path.join(parent_directory, 'Python', 'Sandbox', 'rinap32', 'catalogue.json')

## This feature imports the .json catalogue it was directed toward, then reads(, prints,) and loads it.

FI = FileImport(file)
#print()
#print("Read Catalogue:")
FI.read_catalogue()
#print()
#print("Load Corpus into Catalogue:")
FI.load_corpus()
#print()
#print('Print Catalogue:')
#FI.print_catalogue()
#print()

## This feature ingests texts on a corpus or single level basis from FileImport
# Still WIP

RE = Reader(FI.filedata)
print()
print('QTEST')
RE.print_single_text('QTEST')
print()
print('Q003475')
RE.print_single_text('Q003475')
print()
print("Print Text Keys:")
print()
RE.print_toc()
print()
RE.ingest_corpus()
print()
print(RE.data['textid'])
RE.__ingest_text__('Q003475')
print(RE.data['textid'])
# problem: data looks at last entry, not at every entry...
