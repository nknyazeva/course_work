import os, re

direct = "/mnt/lustre/potapova/200_flies/all_genes/"
in_file = "/mnt/lustre/nknyazeva/courseWork4/repository/output/files_with_stop_codon.txt"
out_file_gene = "/mnt/lustre/nknyazeva/courseWork4/repository/output/all_genes_with_stop.txt"
out_file_gene_threshold = "/mnt/lustre/nknyazeva/courseWork4/repository/output/threshold_genes_with_stop"
out_file_gene_threshold_no = "/mnt/lustre/nknyazeva/courseWork4/repository/output/no_threshold_genes_with_stop"


# direct = "/Users/anastasia/PycharmProjects/course_work/testData/"
# in_file = "/Users/anastasia/PycharmProjects/course_work/files_with_stop_codon.txt"
# out_file_gene = "/Users/anastasia/PycharmProjects/course_work/all_genes_with_stop.txt"
# out_file_gene_threshold = "/Users/anastasia/PycharmProjects/course_work/threshold_genes_with_stop"
# out_file_gene_threshold_no = "/Users/anastasia/PycharmProjects/course_work/no_threshold_genes_with_stop"


global gene_catalog
gene_catalog = []

global number_individual
number_individual = float(197)

list_threshold = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5]


class Gene:
    def __init__(self, name_file, id, exons, orf_start, orf_stop, stop_codon, frequency_stop):
        self.name_file = name_file
        self.id = id
        self.exons = exons
        self.orf_start = orf_start
        self.orf_stop = orf_stop
        self.stop_codon = stop_codon
        self.frequency_stop = frequency_stop


def parse_string(file_current, file):
    for line in range(int(number_individual)):
        get_meta(file_current, file)

def get_meta(file_current, file):
    data = file_current.readline()
    name_file = file
    id = re.search(r'>\w+', data).group(0)
    if "[" in data:
        exons = eval(re.search(r'\[.*\]', data).group(0))
    else:
        exons = []
    orf_start = int(re.search(r'(\d+)\s(\d+)\n', data).group(1))
    orf_stop = int(re.search(r'(\d+)\s(\d+)\n', data).group(2))
    stop_codon = {}
    frequency_stop = 0
    gene = Gene(name_file, id, exons, orf_start, orf_stop, stop_codon, frequency_stop)
    get_seq(file_current, gene)


def get_seq(file_current, gene):
    seq = file_current.readline().strip()[:-3]
    dict_coordinates = coordinate_determination(seq, gene)
    search_codon(seq, gene, dict_coordinates)


def coordinate_determination(seq, gene):
    dict_coordinates = {}
    coord = gene.orf_start
    if gene.exons == []:
        for i in range(len(seq)):
            dict_coordinates[i] = coord
            coord = coord + 1
    else:
        exon_index = 0
        for i in range(len(seq)):
            if coord > gene.exons[exon_index][1] - 1:
                exon_index = exon_index + 1
                if coord < gene.exons[exon_index][0]:
                    coord = gene.exons[exon_index][0]
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


def frequency_stop_codon (gene_catalog):
    dict_file_gene = {}
    for gene in gene_catalog:
        if gene.name_file in dict_file_gene.keys():
            dict_file_gene[gene.name_file].append(gene)
        else:
            dict_file_gene[gene.name_file] = []
            dict_file_gene[gene.name_file].append(gene)
    for file in dict_file_gene.keys():
        index = 0
        for gene in dict_file_gene[file]:
            if gene.stop_codon != {}:
                index = index + 1
        for gene in dict_file_gene[file]:
            gene.frequency_stop = float(index) / number_individual


def write_gene(gene_catalog, out_fileGene):
    file_gene = open(out_fileGene, "w")
    for gene in gene_catalog:
        file_gene.write(str(gene.name_file) + "\t" + str(gene.id) + "\t" + str(gene.exons) + "\t" + str(gene.orf_start) + "\t" + str(gene.orf_stop) + "\t" + str(gene.stop_codon) + "\t" + str(gene.frequency_stop) + "\n")
    file_gene.close()


def write_gene_threshold(gene, file):
    file.write(str(gene.name_file) + "\t" + str(gene.id) + "\t" + str(gene.exons) + "\t" + str(gene.orf_start) + "\t" + str(gene.orf_stop) + "\t" + str(gene.stop_codon) + "\t" + str(gene.frequency_stop) + "\n")


files_name = open(in_file, "r")
for line in files_name:
    file = line.strip()
    file_current = open(os.path.join(direct, file), "r")
    parse_string(file_current, file)
    file_current.close()
files_name.close()

frequency_stop_codon(gene_catalog)
write_gene(gene_catalog, out_file_gene)

for threshold in list_threshold:
    file_gene_threshold = open('_'.join([out_file_gene_threshold, str(threshold)]), "w")
    file_gene_threshold_no = open('_'.join([out_file_gene_threshold_no, str(threshold)]), "w")
    for gene in gene_catalog:
        if gene.frequency_stop <= threshold:
            write_gene_threshold(gene, file_gene_threshold)
        else:
            file_gene_threshold_no.write(gene.name_file + "\n")

    file_gene_threshold_no.close()
    file_gene_threshold.close()