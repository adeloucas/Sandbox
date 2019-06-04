"""
The Importer feature sets up the ability to work with cuneiform text(s)
one-on-one, whether it is the Code of Hammurabi, a collection of texts such as
ARM01, or whatever your research desires.

This oracc_importer module is for unzipping text files downloaded through
CLTK's corpora, as well as importing the texts for further work.

ORACC can be downloaded through CLTK:
    from cltk.corpus.utils.importer import CorpusImporter
    corpus_importer = CorpusImporter('Akkadian')
    corpus_importer.import_corpus('ORACC')
or otherwise downloaded from ORACC's GitHub:
    https://github.com/oracc/json
"""

import json
import os
from zipfile import ZipFile

__author__ = ['Andrew Deloucas <ADeloucas@g.harvard.com>']
__license__ = 'MIT License. See LICENSE.'


class ORACCUnzip(object):  # pylint: disable=too-few-public-methods
    """
    This class is necessary if ORACC .json data has just been
    recently downloaded, but hasn't been manually unzipped yet.

    It needs two requirements:
    1) Folder = location of ORACC files, most commonly:
        os.path.join(os.path.expanduser('~'), \
                     'Python', 'json-master', 'json-master')
    2) Target Directory Location = where you'd like to unzip
       the files for ease of access.
    """
    def __init__(self, folder, target_directory_location):

        self.folder = folder
        self.zip = []
        self.target_directory_location = target_directory_location

    def unzip(self):
        """
        This function unzips your documents.
        :return: A folder with all the .json documents downloaded.
        """
        for f in os.walk(self.folder):  # pylint: disable=invalid-name
            for x in f[2]:  # pylint: disable=invalid-name
                if x.endswith('.zip'):
                    self.zip.append(x)
        cwd = os.getcwd()
        os.chdir(self.folder)
        for file in self.zip:
            with ZipFile(file, 'r') as zip_obj:
                zip_obj.extractall(self.target_directory_location)
        os.chdir(cwd)


class FileImport(object):
    """
    This class checks for .json files (read_catalogue) and imports their
    text for further work (load_corpus). Examining the files can be done
    through 'print_catalogue'.
    """
    def __init__(self, filename):
        """
        :param filename: catalogue.json file from downloaded corpus from ORACC.
        Note, if you've used CLTK's corpus importer to import ORACC's json files,
        you may need to unzip the folders that were downloaded. See above notes
        for further information.
        """
        self.filename = filename

    def read_catalogue(self):
        """
        Looks for catalogue of publications listed in particular volumes. Does not
        currently work for series (e.g. saao/saa01 works, but not saao).
        """
        if self.filename.endswith('catalogue.json'):
            with open(self.filename, encoding="utf8") as json_file:
                self.filedata = json.load(json_file)  # pylint: disable= attribute-defined-outside-init
                print('Catalogue is ready.')
        else:
            print('File must be catalogue.json.')

    def load_corpus(self):
        """
        Loads 'corpusjson' folder associated into catalogue for future calling.
        :return: added dictionary value in .catalogue file containing the json file of the text?
                 Maybe just a reference to the .json file? Is that even possible?
        """
        pathway = os.path.split(self.filename)
        self.catalog = sorted(os.listdir(pathway[0]))  # pylint: disable= attribute-defined-outside-init
        for file in self.catalog:
            if not file == 'corpusjson':
                pass
            else:
                corpus = os.path.join(pathway[0], 'corpusjson')
                os.chdir(corpus)
                for ind_text in os.listdir(corpus):
                    if ind_text.endswith('.json'):
                        # print('{x} has been loaded!'.format(x=ind_text))
                        f_i = open(ind_text, encoding="utf8")
                        data = json.load(f_i)
                        f_i.close()
                        if self.filedata['members'][data['textid']]:
                            self.filedata['members'][data['textid']].update({'text_file': data})
                        else:
                            print('error!')
                    else:
                        print('{x} is not .json file; ignored.'.format(x=ind_text))

    def print_catalogue(self):
        """
        Prints catalogue. Currently only works with corpora that use "id_composite";
        there are other corpora that use other definitions that need to be considered.
        :return: printed catalogue of texts in a corpus.
        """
        try:
            if self.filedata:
                print('Catalogue of Texts:')
                print()
                print("{number:>8} {text:<20} {id_composite:<10}". \
                      format(number='', text='Publication Name', id_composite='Call Number'))
                print('       -------------------------------')
                texts = self.filedata['members']
                for i, text in enumerate(texts.items()):
                    #
                    # Not every catalogue uses this naming format... ideally can spot any "id":
                    #
                    # ex:
                    # test = next( v for k,v in text[1].items() if k.startswith('Date'))
                    #    [ v for k,v in text[1].items() if k.startswith('id')]
                    #
                    try:
                        print("{number:>6}.| {text:<20} {id_composite:<10}". \
                              format(number=i+1, text=text[1]['display_name'],
                                     id_composite=text[1]['id_composite']))
                    except KeyError:
                        print("{number:>6}.| {text:20} {message}". \
                              format(number=i+1, text=text[0], message='KeyError!'))
        except AttributeError:
            print("Must 'read_catalogue' first!")
