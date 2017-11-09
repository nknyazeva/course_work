import os, re
from collections import Counter

direct = "/Users/anastasia/PycharmProjects/course_work/testData/"
in_file = "/Users/anastasia/PycharmProjects/course_work/files_with_stop_codon.txt"
out_fileCodon = "/Users/anastasia/PycharmProjects/course_work/testCodon_one.txt"
out_fileGene = "/Users/anastasia/PycharmProjects/course_work/testGene_one.txt"

global gene_catalog
gene_catalog = []


class Gene:
    def __init__(self, name_file, id, orf_start, orf_stop, stop_codon):
        self.name_file = name_file
        self.id = id
        self.orf_start = orf_start
        self.orf_stop = orf_stop
        self.stop_codon = stop_codon


def parse_string(file_current, file):
    for line in range(197):
        get_meta(file_current, file)

def get_meta(file_current, file):
    data = file_current.readline()
    name_file = file
    id = re.search(r'>\w+', data).group(0)
    orf_start = int(re.search(r'(\d+)\s(\d+)\n', data).group(1))
    orf_stop = int(re.search(r'(\d+)\n', data).group(1))
    stop_codon = {}
    gene = Gene(name_file, id, orf_start, orf_stop, stop_codon)
    get_seq(file_current, gene)


def get_seq(file_current, gene):
    seq = file_current.readline().strip()[:-3]
    dict_coordinates = coordinate_determination(seq, gene)
    search_codon(seq, gene, dict_coordinates)


def coordinate_determination(seq, gene):
    dict_coordinates = {}
    coord = gene.orf_start
    for i in range(len(seq)):
        dict_coordinates[i] = coord
        coord = coord + 1
    return dict_coordinates


def search_codon (seq, gene, dict_coordinates):
    dict_stopCodon = {}

    for codon in range(0, len(seq), 3):
        current_codon = seq[codon:codon + 3]
        if current_codon == 'TAA' or current_codon == 'TAG' or current_codon == 'TGA':
            dict_stopCodon[dict_coordinates[codon]] = current_codon
    gene.stop_codon = dict_stopCodon
    gene_catalog.append(gene)


def threshold_check (gene_catalog):

    dict_file_stopCodon = {}
    for gene in gene_catalog:
        if gene.name_file in dict_file_stopCodon.keys():
            dict_file_stopCodon[gene.name_file].append(gene.stop_codon)
        else:
            dict_file_stopCodon[gene.name_file] = []
            dict_file_stopCodon[gene.name_file].append(gene.stop_codon)
    dict_write_stop_coordinate = {}
    for file in dict_file_stopCodon.keys():
        list_coordinateStop = []
        for g in dict_file_stopCodon[file]:
            for key in g.keys():
                list_coordinateStop.append(key)

        counter = Counter(list_coordinateStop)
        sort_list_coordinateStop = []
        for i in counter:
            if counter[i] <= 197 * 0.3:
                sort_list_coordinateStop.append([i, counter[i]])
        dict_write_stop_coordinate[file] = sort_list_coordinateStop

    return dict_write_stop_coordinate

def write_stop_coordinate (dict_coordinate, file):
    file_coordStop = open(file, "w")
    for key in dict_coordinate.keys():
        for i in dict_coordinate[key]:
            file_coordStop.write(str(key) + "\t" + str(i[0]) + "\t" + str(i[1]) + "\n")
    file_coordStop.close()

def write_gene (gene_catalog, out_fileGene):
    file_gene = open(out_fileGene, "w")
    for gene in gene_catalog:
        file_gene.write(str(gene.name_file) + "\t" + str(gene.id) + "\t" + str(gene.orf_start) + "\t" + str(gene.orf_stop) + "\t" + str(gene.stop_codon) + "\n")
    file_gene.close()


files_name = open(in_file, "r")


for line in files_name:
    file = line.strip()
    if "one" in file:
        file_current = open(os.path.join(direct, file), "r")
        parse_string(file_current, file)
        file_current.close()

files_name.close()
dict_write = threshold_check(gene_catalog)
write_stop_coordinate (dict_write, out_fileCodon)
write_gene(gene_catalog, out_fileGene)