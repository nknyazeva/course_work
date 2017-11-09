import re

in_file = "/Users/anastasia/PycharmProjects/course_work/old_scripts/testGene.txt"
in_file_one = "/Users/anastasia/PycharmProjects/course_work/old_scripts/testGene_one.txt"
in_file_codon = "/Users/anastasia/PycharmProjects/course_work/old_scripts/frequencyCodon.txt"

out_file_frequency_codon = "/Users/anastasia/PycharmProjects/course_work/old_scripts/testGene_threshold.txt"

# in_file = "/mnt/lustre/nknyazeva/courseWork4/scripts/output/gene_description.txt"
# in_file_one = "/mnt/lustre/nknyazeva/courseWork4/scripts/output/gene_description_one.txt"
# in_file_codon = "/mnt/lustre/nknyazeva/courseWork4/scripts/output/frequency_stop_codon.txt"
#
# out_file_frequency_codon = "/mnt/lustre/nknyazeva/courseWork4/scripts/output/gene_description_threshold.txt"

global gene_catalog
gene_catalog = []

global codon_catalog
codon_catalog = []

class Gene:
    def __init__(self, name_file, id, exons, orf_start, orf_stop, stop_codon):
        self.name_file = name_file
        self.id = id
        self.exons = exons
        self.orf_start = orf_start
        self.orf_stop = orf_stop
        self.stop_codon = stop_codon

class Codon:
    def __init__(self, name_file, coordinate, frequency):
        self.name_file = name_file
        self.coordinate = coordinate
        self.frequency = frequency


def deserialization_gene(line):
    name_file = re.search(r'\w+\.\w+', line).group(0)
    id = re.search(r'>\w+', line).group(0)
    exons = eval(re.search(r'\[\[.+\]\]', line).group(0))
    orf_start = int(re.search(r'(\d+)\s(\d+)\t\{', line).group(1))
    orf_stop = int(re.search(r'(\d+)\s(\d+)\t\{', line).group(2))
    stop_codon = eval(re.search(r'\{.*\}', line).group(0))
    gene = Gene(name_file, id, exons, orf_start, orf_stop, stop_codon)
    return gene

def deserialization_gene_one(line):
    name_file = re.search(r'\w+\.\w+', line).group(0)
    id = re.search(r'>\w+', line).group(0)
    exons = []
    orf_start = int(re.search(r'(\d+)\s(\d+)\t\{', line).group(1))
    orf_stop = int(re.search(r'(\d+)\s(\d+)\t\{', line).group(2))
    stop_codon = eval(re.search(r'\{.*\}', line).group(0))
    gene = Gene(name_file, id, exons, orf_start, orf_stop, stop_codon)
    return gene

def deserialization_codon(line):
    name_file = re.search(r'(c[^\t]+)\t', line).group(1)
    coordinate = re.search(r'(c[^\t]+)\t([^\t]+)', line).group(2)
    frequency = eval(re.search(r'([^\t]+)\n', line).group(1))
    codon = Codon(name_file, coordinate, frequency)
    return codon

file = open(in_file, "r")
for line in file:
    gene_catalog.append(deserialization_gene(line))
file.close()


file_one = open(in_file_one, "r")
for line in file_one:
    gene_catalog.append(deserialization_gene_one(line))
file_one.close()

file_codon = open(in_file_codon, "r")
for line in file_codon:
    codon_catalog.append(deserialization_codon(line))
file.close()

file_write = open(out_file_frequency_codon, "w")
for codon in codon_catalog:
    for gene in gene_catalog:
        if codon.name_file == gene.name_file:
            file_write.write(str(gene.name_file) + "\t" + str(gene.id) + "\t" + str(gene.exons) + "\t" + str(gene.orf_start) + "\t" + str(gene.orf_stop) + "\t" + str(gene.stop_codon) + "\t" + str(codon.coordinate) + "\t" + str(codon.frequency) + "\n")
file_write.close()


