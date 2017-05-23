#!/usr/bin/env python

import os
import argparse
import huffman

parser = argparse.ArgumentParser()
parser.add_argument('path', metavar='FILE_PATH')

if __name__ == '__main__':
    args = parser.parse_args()

    out_path = os.path.splitext(args.path)
    out_path = out_path[0]+'_decompressed.txt'
    decoded_text = huffman.decode(args.path)

    with open(out_path, 'w') as out:
        out.write(decoded_text)

    print('Uncompressed text stored in {}'.format(out_path))