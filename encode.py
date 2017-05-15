#!/usr/bin/env python
import argparse
import bwt
import mtf
import huffman


parser = argparse.ArgumentParser()
parser.add_argument('orig_string', metavar='S')

if __name__ == '__main__':
	args = parser.parse_args()
	
	bwt_string = bwt.bwt(args.orig_string)
	bwt_alphabet = bwt.alphbt(bwt_string)

	mtf_string, mtf_alphabet, occ = mtf.encode(bwt_string, bwt_alphabet)

	bwt_alphabet = bwt.alphbt(bwt_string)

	huffman_tree = huffman.encode(mtf_string, occ)

	huffman_table = huffman.build_table(huffman_tree, occ)

	print(huffman_tree)

	print(huffman_table)

	print(mtf_string)