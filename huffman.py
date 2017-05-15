#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
        self.alphabet = []
        self.freq = {}

    def prepare_string(self, text):
        self.bwt_string = bwt.bwt(text)
        alphabet = bwt.alphbt(self.bwt_string)
        self.mtf_string, alphabet, self.freq = mtf.encode(self.bwt_string, alphabet)
        self.alphabet = bwt.alphbt(self.bwt_string)

    def build_heap(self):
        for key, value in self.freq.iteritems():
            node = HuffmanNode(key, value)
            heapq.heappush(self.heap, node)

        while len(self.heap) > 1:
            node1 = heapq.heappop(self.heap)
            node2 = heapq.heappop(self.heap)

            parent = HuffmanNode(None, node1.freq + node2.freq, left=node1, right=node2)
            heapq.heappush(self.heap, parent)

    def _generate_codes(self, node, code):

        if not node:
            return

        if node.char != None:
            self.codes[node.char] = code
            self.reverse_mapping[code] = node.char
            return

        self._generate_codes(node.left, code + '0')
        self._generate_codes(node.right, code + '1')

    def generate_codes(self):
        node = heapq.heappop(self.heap)
        code = ''
        self._generate_codes(node, code)
        heapq.heappush(self.heap, node)

    def encode_text(self):
        encoded_text = ''
        for character in self.mtf_string:
            encoded_text += self.codes[character]

        padding = 8 - len(encoded_text) % 8

        print(padding)

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

        for i in xrange(0, len(encoded_text), 8):
            byte = encoded_text[i:i + 8]
            arr.append(int(byte, 2))
        return arr

    def encode(self):
        filename, ext = os.path.splitext(self.path)
        out_path = filename + '.huf'

        with open(self.path, 'r+') as input_file, open(out_path, 'wb') as output:
            text = input_file.read()
            text = text.rstrip()

            self.prepare_string(text)
            self.build_heap()
            self.generate_codes()

            arr = self.generate_byte_array()

            output.write(bytes(arr))


# Old useless stuff

def encode(string, occ):
    heap = [[count, [letter, '']] for letter, count in occ.iteritems()]
    heapq.heapify(heap)
    print(heap)
    while len(heap) > 1:
        lo = heapq.heappop(heap)
        hi = heapq.heappop(heap)

        for pair in lo[1:]:
            pair[1] = '0' + pair[1]

        for pair in hi[1:]:
            pair[1] = '1' + pair[1]
        heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])
    return sorted(heapq.heappop(heap)[1:], key=lambda p: (len(p[-1]), p))


def build_table(tree, occ):
    table = {}
    for n in tree:
        table[n[1]] = n[0]
    return table


def print_table(tree, occ):
    print("Symbol".ljust(10) + "Weight".ljust(10) + "Huffman Code")
    for p in tree:
        print(str(p[0]).ljust(10) + str(occ[p[0]]).ljust(10) + p[1])
