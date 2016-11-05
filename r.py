#!/usr/bin/env python
""" rot13 utility to demonstrate architectural concepts  """

# required stdlib modules
import string
import sys
from argparse import ArgumentParser

# test-related modules
import errno
import unittest
from os import path, remove
from StringIO import StringIO


class Rot13:
    """ _ """

    ALPHABET_SIZE = len(string.lowercase)
    ROTATE_BY = ALPHABET_SIZE / 2

    # read input file in block of n bytes
    BLOCK_SIZE = 8

    def __init__(self, source, sink, slurp=False, silent=False):
        self.source = source
        self.sink = sink
        self.slurp = slurp
        self.silent = silent

    @classmethod
    def open(cls, file, mode='r'):
        """ IO wrapper per requirement """
        return open(file, mode)

    @classmethod
    def close(cls, file):
        """ IO wrapper per requirement """
        file.close()

    @classmethod
    def read(cls, file, size=BLOCK_SIZE):
        """ IO wrapper per requirement """
        while True:
            data = file.read(size)

            if data:
                yield data
            else:
                raise StopIteration

    @classmethod
    def write(cls, file, data):
        """ IO wrapper per requirement """
        file.write(data)

    @classmethod
    def translate(cls, chars):
        """ Ordinal Values | A - Z : 65 - 90 | a - z : 97 - 122 """

        translated = ''
        for char in chars:
            if not char.isalpha():
                translated += char
                continue

            # starting offset in ordinal table
            start = 'A' if char.isupper() else 'a'

            translated += chr(
                ord(start) + (
                    ord(char) - ord(start) + Rot13.ROTATE_BY
                ) % Rot13.ALPHABET_SIZE
            )

        return translated

    def rotate(self):
        """ _ """

        source = self.open(self.source, 'r')
        sink = self.open(self.sink, 'w')

        try:
            size = -1 if self.slurp else Rot13.BLOCK_SIZE

            for chars in self.read(source, size=size):
                translated = self.translate(chars)
                self.write(sink, translated)

                if not self.silent:
                    self.write(sys.stdout, translated)
        finally:
            self.close(sink)
            self.close(source)

        return


class Rot13UnitTest(unittest.TestCase):
    """ _ """

    def setUp(self):
        self.hex_file = StringIO()
        self.hex_file.write('0123456789abcdef')
        self.hex_file.seek(0)

    def tearDown(self):
        self.hex_file = None

    def test_lowercase(self):
        """ u.lowercase """

        expected = 'nopqrstuvwxyzabcdefghijklm'
        actual = Rot13.translate(string.lowercase)

        self.assertEqual(expected, actual)

    def test_uppercase(self):
        """ u.uppercase """

        expected = 'NOPQRSTUVWXYZABCDEFGHIJKLM'
        actual = Rot13.translate(string.uppercase)

        self.assertEqual(expected, actual)

    def test_sentence(self):
        """ u.sentence """

        expected = 'Pnrfne Pvcure'  # 'Caesar Cipher'
        actual = Rot13.translate('Caesar Cipher')

        self.assertEqual(expected, actual)

    def test_digits(self):
        """ u.digits """

        expected = string.digits
        actual = Rot13.translate(string.digits)

        self.assertEqual(expected, actual)

    def test_punctuation(self):
        """ u.punctuation """

        expected = string.punctuation
        actual = Rot13.translate(string.punctuation)

        self.assertEqual(expected, actual)

    def test_whitespace(self):
        """ u.whitespace """

        expected = string.whitespace
        actual = Rot13.translate(string.whitespace)

        self.assertEqual(expected, actual)

    def test_printable(self):
        """ u.printable """

        expected = ("""0123456789"""
                    """nopqrstuvwxyzabcdefghijklm"""
                    """NOPQRSTUVWXYZABCDEFGHIJKLM"""
                    """!"#$%&\'()*+,-./:;<=>?@[\\]"""
                    """^_`{|}~ \t\n\r\x0b\x0c""")

        actual = Rot13.translate(string.printable)

        self.assertEqual(expected, actual)

    def test_slurp(self):
        """ u.slurp """

        expected = Rot13.BLOCK_SIZE * 2
        self.hex_file.seek(0)
        letters = Rot13.read(self.hex_file, -1).next()
        actual = len(letters)

        self.assertEqual(expected, actual)

    def test_block(self):
        """ u.block """

        expected = [Rot13.BLOCK_SIZE] * 2
        actual = []
        self.hex_file.seek(0)
        for letters in Rot13.read(self.hex_file, Rot13.BLOCK_SIZE):
            actual.append(len(letters))

        self.assertEqual(expected, actual)


class Rot13IntegrationTests(unittest.TestCase):
    """ _ """

    def setUp(self):
        self.source = 'source.txt'
        self.sink = 'sink.txt'

        with open(self.source, 'w') as source:
            source.write(string.lowercase)

        with open(self.sink, 'w') as sink:
            assert sink

    def tearDown(self):
        try:
            remove(self.source)
            remove(self.sink)
        except OSError as error:
            # suppress all errors except ENOENT
            # errno.ENOENT = no such file or directory
            if error.errno != errno.ENOENT:
                raise

    def test_source(self):
        """ i.source """

        expected = string.lowercase
        with open(self.source) as source:
            actual = source.read()

        self.assertEqual(expected, actual)

    def test_rot13(self):
        """ i.rot13 """

        expected = 'nopqrstuvwxyzabcdefghijklm'
        rot13 = Rot13(source=self.source, sink=self.sink)
        rot13.rotate()

        with open(self.sink) as sink:
            actual = sink.read()

        self.assertEqual(expected, actual)

    def test_sink(self):
        """ i.sink """

        expected = True
        actual = path.exists(self.sink)

        self.assertEqual(expected, actual)


def main():
    """ _ """

    description = 'rot13 command-line utility'
    parser = ArgumentParser(description=description)
    parser.add_argument('-i', '--input', dest='source', required=True)
    parser.add_argument('-o', '--output', dest='sink', required=True)
    parser.add_argument('-s', '--slurp', dest='slurp', action='store_true')
    parser.add_argument('-q', '--quiet', dest='silent', action='store_true')

    args = parser.parse_args()
    source, sink = args.source, args.sink
    slurp, silent = args.slurp, args.silent

    rot13 = Rot13(source=source, sink=sink, slurp=slurp, silent=silent)
    rot13.rotate()

    return 0


if __name__ == '__main__':
    retval = main()
    sys.exit(retval)
