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
    global b_Orig_Header_Comments

    l_counter = 0
    len_file = 0

    OUTPUT_FILE_STR = ""
    w = open(proteome_file, "r"); len_file = len(w.readlines()); w.close()
    w = open(proteome_file, "r")
    l_counter = 0
    for l_orig in w.xreadlines():
        l_counter += 1
        l = l_orig.rstrip().lstrip()
        if l == "": continue;
        if l[:1] == ">":
            l_aux = l.split("|")
            header = ">"
            header += l_aux[2]
            header += "\t" + get_Gen_Id_case_001(genome_file, l_aux[2], "-PA", "-RA")
            header += "\t" + put_Comments(comments, b_Orig_Header_Comments, l)
            sys.stderr.write("  [%s/%s]  %s ...\r" % (str(l_counter), str(len_file),header))
            OUTPUT_FILE_STR += header + "\n"
        else:
            OUTPUT_FILE_STR += l + "\n"
    w.close()
    Write_FILE(OUTPUT_FILE_STR.rstrip(), output_file)

def Write_FILE(v_Stream, v_Filename):
    w = open(v_Filename, "w")
    w.write(v_Stream)
    w.close()

def get_Gen_Id_case_001(v_genome_file, v_prot_Id, v_suff_prot, v_suff_gen):
    if v_prot_Id.find(v_suff_prot) == -1: print "\n\n  Suffix \"%s\" not found in the Prot_ID %s of the header of proteome file!\n" % (v_suff_prot, v_prot_Id); exit()
    prot_id_aux = v_prot_Id[:v_prot_Id.find(v_suff_prot)]
    gen_id_aux = prot_id_aux + v_suff_gen
    w = open(v_genome_file, "rb")
    TMP_FILE = w.read()
    if not TMP_FILE.find(gen_id_aux) != -1:
        print "\n\n  WARNING: Proteine Id %s not match in genome file!\n" % (v_prot_Id)
        w.close()
        exit()
    else:
        w.close()
        return gen_id_aux

def put_Comments(v_Str_Comments, v_b_Orig_Comments, v_Str_Orig_Comments):
    if v_Str_Comments != "":
        return comments
    else:
        if (b_Orig_Header_Comments == True):
            return v_Str_Orig_Comments[1:]
        else:
            return ""

def getStr_Msg():
    return "\n\nUsage: PHY_Header_parser.py -i SCRIPT input_file\n"

def argparse_check(v_ArgParse_Check, v_String, v_b_Print = False, v_EXIT = False):
    if (repr(v_ArgParse_Check) == "None"):
        if (v_b_Print == True): print v_String
        if v_EXIT == True: exit()
    else:
        return True

if __name__ == "__main__":
    proteome_file = ""
    genome_file = ""
    comments = ""
    b_Orig_Header_Comments = True
    header = ""

    argparse_check(args.input_proteome, "\n  You must specify an input (-i) Proteome file\n", True, True)
    argparse_check(args.input_genome, "\n  You must specify an input (-g) Genome file\n", True, True)
    if not os.path.isfile(args.input_proteome): print "\n  You must specify a CORRECT input (-i) Proteome file\n"; exit()
    if not os.path.isfile(args.input_genome): print "\n  You must specify a CORRECT input (-g) Genome file\n"; exit()
    proteome_file = args.input_proteome
    genome_file = args.input_genome
    if not (repr(args.comments) == "None"): comments= args.comments; b_Orig_Header_Comments = False
    output_file = proteome_file + ".db"
    main()