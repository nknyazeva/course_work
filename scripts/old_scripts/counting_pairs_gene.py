import re
from itertools import combinations

in_file = "/Users/anastasia/PycharmProjects/course_work/testGene_threshold.txt"
out_file_frequency_codon = "/Users/anastasia/PycharmProjects/course_work/frequencyCodon_gene.txt"
out_file_frequency_codon_counting = "/Users/anastasia/PycharmProjects/course_work/frequencyCodon_gene_counting.txt"

# in_file = "/mnt/lustre/nknyazeva/courseWork4/scripts/output/gene_description_threshold.txt"
# out_file_frequency_codon = "/mnt/lustre/nknyazeva/courseWork4/scripts/output/description_pairs_gene.txt"
# out_file_frequency_codon_counting = "/mnt/lustre/nknyazeva/courseWork4/scripts/output/pairs_gene_counting.txt"

number_individual = float(197)
global gene_catalog
gene_catalog = []

global number_neighbors
number_neighbors = 3

global catalog_pairs_gene
catalog_pairs_gene = []

global counting_pairs_gene
counting_pairs_gene = {}

class Gene:
    def __init__(self, name_file, id, exons, orf_start, orf_stop, stop_codon, coordinate_stop, frequency_stop):
        self.name_file = name_file
        self.id = id
        self.exons = exons
        self.orf_start = orf_start
        self.orf_stop = orf_stop
        self.stop_codon = stop_codon
        self.coordinate_stop = coordinate_stop
        self.frequency_stop = frequency_stop

class NameFile:
    def __init__(self, name_file, chr, number):
        self.name_file = name_file
        self.chr = chr
        self.number = number

class ComparisonPairs:
    def __init__(self, name_file_first, name_file_second, id, stop_codon_first, stop_codon_second):
        self.name_file_first = name_file_first
        self.name_file_second = name_file_second
        self.id = id
        self.stop_codon_first = stop_codon_first
        self.stop_codon_second = stop_codon_second



def deserialization(line):
    name_file = re.search(r'\w+\.fasta', line).group(0)
    id = re.search(r'>\w+', line).group(0)
    exons = eval(re.search(r'\[.*\]', line).group(0))
    orf_start = int(re.search(r'(\d+)\s(\d+)\t\{', line).group(1))
    orf_stop = int(re.search(r'(\d+)\s(\d+)\t\{', line).group(2))
    stop_codon = eval(re.search(r'\{.*\}', line).group(0))
    coordinate_stop = int(re.search(r'\}\t([^\t]+)', line).group(1))
    frequency_stop = float(re.search(r'([^\t]+)\n', line).group(1))
    gene = Gene(name_file, id, exons, orf_start, orf_stop, stop_codon, coordinate_stop, frequency_stop)
    return gene


def sort_name_file(list_files):
    list_name_file = []
    for file in list_files:
        name_file = file
        chr = re.search(r'chr([^_]+)', file).group(1)
        number = int(re.search(r'_(\d+)', file).group(1))
        name_gene = NameFile(name_file, chr, number)
        list_name_file.append(name_gene)

    list_name_file.sort(key=lambda x: [x.chr, x.number])
    return list_name_file


def creation_pairs_genes(list_genes):
    list_neighbors = list_genes[:number_neighbors]
    combinations_neighbors = list(combinations(list_neighbors, 2))
    for i in range(number_neighbors, len(list_genes)):
        list_neighbors = list_genes[i - number_neighbors + 1:i]
        new_neighbors = list_genes[i]
        for gene in list_neighbors:
            combinations_neighbors.append((gene, new_neighbors))
    return combinations_neighbors


def creation_pairs_gene(file_pairs):
    dict_gene_pairs = {}
    for file in file_pairs:
        dict_gene_pairs[file.name_file] = []
        for gene in gene_catalog:
            if file.name_file == gene.name_file:
                dict_gene_pairs[file.name_file].append(gene)
    comparison_pairs_gene(dict_gene_pairs)

def comparison_pairs_gene(comparison_pairs_gene):
    key = comparison_pairs_gene.keys()
    file_first = comparison_pairs_gene[key[0]]
    file_second = comparison_pairs_gene[key[1]]
    index = 0
    for i in range(len(file_first)):
        if file_first[i].id == file_second[i].id:
            if file_first[i].stop_codon != {} and file_second[i].stop_codon != {}:
                pairs = ComparisonPairs(file_first[i].name_file, file_second[i].name_file, file_first[i].id, file_first[i].stop_codon, file_second[i].stop_codon)
                catalog_pairs_gene.append(pairs)
                index = index + 1
    counting_pairs_gene[str(key[0])+ '|' + str(key[1])] = [index, index / number_individual]




file = open(in_file, "r")
for line in file:
    gene_catalog.append(deserialization(line))
file.close()

list_name_file = []
for gene in gene_catalog:
    list_name_file.append(gene.name_file)
#remove repeat
list_name_file = list(set(list_name_file))
list_name_file_sorted = sort_name_file(list_name_file)


dict_chr_file = {}
chr = list_name_file_sorted[0].chr
dict_chr_file[chr] = []
for file in list_name_file_sorted:
    if chr == file.chr:
        dict_chr_file[chr].append(file)
    else:
        chr = file.chr
        dict_chr_file[chr] = []
        dict_chr_file[chr].append(file)


dict_combinations_neighbor_genes = {}
for key in dict_chr_file.keys():
    list_one_chr_files = dict_chr_file[key]
    combinations_neighbor_genes = creation_pairs_genes(list_one_chr_files)
    dict_combinations_neighbor_genes[key] = combinations_neighbor_genes

for c in dict_combinations_neighbor_genes:
    for file_pairs in dict_combinations_neighbor_genes[c]:
        creation_pairs_gene(file_pairs)

file_write = open(out_file_frequency_codon, "w")
for pair in catalog_pairs_gene:
    file_write.write(str(pair.name_file_first) + "\t" + str(pair.name_file_second) + "\t" + str(pair.id) + "\t" + str(pair.stop_codon_first) + "\t" + str(pair.stop_codon_second) + "\n")
file_write.close()

file_write_counting = open(out_file_frequency_codon_counting, "w")
for pair in counting_pairs_gene:
    file_write_counting.write(str(pair) + "\t" + str(counting_pairs_gene[pair][0]) + "\t" + str(counting_pairs_gene[pair][1]) + "\n")
file_write_counting.close()
