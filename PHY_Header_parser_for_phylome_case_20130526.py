#!/usr/bin/python

# Sacado de RNA-Seq, parsear el proteoma Y el GENOMA rna.fa
# haciendo un BLAST primero para saber cual proteina concuerda con cual gen
#
# PROTEOME:
# ><ID_Prot> __\t__ <ID_Gen> __\t__ <HEADER ORIGINAL COMPLETO>
#
# TRANSCRIPTOME (rna.fa):
# ><ID_Prot> __\t__ <ID_Gen> __\t__ <HEADER ORIGINAL COMPLETO>
#
#

import sys
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input_proteome", help="Input Proteome File (Fasta format)")
parser.add_argument("-g", "--input_genome", help="Input Genome File (Fasta format)")
parser.add_argument("-l", "--gff_input", help="Gff file ((-l) link)")
parser.add_argument("-o1", "--output_proteome_file", help="Output Proteome parsed file (Fasta format)")
parser.add_argument("-o2", "--output_genome_file", help="Output Genome parsed (CDS) file (Fasta format)")

args = parser.parse_args()

def main():
    global proteome_file
    global genome_file
    global gff_file
    global parsed_proteome_file
    #print proteome_file; print genome_file; print blast_file; print parsed_proteome_file; print parsed_transcriptome_file

    len_proteome = 0
    zf_counter = 0

    w = open(proteome_file, "r"); len_proteome = w.read().count(">"); w.close()
    zf_counter = len(str(len_proteome))

    counter = 0
    v_prot_header = ""
    v_rna_header = ""

    v_prot_id = ""
    v_gen_id = ""

    l_prot_ids = []
    l_gen_ids = []

    STR_FILE = ""

    w = open(genome_file, "r"); v_GENOME_FILE = w.read(); w.close()
    l_GENOME_FILE = v_GENOME_FILE.split("\n")

    w = open(gff_file, "r"); v_GFF_FILE = w.read(); w.close()
    l_GFF_FILE = v_GFF_FILE.split("\n")


    w = open(proteome_file, "r")
    for l in w.xreadlines():
        l_aux = l.rstrip().lstrip()
        if l_aux == "": continue;
        if l_aux[:1] == ">":
            v_prot_id = l_aux[1:]
            v_gen_id = get_Gen_Id_case_20130526(v_prot_id, l_GFF_FILE, l_GENOME_FILE)
            sys.stderr.write("  %s / %s - %s\r" % (str(counter).zfill(zf_counter), len_proteome, v_gen_id))
            v_header = ">%s\t%s\t%s" % (v_prot_id, v_gen_id, "")
            if v_prot_id in l_prot_ids:
                print "\n\n  WARNING: Protein %s duplicated!\n" % (v_prot_id)
                exit()
            else:
                l_prot_ids.append(v_prot_id)

            if v_gen_id in l_gen_ids:
                print "\n\n  WARNING: Gen %s duplicated! (ID_Prot: %s)\n" % (v_gen_id, v_prot_id)
                #exit()
            else:
                l_gen_ids.append(v_gen_id)
            #print v_header
            STR_FILE += v_header + "\n"
            counter += 1
            #if counter >= 15: break;
        else:
            STR_FILE += l
    w.close()
    Write_FILE(STR_FILE, parsed_proteome_file)

def get_Gen_Id_case_20130526(v_prot_id, v_l_GFF_FILE, v_l_GENOME_FILE):
    v_l_aux = ""
    v_gen_id = ""
    for l in v_l_GFF_FILE:
        if (l.find(v_prot_id) != -1):
            v_l_aux = l.split("\t")[0].rstrip().lstrip()
            if v_gen_id == "": v_gen_id = v_l_aux
            if v_gen_id != v_l_aux: print "ERROR! %s" % v_gen_id; exit()
    return v_gen_id

def Write_FILE(v_Stream, v_Filename):
    w = open(v_Filename, "w")
    w.write(v_Stream)
    w.close()

