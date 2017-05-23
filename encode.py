#!/usr/bin/env python

import os
import argparse
import huffman

parser = argparse.ArgumentParser()
parser.add_argument('path', metavar='FILE_PATH')

if __name__ == '__main__':
    args = parser.parse_args()

    text_object = huffman.Huffman(args.path)
    text_object.encode()

    out_path = os.path.splitext(args.path)[0] + '.huf'

    print('compressed info stored in {}'.format(out_path))