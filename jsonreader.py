"""
WIP: ingest text is almost entirely based off work based off work by Willis Monroe:
https://gist.github.com/willismonroe/e3dbc9ba0ee834befae82fb641535783
"""

__author__ = ['Andrew Deloucas <ADeloucas@g.harvard.com>']
__license__ = 'MIT License. See LICENSE.'

class Reader(object):
    """
    Fulfills function of calling both individual and corpus level texts for analysis
    """
    def __init__(self, filedata):
        """
        :param filename: catalogue.json file from downloaded corpus from ORACC.
        """
        self.filedata = filedata
        self.texts = filedata['members']

    def __ingest_text__(self, call_number):  # pylint: disable=too-many-branches
        """
        Reads cdl documentation and outputs information into sections to be printed later.
        Can be used on a single text, otherwise is used on each text in ingest_corpus.
        :param call_number: Whichever text you wish to access in filedata[members]
        :return:
        """
        self.data = self.texts[call_number]['text_file']  # pylint: disable= attribute-defined-outside-init
        for node in self.data['cdl'][0]['cdl']:
            if 'cdl' in node.keys():
                self.text = node['cdl'][0]['cdl']  # pylint: disable= attribute-defined-outside-init

        transliteration = []
        line = ''
        for node in self.text:
            if node['node'] == 'd' and 'label' in node.keys():
                transliteration.append(line)
                line = node['label'] + '.'
            elif node['node'] == 'l':
                line += ' ' + node['frag']
        transliteration.append(line)
        normalization = []
        line = ''
        for node in self.text:
            if node['node'] == 'd' and 'label' in node.keys():
                normalization.append(line)
                line = node['label'] + '.'
            elif node['node'] == 'l':
                if 'norm' in node['f'].keys():
                    line += ' ' + node['f']['norm']
                else:
                    line += ' ' + node['f']['form']
        normalization.append(line)
        lit_trans = []
        line = ''
        for node in self.text:
            if node['node'] == 'd' and 'label' in node.keys():
                lit_trans.append(line)
                line = node['label'] + '.'
            elif node['node'] == 'l':
                if 'sense' in node['f'].keys():
                    line += ' ' + node['f']['sense']
                else:
                    line += ' ' + node['f']['form']
        lit_trans.append(line)

        self.data.update({'transliteration': transliteration})
        self.data.update({'normalization': normalization})
        self.data.update({'lit_trans': lit_trans})

        return # print('{text} ingested. \n'
                     # '{len1} lines of transliteration \n'
                     # '{len2} lines of normalization \n'
                     # '{len3} lines of literal translation'. \
                     # format(text=call_number, len1=len(transliteration)-1,
                     #        len2=len(normalization)-1, len3=len(lit_trans)-1))

    def print_single_text(self, call_number):
        """
        Prints and ingests only the one text.
        :param call_number: text you wish to print.
        :return:
        """

        self.__ingest_text__(call_number)
        print()
        print('Transliteration:')
        print('\n'.join(self.data['transliteration'][1:]))
        print()
        print('Normalization:')
        print('\n'.join(self.data['normalization'][1:]))
        print()
        print('Literal Translation:')
        print('\n'.join(self.data['lit_trans'][1:]))

    def print_toc(self):
        """
        Prints the items available for individual printing...
        """
        print('Table of Contents:')
        print('\n'.join([x for x in self.texts]))

    def ingest_corpus(self):
        """
        Reads a single text
        :param call_number: Whichever text you wish to access in filedata[members]
        :return: the text
        """
        print('Ingesting corpus...')
        for call_number in self.texts:
            self.__ingest_text__(call_number)
            print('{x} is ingested!'.format(x=call_number))
