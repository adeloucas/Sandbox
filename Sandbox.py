"""
JSON File Reader.
"""

from jsonreader import FileImport
import os

## The following directs the program to look at wherever your json files are stored.

parent_directory = os.path.expanduser('~')
file = os.path.join(parent_directory, 'Python', 'Sandbox', 'rinap32', 'catalogue.json')
# print(os.path.isfile(file))
# print(file)

## This Feature imports the .json catalogue it was directed toward, then reads(, prints,) and loads it.

FI = FileImport(file)
FI.read_catalogue()
# (Optional, but probably best after loading corpus so one can know which text they wish to analyze?)
FI.print_catalogue()
print()
#
FI.load_corpus()

## From here, import a "call" feature, which lets you analyze corpora on a publication and individual text basis.
## Right now, this is being set up also in jsonreader.py, but under the class "Reader", bracketed out.