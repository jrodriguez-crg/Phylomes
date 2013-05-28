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
parser.add_argument("-b", "--blast_input", help="Blas file Proteome vs genome (RNA)")
parser.add_argument("-o1", "--parsed_proteome_file", help="Output Proteome parsed file (Fasta format)")
parser.add_argument("-o2", "--parsed_transcriptome_file", help="Output Transcriptome (RNA) parsed file (Fasta format)")
args = parser.parse_args()

def main():
    global proteome_file
    global genome_file
    global blast_file
    global parsed_proteome_file
    global parsed_transcriptome_file
    #print proteome_file; print genome_file; print blast_file; print parsed_proteome_file; print parsed_transcriptome_file

    counter = 0
    v_prot_header = ""
    v_rna_header = ""

    v_prot_id = ""
    v_gen_id = ""

    l_prot_ids = []
    l_gen_ids = []

    STR_FILE = ""

    #w = open(blast_file, "r")
    w = open(proteome_file, "r")
    for l in w.xreadlines():
        l_aux = l.rstrip().lstrip()
        if l_aux == "": continue;
        if l_aux[:1] == ">":
            l_aux = l_aux.split("\t")
            l_aux2 = l_aux[0].split("|")
            v_prot_id = l_aux2[3]
            v_gen_id = l_aux2[1]
            v_header = ">%s\t%s\t%s" % (v_prot_id, v_gen_id, l.rstrip().lstrip()[1:])
            if v_prot_id in l_prot_ids:
                print "\n\n  WARNING: Protein %s duplicated!\n" % (v_prot_id)
                exit()
            else:
                l_prot_ids.append(v_prot_id)
            if v_gen_id in l_gen_ids:
                print "\n\n  WARNING: Protein %s duplicated!\n" % (v_gen_id)
                exit()
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

def Get_BLAST_dict_case20130522(v_blast_file):
    v_BLAST_dict = {}
    l_Prots_Warnings = []
    w = open(v_blast_file, "r")
    for l in w.xreadlines():
        l_aux = l.split("\t")
        l_aux2 = l_aux[0].split("|")
        v_prot_id = l_aux2[3]
        v_gen_id = l_aux2[1]
        #if
        v_BLAST_dict[v_prot_id] = v_gen_id
        counter += 1
        if counter >= 15: break;
    w.close()
    return v_BLAST_dict


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
    return "\n\nUsage: PHY_Header_parser.py -i SCRIPT input_file\n"

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
    blast_file = ""
    parsed_proteome_file = ""
    parsed_transcriptome_file = ""

    argparse_check(args.input_proteome, "\n  You must specify an input (-i) Proteome file\n", True, True)
    argparse_check(args.input_genome, "\n  You must specify an input (-g) Genome file\n", True, True)
    argparse_check(args.blast_input, "\n  You must specify an input blast (-b) file\n", True, True)
    argparse_check(args.parsed_proteome_file, "\n  You must specify an output (-o1) name for parsed proteome file\n", True, True)
    argparse_check(args.parsed_transcriptome_file, "\n  You must specify an output (-o2) name for parsed transcriptome file\n", True, True)

    if not os.path.isfile(args.input_proteome): print "\n  You must specify a CORRECT input (-i) Proteome file\n"; exit()
    if not os.path.isfile(args.input_genome): print "\n  You must specify a CORRECT input (-g) Genome file\n"; exit()
    if not os.path.isfile(args.blast_input): print "\n  You must specify a CORRECT input Blast (-b) file\n"; exit()
    proteome_file = args.input_proteome
    genome_file = args.input_genome
    blast_file = args.blast_input

    parsed_proteome_file = args.parsed_proteome_file
    parsed_transcriptome_file = args.parsed_transcriptome_file

    main()