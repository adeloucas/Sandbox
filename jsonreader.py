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
        self.failed_texts = []

    def __transliteration__(self):
        """

        :return:
        """
        section = []
        transliteration = []
        line = ''
        for text in self.data['cdl'][0]['cdl']:
            if text['node'] == 'c':
                section.append(text['cdl'])
        # checks if sections have sentence structure; otherwise taken as single text.
        for sentences in section:
            if len(sentences) > 6:
                for node in sentences:
                    if node['node'] == 'c':
                        transliteration.append(line)
                        line = node['label'] + '.'
                        for cdl in node['cdl']:
                            if cdl == 'd' and 'label' in cdl.keys():
                                line = cdl['label'] + '.'
                            elif cdl['node'] == 'l':
                                try:
                                    line += ' ' + cdl['frag']
                                except KeyError:
                                    line += ' ' + cdl['f']['form']
            else:
                for node in self.text:
                    if node['node'] == 'd' and 'label' in node.keys():
                        transliteration.append(line)
                        line = node['label'] + '.'
                    elif node['node'] == 'l':
                        try:
                            line += ' ' + node['frag']
                        except KeyError:
                            line += ' ' + node['f']['form']
        transliteration.append(line)
        self.data['transliteration'] = transliteration[1:]

    def __normalization__(self):
        """

        :return:
        """
        section = []
        normalization = []
        line = ''
        for text in self.data['cdl'][0]['cdl']:
            if text['node'] == 'c':
                section.append(text['cdl'])
        # checks if sections have sentence structure; otherwise taken as single text.
        for sentences in section:
            if len(sentences) > 6:
                for node in sentences:
                    if node['node'] == 'c':
                        normalization.append(line)
                        line = node['label'] + '.'
                        for cdl in node['cdl']:
                            if cdl == 'd' and 'label' in cdl.keys():
                                line = cdl['label'] + '.'
                            elif cdl['node'] == 'l':
                                try:
                                    line += ' ' + cdl['f']['norm']
                                except KeyError:
                                    line += ' ' + cdl['f']['form']
            else:
                for node in self.text:
                    if node['node'] == 'd' and 'label' in node.keys():
                        normalization.append(line)
                        line = node['label'] + '.'
                    elif node['node'] == 'l':
                        try:
                            line += ' ' + node['f']['norm']
                        except KeyError:
                            line += ' ' + node['f']['form']
        normalization.append(line)
        self.data['normalization'] = normalization[1:]

    def __cuneiform__(self):  # not working, same as transliteration for now
        """

        :return:
        """
        section = []
        transliteration = []
        line = ''
        for text in self.data['cdl'][0]['cdl']:
            if text['node'] == 'c':
                section.append(text['cdl'])
        # checks if sections have sentence structure; otherwise taken as single text.
        for sentences in section:
            if len(sentences) > 6:
                for node in sentences:
                    if node['node'] == 'c':
                        transliteration.append(line)
                        line = node['label'] + '.'
                        for cdl in node['cdl']:
                            if cdl == 'd' and 'label' in cdl.keys():
                                line = cdl['label'] + '.'
                            elif cdl['node'] == 'l':
                                try:
                                    line += ' ' + cdl['frag']
                                except KeyError:
                                    line += ' ' + cdl['f']['form']
            else:
                for node in self.text:
                    if node['node'] == 'd' and 'label' in node.keys():
                        transliteration.append(line)
                        line = node['label'] + '.'
                    elif node['node'] == 'l':
                        try:
                            line += ' ' + node['frag']
                        except KeyError:
                            line += ' ' + node['f']['form']
        transliteration.append(line)
        self.data['transliteration'] = transliteration[1:]

    def __ingest_text__(self, call_number):  # pylint: disable=too-many-branches
        """
        Reads cdl documentation and outputs information into sections to be printed later.
        Can be used on a single text, otherwise is used on each text in ingest_corpus.
        :param call_number: Whichever text you wish to access in filedata[members]
        :return:
        """
        if 'text_file' in self.texts[call_number]:
            self.data = self.texts[call_number]['text_file']  # pylint: disable= attribute-defined-outside-init
            for node in self.data['cdl'][0]['cdl']:
                if 'cdl' in node.keys():
                    self.text = node['cdl'][0]['cdl']  # pylint: disable= attribute-defined-outside-init
            self.__transliteration__()
            self.__normalization__()
            self.__cuneiform__()
        else:
            self.failed_texts.append(call_number)
            print('{text} did not ingest; text either empty or missing. (Text Fail 1)'.format(text=call_number))

    def ingest_corpus(self):
        """
        Reads a single text
        :param call_number: Whichever text you wish to access in filedata[members]
        :return: the text
        """
        print('Ingesting corpus...')
        for call_number in self.texts:
            self.__ingest_text__(call_number)
        print()

    def print_toc(self):
        """
        Prints the items available for individual printing...
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

    def text_information(self, call_number):
        info1 = []
        info2 = ['cdl', 'transliteration', 'normalization', 'cuneiform']  # add filters as they are made
        if call_number in self.texts and call_number not in self.failed_texts:
            text = self.texts[call_number]['text_file']
            for k, v in text.items():
                if k not in info2:
                    info1.append(k)
                    print('{k}: {v}'.format(k=k, v=v))
            print('------')
            for k, v in self.data.items():
                if k in info2 and k != 'cdl':
                    if k == 'transliteration':
                        print(('{k}: {v} lines available'.format(k=k, v=len(text['transliteration']))))
                    elif k != 'transliteration' and v == self.data['transliteration']:
                        pass
                        #print('{k}: {v}'.format(k=k, v='Not available'))
                    else:
                        print(('{k}: {v}'.format(k=k, v='available')))
            print()

    def print_single_text(self, call_number, catalog_filter=[]):
        """
        Prints and ingests only the one text.
        :param call_number: text you wish to print.
        :return:
        """
        if call_number in self.texts and call_number not in self.failed_texts:
            text = self.texts[call_number]['text_file']
            if len(catalog_filter) > 0:  # pylint: disable=len-as-condition
                if catalog_filter in text:
                    if catalog_filter == 'transliteration':
                        print('\n'.join([line for line in text[catalog_filter]]))
                    elif text[catalog_filter] == text['transliteration']:
                        print('Filter not available.')
                    else:
                        print('\n'.join([line for line in text[catalog_filter]]))
                else:
                    print('not a filter, use text_information for available filters.')
                    # make section that shows which filters are available (len > 0?)
            else:
                print('\n'.join([line for line in text['transliteration']]))
        else:
            print('Text does not exist in this corpus.')
