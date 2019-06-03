"""
ORACC File Reader. Ideally a one-stop shop of taking ORACC data and absorbing it
for analysis akin to CDLI data for CLTK. If not, FileImport and 'Reader' can be
separated off just like File Importer and CDLI Importer currently on CLTK.

Right now, I am working on 'load corpus', which will, upon acknowledgement that
ones file system is as was downloaded from ORACC's .json files accessible at
https://github.com/oracc/json, it will take the .catalogue and subsequent
'corpusjson' folder and its derivative .json files and allow users to take
text on an individual and corpus-level basis and prepare the texts for analysis.
"""

import json
import os

__author__ = ['Andrew Deloucas <ADeloucas@g.harvard.com>']
__license__ = 'MIT License. See LICENSE.'


class FileImport(object):
    """
    Takes a text file and prepares it in two ways: as a whole (raw_file) and as
    a list of strings denoting the text line by line.
    """
    def __init__(self, filename):
        """
        :param filename: catalogue.json file from downloaded corpus from ORACC.
        """
        self.filename = filename

    def read_catalogue(self):
        """
        Takes a text file and prepares it for analysis.
        """
        if self.filename.endswith('catalogue.json'):
            with open(self.filename, encoding="utf8") as json_file:
                self.filedata = json.load(json_file)  # pylint: disable= attribute-defined-outside-init
                # print('Catalogue is ready.')
        else:
            print('File must be catalogue.json.')

    def load_corpus(self):
        """
        Loads 'corpusjson' folder associated with catalogue.
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
        Prints catalogue
        :return: printed catalogue
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
