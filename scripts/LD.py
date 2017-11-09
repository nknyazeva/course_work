import re
in_file_pairs = "/Users/anastasia/PycharmProjects/course_work/real_data/frequency_pairs_genes.txt"
in_file_genes = "/Users/anastasia/PycharmProjects/course_work/real_data/threshold_genes_with_stop.txt"
out_file = "/Users/anastasia/PycharmProjects/course_work/LD.txt"

file_pairs = open(in_file_pairs, "r")
list_pairs = []
for line in file_pairs:
    name_file_first = re.search(r'(.+)\.fasta\|', line).group(1)
    name_file_second = re.search(r'\|(.+)\.fasta', line).group(1)
    frequency = float(re.search(r'\t(.+)\n', line).group(1))
    list_pairs.append([name_file_first, name_file_second, frequency])
file_pairs.close()

file_genes = open(in_file_genes, "r")
dict_genes = {}
for line in file_genes:
    name_file = re.search(r'(.+)\.fasta', line).group(1)
    frequency = float(re.search(r'\}\t(.+)\n', line).group(1))
    if name_file not in dict_genes.keys():
        dict_genes[name_file] = frequency
file_genes.close()

list_ld = []
file_none = []
for pair in list_pairs:
    p_a = dict_genes[pair[0]]
    p_b = dict_genes[pair[1]]
    p_ab = pair[2]
    ld = p_ab - p_a * p_b
    r2 = ld ** 2 / (p_a * (1 - p_a) * p_b * (1 - p_b))
    list_ld.append([pair[0], pair[1], ld, r2])

# print(list_ld)

file_ld = open(out_file, "w")
file_ld.write('gene_first' + "\t" + 'gene_second' + "\t" + 'ld' + "\t" + "r2" + '\n')
for pair in list_ld:
    file_ld.write(str(pair[0]))
    file_ld.write("\t")
    file_ld.write(str(pair[1]))
    file_ld.write("\t")
    file_ld.write(str(pair[2]))
    file_ld.write("\t")
    file_ld.write(str(pair[3]))
    file_ld.write("\n")
file_ld.close()