"""
This file tests methods in file_import.py.
"""

import unittest
import os
import pytest

from oracc_importer import ORACCUnzip  # pylint: disable =import-error
from oracc_importer import FileImport  # pylint: disable =import-error

__author__ = ['Andrew Deloucas <ADeloucas@g.harvard.com>']
__license__ = 'MIT License. See LICENSE.'


class Test1(unittest.TestCase):  # pylint: disable=R0904
    """
    Tests ORACCUnzip class.
    """
    def test_unzip(self):
        """
        Tests read_file.
        """
        parent_directory = os.path.expanduser('~')
        folder = os.path.join(parent_directory, 'Python', 'cltk', 'cltk', 'tests', 'test_akkadian')
        destination = os.path.join(parent_directory)
        f_i = ORACCUnzip(folder, destination)
        f_i.unzip()
        testfolder = os.path.join(destination, 'ORACC-Files')
        final = os.listdir(testfolder)
        goal = ['aemw', 'armep', 'arrim', 'blms', 'cams', 'ccpo', 'ckst',
                'cmawro', 'contrib', 'ctij', 'dcclt', 'dccmt', 'etcsri',
                'glass', 'hbtin', 'lacost', 'nimrud', 'obmc', 'obta',
                'ogsl', 'oimea', 'ORACC-Test-Text-1', 'ORACC-Test-Text-2',
                'qcat', 'riao', 'ribo', 'rimanum', 'rinap', 'saao', 'suhu', 'xcat']
        self.assertEqual(final, goal)

class Test2(unittest.TestCase):  # pylint: disable=R0904
    """
    # Tests FileImport class.
    """
    def test_read_catalogue(self):
        """
        # Tests read_file.
        """
        parent_directory = os.path.expanduser('~')
        test_text = os.path.join(parent_directory, \
                                 'ORACC-Files', 'ORACC-Test-Text-1', 'catalogue.json')
        r_c = FileImport(test_text)
        r_c.read_catalogue()
        final = r_c.message
        goal = 'Catalogue is ready.'
        self.assertEqual(final, goal)

    def test_load_corpus(self):
        """
        # Tests file_catalog.
        """
        parent_directory = os.path.expanduser('~')
        test_text = os.path.join(parent_directory, \
                                 'ORACC-Files', 'ORACC-Test-Text-1', 'catalogue.json')
        r_c = FileImport(test_text)
        r_c.load_corpus()
        final = len(r_c.catalog)
        goal = 20
        self.assertEqual(final, goal)

    @pytest.fixture(autouse=True)
    def _pass_fixtures(self, capsys):
        self.capsys = capsys  # pylint: disable=attribute-defined-outside-init

    def test_print_catalogue(self):
        """
        # Tests file_catalog.
        """

        parent_directory = os.path.expanduser('~')
        test_text = os.path.join(parent_directory, \
                                 'ORACC-Files', 'ORACC-Test-Text-1', 'catalogue.json')
        r_c = FileImport(test_text)
        r_c.read_catalogue()
        r_c.print_catalogue()
        captured = self.capsys.readouterr()
        goal = \
"""Catalogue is ready.
Catalogue of Texts:

         Publication Name     Call Number
       -------------------------------
     1.| X123456              X123456   
"""
        self.assertEqual(captured.out, goal)


if __name__ == '__main__':
    unittest.main()
