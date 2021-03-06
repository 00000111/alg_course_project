#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import os
import heapq
import bwt
import mtf


class HuffmanNode(object):
    def __init__(self, char, freq, left=None, right=None, root=None):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right
        self.root = root

    def __lt__(self, other):
        if other and isinstance(other, HuffmanNode):
            return self.freq < other.freq
        return -1

    def __le__(self, other):
        if other and isinstance(other, HuffmanNode):
            return self.freq <= other.freq
        return -1

    def __gt__(self, other):
        if other and isinstance(other, HuffmanNode):
            return self.freq > other.freq
        return -1

    def __ge__(self, other):
        if other and isinstance(other, HuffmanNode):
            return self.freq >= other.freq
        return -1

    def __eq__(self, other):
        if other and isinstance(other, HuffmanNode):
            return self.freq == other.freq
        return -1

    def __ne__(self, other):
        return not self.__eq__(other)

    def children(self):
        return self.left, self.right


class Huffman(object):

    def __init__(self, path):
        self.path = path
        self.heap = []
        self.codes = {}
        self.reverse_mapping = {}
        self.bwt_string = ''
        self.mtf_string = ''
        # self.rle_string = []
        self.alphabet = []
        self.freq = {}
        self._original_string = None
        self._compressed_string = None
        self._compressed_unpadded_string = None

    @property
    def compressed_string(self):
        if self._compressed_string:
            string = ''
            for byte in self._compressed_string:
                bits = bin(byte)[2:]
                string += bits
            return string
        return None

    def prepare_string(self, text):
        self.bwt_string = bwt.encode(text)
        alphabet = bwt.alphabet(self.bwt_string)
        self.mtf_string, self.freq = mtf.encode(self.bwt_string, alphabet)
        self.alphabet = bwt.alphabet(self.bwt_string)

    def build_heap(self):
        for char, frequency in self.freq.iteritems():
            heapq.heappush(self.heap, HuffmanNode(char, frequency))

        while len(self.heap) > 1:
            node1 = heapq.heappop(self.heap)
            node2 = heapq.heappop(self.heap)

            parent = HuffmanNode(None, node1.freq + node2.freq, left=node1, right=node2)
            heapq.heappush(self.heap, parent)

    def _generate_codes(self, node, code):

        if not node:
            return

        if node.char is not None:
            self.codes[node.char] = code
            self.reverse_mapping[code] = node.char
            return

        self._generate_codes(node.left, code + '0')
        self._generate_codes(node.right, code + '1')

    def generate_codes(self):
        root = heapq.heappop(self.heap)
        code = ''
        self._generate_codes(root, code)
        heapq.heappush(self.heap, root)

    def encode_text(self):
        encoded_text = ''
        for character in self.mtf_string:
            encoded_text += self.codes[character]

        self._compressed_unpadded_string = encoded_text

        padding = 8 - len(encoded_text) % 8

        encoded_text += '0' * padding

        padding_info = "{0:08b}".format(padding)
        encoded_text = padding_info + encoded_text
        return encoded_text

    def generate_byte_array(self):
        encoded_text = self.encode_text()
        if len(encoded_text) % 8 != 0:
            print('Incorrect padding')
            return -1

        arr = bytearray()

        # TODO: Optimize this

        for i in xrange(0, len(encoded_text), 8):
            byte = encoded_text[i:i + 8]
            arr.append(int(byte, 2))
        return arr

    def encode(self):
        start = time.time()
        filename, ext = os.path.splitext(self.path)
        out_path = filename + '.huf'

        with open(self.path, 'r+') as input_file, open(out_path, 'wb') as output:
            text = input_file.read()
            text = text.rstrip()

            self._original_string = text

            preparation_start = time.time()
            self.prepare_string(text)
            preparation_end = time.time()
            heap_build_start = time.time()
            self.build_heap()
            heap_build_end = time.time()
            code_generation_start = time.time()
            self.generate_codes()
            code_generation_end = time.time()

            compression_start = time.time()

            arr = self.generate_byte_array()

            compression_end = time.time()

            payload_generation_start = time.time()
            reverse_mapping_string = ''
            for key, value in self.reverse_mapping.items():
                reverse_mapping_string += '{k} {v},'.format(k=key, v=value)

            alphabet_string = ' '.join((str(ord(x)) for x in self.alphabet))
            print(alphabet_string)

            payload_generation_end = time.time()
            self._compressed_string = arr

            file_write_start = time.time()
            output.write(reverse_mapping_string + '\n')
            output.write(alphabet_string + '\n')
            output.write(bytes(arr))
            file_write_end = time.time()

        end = time.time()

        print('Prepared (transformed) at {}'.format(preparation_end - preparation_start))
        print('Huffman Heap build at {}'.format(heap_build_end - heap_build_start))
        print('Huffman codes generated at {}'.format(code_generation_end - code_generation_start))
        print('Payload generated at {}'.format(payload_generation_end - payload_generation_start))
        print('Compressed at {}'.format(compression_end - compression_start))
        print('Writed to file in {}'.format(file_write_end - file_write_start))

        print('Total time {}'.format(end - start))


def extract_encoded_data(path):
    with open(path, 'rb+') as in_file:
        codes = {}
        raw_codes = in_file.readline().split(',')
        for code in raw_codes:
            if code != '\n':
                code = code.split()
                codes[code[0]] = int(code[1])


        # extract alphabet

        int_alphabet = in_file.readline().split()
        alphabet = []
        for i in xrange(len(int_alphabet)):
            if int_alphabet != '\n':
                alphabet.append(chr(int(int_alphabet[i])))

        # read coded string

        coded_string = ''
        byte = in_file.read(1)
        while byte:
            byte = ord(byte)
            bits = bin(byte)[2:].rjust(8, '0')
            coded_string += bits
            byte = in_file.read(1)

    return codes, alphabet, coded_string


def decode_string(coded_string, codes):
    current_code = ''
    decoded_string = []
    for bit in coded_string:
        current_code += bit
        if current_code in codes.keys():
            decoded_string.append(codes[current_code])
            current_code = ''

    return decoded_string


def decode(path):
    filename, ext = os.path.splitext(path)
    codes, alphabet, coded_string = extract_encoded_data(path)


    #remove padding
    padding = int(coded_string[:8], 2)
    coded_string = coded_string[8:-1*padding]

    #decode
    decoded_string = decode_string(coded_string, codes)
    # decoded_string = rle.decode(decoded_string)
    decoded_string = mtf.decode(decoded_string, alphabet)
    decoded_string = bwt.decode(decoded_string, alphabet)
    return decoded_string

