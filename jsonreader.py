"""
The Importer feature sets up the ability to work with cuneiform text(s)
from ORACC.

This module is for ingesting and preparing ORACC text files for textual
analysis.

ORACC can be downloaded through CLTK:
    from cltk.corpus.utils.importer import CorpusImporter
    corpus_importer = CorpusImporter('Akkadian')
    corpus_importer.import_corpus('ORACC')
or otherwise downloaded from ORACC's GitHub:
    https://github.com/oracc/json

This module is dependent upon the structure CLTK unzips ORACC files,
see ORACC_Importer for more information.
"""

__author__ = ['Andrew Deloucas <ADeloucas@g.harvard.com>']
__license__ = 'MIT License. See LICENSE.'


class Reader(object):
    """
    Fulfills function of parsing text files via sentences, if avaiable,
    or line-by-line (WIP). Parsed work is available in transliteration
    and possibly normalization, cuneiform reconstruction, or etc., depending
    on the level of annotation for each independent text.
    """
    def __init__(self, filedata):
        """
        :param filename: catalogue.json file from downloaded corpus from ORACC.
        """
        self.filedata = filedata
        self.texts = filedata['members']
        self.failed_texts = []

    def __parse_sentence__(self):
        """
        Takes CDL data from a text and parses data into established sentences.
        :return: self.sentences for further parsing.
        """
        self.sentences = {}   # pylint: disable=attribute-defined-outside-init
        for text in self.textanalysis:
            if text['type'] == 'sentence':
                if 'label' not in text:
                    self.sentences[text['type']] = text['cdl']
                else:
                    self.sentences[text['label']] = text['cdl']
            elif text['type'].startswith('non'):
                pass
            else:
                try:
                    self.sentences['Sentence'] = text['cdl']
                except KeyError:
                    pass

    def __transliteration__(self):
        """
        Looks at either sentence or line-by-line structure and outputs
        transliteration.
        :return: transliteration found in each text's textdata.
        """
        self.__parse_sentence__()
        self.text = []  # pylint: disable=attribute-defined-outside-init
        for k, values in self.sentences.items():  # pylint: disable=redefined-outer-name
            self.text.append(k)
            line = []
            for key in values:
                if key['node'] == 'd':
                    if 'label' in key.keys():
                        if len(line) > 0:  # pylint: disable=len-as-condition
                            self.text.append(line)
                        line = key['label'] + '. '
                    else:
                        try:
                            line += key['frag'] + ' '
                        except KeyError:
                            line += ''
                elif key['node'] == 'l':
                    if len(line) == 0:  # pylint: disable=len-as-condition
                        line = k.split(' -')[0] + '. '
                    try:
                        if '\\' in key['frag']:
                            line += key['f']['form'] + ' '
                        else:
                            line += key['frag'] + ' '
                    except KeyError:
                        line += key['f']['form'] + ' '
                elif key['node'] == 'c':
                    if key['type'] == 'phrase':
                        for node in key['cdl']:
                            for k, v in node.items():
                                if k == 'f':
                                    line += v['form'] + ' '
                    else:
                        for node in key['cdl']:
                            try:
                                line += ' ' + node['frag']
                            except KeyError:
                                try:
                                    line += ' ' + node['cdl'][0]['frag']
                                except KeyError:
                                    line += 'ERROR! '
                else:
                    line += '~~~'
            self.text.append(line)
        self.textdata['transliteration'] = self.text

    def __normalization__(self):
        """
        Looks at either sentence or line-by-line structure and outputs
        normalization.
        :return: normalization found in each text's textdata.
        """
        self.__parse_sentence__()
        self.text = []  # pylint: disable=attribute-defined-outside-init
        for k, v in self.sentences.items():
            self.text.append(k)
            line = []
            for key in v:
                if key['node'] == 'd':
                    if 'label' in key.keys():
                        if len(line) > 0:  # pylint: disable=len-as-condition
                            self.text.append(line)
                        line = key['label'] + '. '
                    else:
                        try:
                            line += key['f']['norm'] + ' '
                        except KeyError:
                            line += ''
                elif key['node'] == 'l':
                    if len(line) == 0:  # pylint: disable=len-as-condition
                        line = k.split(' -')[0] + '. '
                    try:
                        if '\\' in key['f']['norm']:
                            line += key['f']['form'] + ' '
                        else:
                            line += key['f']['norm'] + ' '
                    except KeyError:
                        line += key['f']['form'] + ' '
                elif key['node'] == 'c':
                    if key['type'] == 'phrase':
                        for node in key['cdl']:
                            for k, v in node.items():
                                if k == 'f':
                                    line += v['form'] + ' '
                    else:
                        for node in key['cdl']:
                            try:
                                line += ' ' + node['f']['norm']
                            except KeyError:
                                try:
                                    line += ' ' + node['cdl'][0]['f']['norm']
                                except KeyError:
                                    line += 'ERROR! '
                else:
                    line += '~~~'
            self.text.append(line)
        self.textdata['normalization'] = self.text

    def __ingest_text__(self, call_number):  # pylint: disable=too-many-branches
        """
        Reads cdl documentation and outputs information into sections to be printed later.
        :param call_number: Text to be accessed in filedata[members] This is automatic
                            via ingest_corpus.
        :return: transliteration and normalization (in call_number.textdata), as well as
                 a list of failed texts (mostly due to being empty) that filters out
                 texts for print_toc.
        """
        if 'text_file' in self.texts[call_number]:
            self.metadata = self.texts[call_number]  # pylint: disable=attribute-defined-outside-init
            self.textdata = self.texts[call_number]['text_file']  # pylint: disable= attribute-defined-outside-init
            for node in self.textdata['cdl']:
                if 'linkbase' in node.keys():
                    pass
                else:
                    if node['node'] == 'c' and 'cdl' in node.keys():
                        # don't need this information for now.
                        # obj_type.append(node['type'])
                        obj = node['cdl']
                        for cdl in obj:
                            # don't need this information for now.
                            # if cdl['node'] == 'd':
                            #     obj_detail.append(cdl['subtype'])
                            if cdl['node'] == 'c' and 'cdl' in cdl.keys():
                                self.textanalysis = cdl['cdl']  # pylint: disable=attribute-defined-outside-init
                                self.__transliteration__()
                                self.__normalization__()
        else:
            self.failed_texts.append(call_number)
            print('{text} did not ingest; text either empty or missing. '
                  '(Text Fail 1)'.format(text=call_number))

    def ingest_corpus(self):
        """
        Reads corpus. Main feature to use.
        :return: Each text "ingested"; see __ingest_text__ for more information.
        """
        print('Ingesting corpus...')
        for call_number in self.texts:
            self.__ingest_text__(call_number)
        print()

    def print_toc(self):
        """
        Prints the items available for individual printing. Unviewable texts are
        not included.
        """
        print('Available Texts:')
        print()
        print("{number:>8} {text:<40} {id_composite:<10}". \
              format(number='', text='Publication Name', id_composite='Call Number'))
        print('       -------------------------------')
        texts = self.filedata['members']
        for i, ind_text in enumerate(texts.items()):
            if ind_text[0] not in self.failed_texts:
                print("{number:>6}.| {text:<40} {id_composite:<10}". \
                  format(number=i+1, text=next( \
                    a for b, a in ind_text[1].items() if 'pub' in b or 'designation' in b),
                         id_composite=next( \
                             v for k, v in ind_text[1].items() if 'id_' in k)))
        print()

    def print_single_text_sentences(self, call_number, catalog_filter=[]):
        """
        Prints and ingests only the one text.
        :param call_number: text you wish to print.
        :return:
        """
        text = self.texts[call_number]['text_file']
        self.lines = []
        if len(catalog_filter) > 0:  # pylint: disable=len-as-condition
            if catalog_filter in text:
                if catalog_filter == 'transliteration':
                    lines = []
                    for string in text[catalog_filter]:
                        if '.' in string[0:8]:
                            lines.append(string.split('. ')[1])
                    self.lines = '\n'.join(lines)
                elif text[catalog_filter] == text['transliteration']:
                    print('Filter not available.')
                else:
                    lines = []
                    for string in text[catalog_filter]:
                        if '.' in string[0:8]:
                            lines.append(string.split('. ')[1])
                    self.lines = '\n'.join(lines)
                print(self.lines)
            else:
                print('not a filter, use text_information for available filters.')
        # don't know if i need this...
        #else:
        #    try:
        #        print('\n'.join(text['transliteration']))
        #    except TypeError:
        #        print('\n'.join([str(line) for line in text['transliteration']]))
        #    except KeyError:
        #        print('Text does not exist in this corpus.')

    def print_single_text(self, call_number):
        """
        Prints one text line by line.
        :param call_number: text you wish to print.
        :return:
        """
        self.__ingest_text__(call_number)
        lines = []   # pylint: disable=attribute-defined-outside-init
        self.tablet = []  # pylint: disable=attribute-defined-outside-init
        for text in self.textanalysis:
            for k, v in text.items():  # pylint: disable=redefined-outer-name
                if k == 'cdl':
                    lines.append(v)
        for sets in lines:
            line = []
            for key in sets:
                if key['node'] == 'd':
                    if 'label' in key.keys():
                        if len(line) > 0:  # pylint: disable=len-as-condition
                            self.tablet.append(line)
                        line = key['label'] + '. '
                    else:
                        try:
                            line += key['frag'] + ' '
                        except KeyError:
                            line += ''
                elif key['node'] == 'l':
                    if len(line) == 0:  # pylint: disable=len-as-condition
                        if key.keys() != 'frag':
                            line += key['f']['form'] + ' '
                            self.tablet[-1] += ''.join(line)
                            line = []
                        else:
                            if '\\' in key['frag']:
                                line += key['f']['form'] + ' '
                                self.tablet[-1] += ''.join(line)
                                line = []
                            else:
                                line += key['frag'] + ' '
                                self.tablet[-1] += ''.join(line)
                                line = []
                    else:
                        try:
                            if '\\' in key['frag']:
                                line += key['f']['form'] + ' '
                            else:
                                line += key['frag'] + ' '
                        except KeyError:
                            line += key['f']['form'] + ' '
                elif key['node'] == 'c':
                    if key['type'] == 'phrase':
                        if len(line) == 0:  # pylint: disable=len-as-condition
                            for node in key['cdl']:
                                for k, v in node.items():
                                    if k == 'f':
                                        line += v['form'] + ' '
                                        self.text[-1] += ''.join(line)
                                        line = []
                        else:
                            for node in key['cdl']:
                                for k, v in node.items():
                                    if k == 'f':
                                        line += v['form'] + ' '
                    else:
                        for node in key['cdl']:
                            try:
                                line += ' ' + node['frag']
                            except KeyError:
                                try:
                                    line += ' ' + node['cdl'][0]['frag']
                                except KeyError:
                                    line += 'ERROR! '
                else:
                    line += '~~~'
            self.tablet.append(line)
        print('\n'.join(self.tablet))
