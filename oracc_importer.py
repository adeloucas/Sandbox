"""
The Importer feature sets up the ability to work with cuneiform text(s)
from ORACC.

This module is for unzipping ORACC text files downloaded through
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
    This class is necessary if ORACC .json data have just been
    recently downloaded, but haven't been manually unzipped yet.

    It needs two requirements:
    1) Folder = location of ORACC files, most commonly
       'os.path.join(os.path.expanduser('~'), 'Python', 'json-master', 'json-master')
    2) Target Directory = location where you'd like
       to unzip.
    """
    def __init__(self, folder, target_directory):

        self.folder = folder
        self.zip = []
        self.target_directory = target_directory

    def unzip(self):
        """
        This function unzips your documents.
        :return: A folder with all the .json documents unzipped.
        """
        for f in os.walk(self.folder):  # pylint: disable=invalid-name
            for x in f[2]:  # pylint: disable=invalid-name
                if x.endswith('.zip'):
                    self.zip.append(x)
        cwd = os.getcwd()
        os.chdir(self.folder)
        for file in self.zip:
            with ZipFile(file, 'r') as zip_obj:
                try:
                    os.mkdir('ORACC-Files')
                    destination = os.path.join(self.target_directory, 'ORACC-Files')
                    zip_obj.extractall(destination)
                except FileExistsError:
                    destination = os.path.join(self.target_directory, 'ORACC-Files')
                    zip_obj.extractall(destination)
        os.chdir(cwd)


class FileImport(object):
    """
    This class checks for .json files (read_catalogue) and imports their
    text for further work (load_corpus). Usable files are viewable with
    the function 'print_catalogue'.

    Some notes:
        1) Arrim and ogsl don't work: ogsl is not text-based and arrim is empty.
        2) Similarly, aemw/alalakh/idrimi, armep, cmawro, nimrud, oimea, qcat,
           and xcat appear to be missing textual information as a whole.
        3) Within other corpora, there appear to be missing textual information
           as well, though on a lesser scale. These texts are printing out
           as issues occur.
        4) Load_corpus has two unknown bugs:
            1) 127-140: Some texts run KeyErrors, and I don't know why.
            2) 148-152: Some json files for particular texts are empty.
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
        Looks for catalogue of publications listed in particular volumes.
        Does not work for full series (e.g. saao/saa01 works, but not just saao/).
        """
        if self.filename.endswith('catalogue.json'):
            with open(self.filename, encoding="utf8") as json_file:
                self.filedata = json.load(json_file)  # pylint: disable= attribute-defined-outside-init
                self.message = 'Catalogue is ready.'  # pylint: disable= attribute-defined-outside-init
        else:
            self.message = 'File must be catalogue.json.'  # pylint: disable= attribute-defined-outside-init
        print(self.message)

    def load_corpus(self):
        """
        Loads 'corpusjson' folder associated into catalogue for future calling.
        :return: added dictionary value in .catalogue file containing json file
        information.
        """
        self.read_corpus = []                          # pylint: disable= attribute-defined-outside-init
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
                        f_i = open(ind_text, encoding="utf8")
                        try:
                            data = json.load(f_i)
                            #
                            # There are a handful of texts that don't seem to work
                            # in the following folders, e.g.:
                            #
                            #      blms: Q003094, Q003097, Q003098, Q003099, Q003102,
                            #            Q003120, Q003122, Q003152 (8/1798 texts)
                            #      riao: P465673, X000123, X029979 (3/885 texts)
                            #   rimanum: P405202, P405400, P405406 (3/375 texts)
                            #     dcclt: P256059, X000101 (2/9211 texts)
                            #       1 each for rinap/sources, /scores, saao/saa04,
                            #                  /saa05, /saa08, /saa15, /saa18
                            #
                            # This except line allows the program to continue running
                            # outside of these edge cases. I have no idea why these
                            # KeyErrors have formed.
                            #
                            try:
                                self.filedata['members'][data['textid']].update({'text_file': data})
                                self.read_corpus.append(ind_text.split('.')[0])
                                # print('{x} has been loaded!'.format(x=ind_text))
                            except KeyError:
                                print('error loading {x}; reason unknown! '
                                      '(Text Fail 2)'.format(x=data['textid']))
                        #
                        # Some folders have empty json files, which disrupt
                        # the program; this exempts those files. They are not
                        # to be seen in the print_catalogue.
                        #
                        except json.decoder.JSONDecodeError:
                            print('{call_number} does not have information, '
                                  'did not load. (Text Fail 1)'. \
                                  format(call_number=ind_text))
                        f_i.close()
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
                print('Catalogue of Loaded Texts:')
                print()
                print("{number:>8} {text:<40} {id_composite:<10}". \
                      format(number='', text='Publication Name', id_composite='Call Number'))
                print('       -------------------------------')
                texts = self.filedata['members']
                for i, text in enumerate(texts.items()):
                    try:
                        if text[0] in self.read_corpus:
                            print("{number:>6}.| {text:<40} {id_composite:<10}". \
                                format(number=i+1, text=next( \
                                a for b, a in text[1].items() if 'pub' in b or 'designation' in b),
                                       id_composite=next( \
                                           v for k, v in text[1].items() if 'id_' in k)))
                    except KeyError:
                        print("{number:>6}.| {text:40} {message}". \
                              format(number=i+1, text=text[0], message='KeyError!'))
        except AttributeError:
            print("Must 'read_catalogue' first!")
