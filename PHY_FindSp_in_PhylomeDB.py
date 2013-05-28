#!/usr/bin/python
import ete2
import sys

def main():
    global l_species
    #user = raw_input('User: ')
    #passwd = raw_input('Password: ')
    user = "phyAdmin"; passwd = "phyd20.admin"
    print "\n\n"
    p = ete2.PhylomeDB3Connector(user=user, passwd=passwd)
    p._trees = "tree"
    p._algs = "alg"
    p._phylomes = "phylome"
    p._phy_content = "phylome_content"
    d_species = p.get_species()

    for j in l_species:
        for i in d_species.keys():
          if d_species[i]["name"].find(j)!=-1: print "\n" + str(i) + " -- NAME: " + d_species[i]["name"] + " - TAXID: " + str(d_species[i]["taxid"]) + "\n   VERS: " + str(p.get_genomes_by_species(d_species[i]["taxid"]))
    print "\n"

def getStr_Msg():
    script_name = sys.argv[0]
    script_name = script_name[script_name.rfind("/") + 1:]
    str_msg = "\n\n  Usage: %s <specie_name>\n" % script_name
    return str_msg

if __name__ == "__main__":
    l_species = []
    if not len(sys.argv) > 1: print getStr_Msg(); exit()
    for i in range(1, len(sys.argv)): # COMMAND-LINE PARSER ...
        param = sys.argv[i]
        if (param[:1] == "-"):
            pass
        else:
             l_species.append(param)
    print l_species
    main()