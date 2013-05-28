#!/usr/bin/python

import sys
import os
import time
import argparse
import shutil

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input_origin", help="Input origin File")
parser.add_argument("-b", "--input_target", help="Input target ((-b) Blast)")
parser.add_argument("-o", "--output_dir", help="Output file to print")
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("-pg", "--proteins_to_genes", help="Proteins to genes", action="store_true")
group.add_argument("-pp", "--proteins_to_proteins", help="Proteins to proteins", action="store_true")
group.add_argument("-gp", "--genes_to_proteins", help="Genes to proteins", action="store_true")
group.add_argument("-gg", "--genes_to_genes", help="Genes to genes", action="store_true")
args = parser.parse_args()

def main():
    global orig_input_file
    global orig_blast_file
    global target_input_file
    global target_blast_file
    global output_dir
    os.chdir(output_dir)
    shutil.copy(orig_input_file, output_dir)
    shutil.copy(orig_blast_file, output_dir)
    if args.proteins_to_genes == True:
        comm_exec = "formatdb -V -o -p F -i %s" % (target_blast_file)
        os.system(comm_exec)
        comm_exec = "blastall -p \"tblastn\" -i %s -d %s -m 8 -b 20 -o output.blast" % (target_input_file, target_blast_file)
        os.system(comm_exec)
    elif args.proteins_to_proteins == True:
        comm_exec = "formatdb -V -o -p T -i %s" % (target_blast_file)
        os.system(comm_exec)
        comm_exec = "blastall -p \"blastp\" -i %s -d %s -m 8 -b 20 -o output.blast" % (target_input_file, target_blast_file)
        os.system(comm_exec)
    elif args.genes_to_proteins == True:
        comm_exec = "formatdb -V -o -p T -i %s" % (target_blast_file)
        os.system(comm_exec)
        comm_exec = "blastall -p \"blastx\" -i %s -d %s -m 8 -b 20 -o output.blast" % (target_input_file, target_blast_file)
        os.system(comm_exec)
    elif args.genes_to_genes == True:
        comm_exec = "formatdb -V -o -p F -i %s" % (target_blast_file)
        os.system(comm_exec)
        comm_exec = "blastall -p \"blastn\" -i %s -d %s -m 8 -b 20 -o output.blast" % (target_input_file, target_blast_file)
        os.system(comm_exec)

def create_dir(f):
    d = os.path.dirname(f)
    if not os.path.exists(d) :
        os.makedirs(d)

def getStr_Msg():
    return "\n\nUsage: SCRIPT.py -i SCRIPT -b input_file\n"

def argparse_check(v_ArgParse_Check, v_String, v_b_Print = False, v_EXIT = False):
    if (repr(v_ArgParse_Check) == "None"):
        if (v_b_Print == True): print v_String
        if v_EXIT == True: exit()
    else:
        return True

if __name__ == "__main__":
    orig_input_file = ""
    orig_blast_file = ""
    target_blast_file = ""
    target_input_file = ""
    output_dir = ""
    orig_dir = ""
    blast_typel = ""

    argparse_check(args.input_origin, "\n  You must specify an input (-i) Proteome file\n", True, True)
    argparse_check(args.input_target, "\n  You must specify an input (-b) Genome file\n", True, True)
    if not os.path.isfile(args.input_origin): print "\n  You must specify a CORRECT input (-i) file\n"; exit()
    if not os.path.isfile(args.input_target): print "\n  You must specify a CORRECT input (-g) target (Blast) file\n"; exit()
    orig_input_file = args.input_origin
    orig_blast_file = args.input_target
    orig_dir = os.getcwd();
    if orig_dir[:-1] != "/": orig_dir += "/"
    output_dir = orig_dir
    if (repr(args.output_dir) != "None"):
        output_dir += args.output_dir; create_dir(output_dir)
    else:
        output_dir += "_BLAST_" + str(time.gmtime().tm_year).zfill(4) + "_" + str(time.gmtime().tm_mon).zfill(2) + "_" + str(time.gmtime().tm_mday).zfill(2) + "_" + str(time.gmtime().tm_hour + 2).zfill(2) + str(time.gmtime().tm_min).zfill(2) + "/"
        create_dir(output_dir)
    target_input_file = output_dir + orig_input_file
    target_blast_file = output_dir + orig_blast_file
    if os.path.dirname(orig_blast_file) == "": orig_blast_file = orig_dir + orig_blast_file
    if os.path.dirname(orig_input_file) == "": orig_input_file = orig_dir + orig_input_file
    main()


