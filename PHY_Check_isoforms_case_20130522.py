#!/usr/bin/python

import sys
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input_proteome", help="Input Proteome File (Fasta format)")
parser.add_argument("-g", "--input_genome", help="Input Genome File (Fasta format)")
parser.add_argument("-o", "--output_file", help="Oputput parsed file (Fasta format)")
parser.add_argument("-c", "--comments", help="Oputput parsed file (Fasta format)")
args = parser.parse_args()

def main():
    global proteome_file
    global genome_file
    global output_file
    global header
    pass


def Write_FILE(v_Stream, v_Filename):
    w = open(v_Filename, "w")
    w.write(v_Stream)
    w.close()

def getStr_Msg():
    return "\n\nUsage: PHY_Header_parser.py -i SCRIPT input_file\n"

def argparse_check(v_ArgParse_Check, v_String, v_b_Print = False, v_EXIT = False):
    if (repr(v_ArgParse_Check) == "None"):
        if (v_b_Print == True): print v_String
        if v_EXIT == True: exit()
    else:
        return True

if __name__ == "__main__":
    input_file = ""
    proteome_file = ""
    comments = ""
    header = ""
    argparse_check(args.input_proteome, "\n  You must specify an input (-i) Proteome file\n", True, True)
    argparse_check(args.input_genome, "\n  You must specify an input (-g) Genome file\n", True, True)
    if not os.path.isfile(args.input_proteome): print "\n  You must specify a CORRECT input (-i) Proteome file\n"; exit()
    if not os.path.isfile(args.input_genome): print "\n  You must specify a CORRECT input (-g) Genome file\n"; exit()
    input_file = args.input_genome
    proteome_file = args.input_proteome
    if not (repr(args.comments) == "None"): comments= args.comments
    output_file = input_file + ".db"
    main()