def get_Gen_Id_case_004(v_GENOME_FILE, v_prot_Id, v_d_suff):
    b_Found = False
    v_suff_prot = ""
    v_suff_gen = []

    for i in v_d_suff:
        if v_prot_Id.find(i) != -1:
            b_Found = True;
            v_suff_prot = i;
            v_suff_gen.append(v_d_suff[i])
    if (b_Found == False):
        print "\n\n  Suffix \"%s\" not found in the Prot_ID %s of the header of proteome file!\n" % (v_suff_prot, v_prot_Id);
        exit()

    prot_id_aux = v_prot_Id[:v_prot_Id.find(v_suff_prot)]
    #gen_id_aux = prot_id_aux + v_suff_gen
    #w = open(v_genome_file, "rb")
    #TMP_FILE = w.read()
    b_Found = False
    TMP_FILE = v_GENOME_FILE
    for k in v_suff_gen:
        if TMP_FILE.find(k) != -1:
            gen_id_aux = prot_id_aux + k
            b_Found = True

    #if not TMP_FILE.find(gen_id_aux) != -1:
    if not (b_Found == True):
        print "\n\n  WARNING: Proteine Id %s not match in genome file!\n" % (v_prot_Id)
        #w.close()
        exit()
    else:
        #w.close()
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
    return "\n\nUsage: PHY_Header_parser.py -i Proteome_File -g Genome_File -l GFF_File\n"

def argparse_check(v_ArgParse_Check, v_String, v_b_Print = False, v_EXIT = False):
    if (repr(v_ArgParse_Check) == "None"):
        if (v_b_Print == True): print v_String
        if v_EXIT == True: exit()
    else:
        return True

def main_old_bak():
    l_counter = 0
    len_file = 0

    w = open(genome_file, "r")
    GENOME_FILE = w.read()
    w.close()

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
            #header += "\t" + get_Gen_Id_case_002(genome_file, l_aux[2], d_suff)
            if l_aux[2] in d_exceptions.keys():
                header += "\t" + d_exceptions[l_aux[2]]
            else:
                header += "\t" + get_Gen_Id_case_004(GENOME_FILE, l_aux[2], d_suff)
            header += "\t" + put_Comments(comments, b_Orig_Header_Comments, l)
            sys.stderr.write("  [%s/%s]  %s ...\r" % (str(l_counter), str(len_file),header))
            OUTPUT_FILE_STR += header + "\n"
        else:
            OUTPUT_FILE_STR += l + "\n"
    w.close()
    Write_FILE(OUTPUT_FILE_STR.rstrip(), output_file)



if __name__ == "__main__":
    proteome_file = ""
    genome_file = ""
    gff_file = ""
    parsed_proteome_file = ""
    parsed_genome_file = ""

    argparse_check(args.input_proteome, "\n  You must specify an input (-i) Proteome file\n", True, True)
    argparse_check(args.input_genome, "\n  You must specify an input (-g) Genome file\n", True, True)
    argparse_check(args.gff_input, "\n  You must specify an input gff input ((-l) link) file\n", True, True)
    argparse_check(args.output_proteome_file, "\n  You must specify an output (-o1) genome file\n", True, True)
    argparse_check(args.output_genome_file, "\n  You must specify an output (-o2) genome file\n", True, True)

    if not os.path.isfile(args.input_proteome): print "\n  You must specify a CORRECT input (-i) Proteome file\n"; exit()
    if not os.path.isfile(args.input_genome): print "\n  You must specify a CORRECT input (-g) Genome file\n"; exit()
    if not os.path.isfile(args.gff_input): print "\n  You must specify a CORRECT gff input ((-l) link) file\n"; exit()

    proteome_file = args.input_proteome
    genome_file = args.input_genome
    gff_file = args.gff_input
    parsed_proteome_file = args.output_proteome_file
    parsed_genome_file = args.output_genome_file

    main()

