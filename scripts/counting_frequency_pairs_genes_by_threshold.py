import re, sys
from itertools import combinations

a = sys.argv
a = a[1:]
threshold = str(a[0])

global number_neighbors
number_neighbors = str(a[1])

in_file = '_'.join(["/Users/anastasia/PycharmProjects/course_work/output/threshold_genes_with_stop", str(threshold)])
in_file_wo_stop = "/Users/anastasia/PycharmProjects/course_work/output/files_wo_stop_codons.txt"
in_file_no_threshold = '_'.join(["/Users/anastasia/PycharmProjects/course_work/output/no_threshold_genes_with_stop", str(threshold)])
out_file_frequency_codon = '_'.join(["/Users/anastasia/PycharmProjects/course_work/output/test_description_pairs_genes", str(threshold)])
out_file_frequency_codon_counting = '_'.join(["/Users/anastasia/PycharmProjects/course_work/output/test_frequency_pairs_genes", str(threshold)])


# in_file = '_'.join(["/mnt/lustre/nknyazeva/courseWork4/repository/output/threshold_genes_with_stop", str(threshold)])
# in_file_wo_stop = "/mnt/lustre/nknyazeva/courseWork4/repository/output/files_wo_stop_codons.txt"
# in_file_no_threshold = '_'.join(["/mnt/lustre/nknyazeva/courseWork4/repository/output/no_threshold_genes_with_stop", str(threshold)])
# out_file_frequency_codon = '_'.join(["/mnt/lustre/nknyazeva/courseWork4/repository/output/description_pairs_genes", str(threshold), str(number_neighbors)])
# out_file_frequency_codon_counting = '_'.join(["/mnt/lustre/nknyazeva/courseWork4/repository/output/frequency_pairs_genes", str(threshold), str(number_neighbors)])

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


def creation_pairs_files(list_genes):
    list_neighbors = list_genes[:number_neighbors]
    combinations_neighbors = []
    tmp = list(combinations(list_neighbors, 2))
    for t in tmp:
        if t[0].name_file in list_files_with_stop:
            if t[1].name_file in list_files_with_stop:
                combinations_neighbors.append(t)
    for i in range(number_neighbors, len(list_genes)):
        list_neighbors = list_genes[i - number_neighbors + 1:i]
        new_neighbors = list_genes[i]
        if new_neighbors.name_file in list_files_with_stop:
            for gene in list_neighbors:
                if gene.name_file in list_files_with_stop:
                    combinations_neighbors.append((gene, new_neighbors))
    return combinations_neighbors


def creation_pairs_gene(file_pairs):
    dict_gene_pairs = {}
    for file in file_pairs:
        dict_gene_pairs[file.name_file] = []
        for gene in gene_catalog:
            if file.name_file == gene.name_file:
                dict_gene_pairs[file.name_file].append(gene)
    print(dict_gene_pairs)
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


file_stop = open(in_file_wo_stop, "r")
list_file_wo_stop = []
for line in file_stop:
    file = line.strip()
    list_file_wo_stop.append(file)
file_stop.close()

#add file more threshold
file_no_threshold = open(in_file_no_threshold, "r")
for line in file_no_threshold:
    file = line.strip()
    if file not in list_file_wo_stop:
        list_file_wo_stop.append(file)
file_no_threshold.close()

list_id = ['>dm5', '>ZI10', '>ZI103', '>ZI104', '>ZI114N', '>ZI117', '>ZI118N', '>ZI126', '>ZI129', '>ZI134N', '>ZI136', '>ZI138', '>ZI152', '>ZI157', '>ZI161', '>ZI164', '>ZI165', '>ZI167', '>ZI170', '>ZI172', '>ZI173', '>ZI176', '>ZI177', '>ZI178', '>ZI179', '>ZI181', '>ZI182', '>ZI184', '>ZI185', '>ZI188', '>ZI190', '>ZI191', '>ZI193', '>ZI194', '>ZI196', '>ZI197N', '>ZI198', '>ZI199', '>ZI200', '>ZI202', '>ZI206', '>ZI207', '>ZI210', '>ZI211', '>ZI212', '>ZI213', '>ZI214', '>ZI216N', '>ZI218', '>ZI219', '>ZI220', '>ZI221', '>ZI225', '>ZI226', '>ZI227', '>ZI228', '>ZI230', '>ZI231', '>ZI232', '>ZI233', '>ZI235', '>ZI237', '>ZI239', '>ZI240', '>ZI241', '>ZI250', '>ZI251N', '>ZI252', '>ZI253', '>ZI254N', '>ZI255', '>ZI26', '>ZI261', '>ZI263', '>ZI264', '>ZI265', '>ZI267', '>ZI268', '>ZI269', '>ZI27', '>ZI271', '>ZI273N', '>ZI276', '>ZI279', '>ZI28', '>ZI281', '>ZI284', '>ZI286', '>ZI291', '>ZI292', '>ZI293', '>ZI295', '>ZI296', '>ZI303', '>ZI311N', '>ZI313', '>ZI314', '>ZI316', '>ZI317', '>ZI319', '>ZI31N', '>ZI320', '>ZI321', '>ZI324', '>ZI329', '>ZI33', '>ZI332', '>ZI333', '>ZI335', '>ZI336', '>ZI339', '>ZI341', '>ZI342', '>ZI344', '>ZI348', '>ZI351', '>ZI352', '>ZI353', '>ZI357N', '>ZI358', '>ZI359', '>ZI362', '>ZI364', '>ZI365', '>ZI368', '>ZI370', '>ZI373', '>ZI374', '>ZI377', '>ZI378', '>ZI379', '>ZI380', '>ZI381', '>ZI384', '>ZI386', '>ZI388', '>ZI392', '>ZI394N', '>ZI395', '>ZI396', '>ZI397N', '>ZI398', '>ZI400', '>ZI402', '>ZI405', '>ZI413', '>ZI418N', '>ZI420', '>ZI421', '>ZI429', '>ZI431', '>ZI433', '>ZI437', '>ZI443', '>ZI444', '>ZI445', '>ZI446', '>ZI447', '>ZI448', '>ZI453', '>ZI455N', '>ZI456', '>ZI457', '>ZI458', '>ZI460', '>ZI466', '>ZI467', '>ZI468', '>ZI471', '>ZI472', '>ZI476', '>ZI477', '>ZI486', '>ZI488', '>ZI490', '>ZI491', '>ZI504', '>ZI505', '>ZI508', '>ZI50N', '>ZI514N', '>ZI517', '>ZI523', '>ZI524', '>ZI527', '>ZI530', '>ZI56', '>ZI59', '>ZI61', '>ZI68', '>ZI76', '>ZI81', '>ZI85', '>ZI86', '>ZI90', '>ZI91', '>ZI99']

for file_wo_stop in list_file_wo_stop:
    name_file = file_wo_stop
    for id in list_id:
        gene = Gene(name_file, id, [], 0, 0, {}, 0.0)
        gene_catalog.append(gene)

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
    combinations_neighbor_genes = creation_pairs_files(list_one_chr_files)
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
    file_write_counting.write(str(pair) + "\t" + str(counting_pairs_gene[pair][1]) + "\n")
file_write_counting.close()
