import re, sys
from itertools import combinations

a = sys.argv
a = a[1:]
threshold = str(a[0])

# in_file = '_'.join(["/Users/anastasia/PycharmProjects/course_work/output/threshold_genes_with_stop", str(threshold)])
# out_file_frequency_codon = '_'.join(["/Users/anastasia/PycharmProjects/course_work/output/all_description_pairs_genes", str(threshold)])
# out_file_frequency_codon_counting = '_'.join(["/Users/anastasia/PycharmProjects/course_work/output/all_frequency_pairs_genes", str(threshold)])


in_file = '_'.join(["/mnt/lustre/nknyazeva/courseWork4/repository/output/n_threshold_genes_with_stop", str(threshold)])
out_file_frequency_codon = '_'.join(["/mnt/lustre/nknyazeva/courseWork4/repository/output/all_description_pairs_genes", str(threshold), str(number_neighbors)])
out_file_frequency_codon_counting = '_'.join(["/mnt/lustre/nknyazeva/courseWork4/repository/output/all_frequency_pairs_genes", str(threshold), str(number_neighbors)])

number_individual = float(197)

global gene_catalog
gene_catalog = []

global catalog_pairs_gene
catalog_pairs_gene = []

global counting_pairs_gene
counting_pairs_gene = {}

global list_files_with_stop

class Gene:
    def __init__(self, name_file, id, exons, orf_start, orf_stop, stop_codon, frequency_stop):
        self.name_file = name_file
        self.id = id
        self.exons = exons
        self.orf_start = orf_start
        self.orf_stop = orf_stop
        self.stop_codon = stop_codon
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
    frequency_stop = float(re.search(r'([^\t]+)\n', line).group(1))
    gene = Gene(name_file, id, exons, orf_start, orf_stop, stop_codon, frequency_stop)
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
    counting_pairs_gene[str(key[0]) + '|' + str(key[1])] = [index, index / number_individual]


file = open(in_file, "r")
list_files_with_stop = []
for line in file:
    gene = deserialization(line)
    gene_catalog.append(gene)
    if gene.name_file not in list_files_with_stop:
        list_files_with_stop.append(gene.name_file)
file.close()

list_name_file = []
for gene in gene_catalog:
    list_name_file.append(gene.name_file)

#remove repeat
list_name_file = list(set(list_name_file))
list_name_file_sorted = sort_name_file(list_name_file)


dict_chr_file = {}
chr_tmp = list_name_file_sorted[0].chr
dict_chr_file[chr_tmp] = []
for file in list_name_file_sorted:
    if chr_tmp == file.chr:
        dict_chr_file[chr_tmp].append(file)
    else:
        chr_tmp = file.chr
        dict_chr_file[chr_tmp] = []
        dict_chr_file[chr_tmp].append(file)


dict_combinations_genes = {}
for key in dict_chr_file.keys():
    list_one_chr_files = dict_chr_file[key]
    combinations_genes = list(combinations(list_one_chr_files, 2))
    dict_combinations_genes[key] = combinations_genes

for c in dict_combinations_genes:
    for file_pairs in dict_combinations_genes[c]:
        creation_pairs_gene(file_pairs)

file_write = open(out_file_frequency_codon, "w")
for pair in catalog_pairs_gene:
    number_first = int(re.search(r'_(\d+)', pair.name_file_first).group(1))
    number_second = int(re.search(r'_(\d+)', pair.name_file_second).group(1))
    difference = max(number_first, number_second) - min(number_first, number_second)
    file_write.write(str(difference) + "\t" +
                     str(pair.name_file_first) + "\t" +
                     str(pair.name_file_second) + "\t" +
                     str(pair.id) + "\t" +
                     str(pair.stop_codon_first) + "\t" +
                     str(pair.stop_codon_second) + "\n")
file_write.close()

file_write_counting = open(out_file_frequency_codon_counting, "w")
for pair in counting_pairs_gene:
    file_write_counting.write(str(pair) + "\t" + str(counting_pairs_gene[pair][1]) + "\n")
file_write_counting.close()
