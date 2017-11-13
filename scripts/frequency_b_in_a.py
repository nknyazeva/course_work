import re, sys
a = sys.argv
a = a[1:]
threshold = str(a[0])

in_file_pairs = '_'.join(["/mnt/lustre/nknyazeva/courseWork4/repository/output/ng_frequency_pairs_genes", str(threshold)])
in_file_genes = '_'.join(["/mnt/lustre/nknyazeva/courseWork4/repository/output/ng_threshold_genes_with_stop", str(threshold)])
out_file = '_'.join(["/mnt/lustre/nknyazeva/courseWork4/repository/output/ng_frequency_b_in_a_max_a", str(threshold)])

# in_file_pairs = '_'.join(["/Users/anastasia/PycharmProjects/course_work/output/real_data/frequency_pairs_genes", str(threshold)])
# in_file_genes = '_'.join(["/Users/anastasia/PycharmProjects/course_work/output/real_data/threshold_genes_with_stop", str(threshold)])
# out_file = '_'.join(["/Users/anastasia/PycharmProjects/course_work/output/real_data/frequency_b_in_a_max_a", str(threshold)])


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

list_frequency = []
file_none = []
for pair in list_pairs:
    p_a = dict_genes[pair[0]]
    p_b = dict_genes[pair[1]]
    p_ab = pair[2]
    frequency_b_in_a = p_ab / min(p_a, p_b)
    list_frequency.append([pair[0], pair[1], max(p_a, p_b), min(p_a, p_b), p_ab, frequency_b_in_a])

file_ld = open(out_file, "w")
file_ld.write('gene_first' + "\t" + 'gene_second' + "\t" + 'frequency_max_a' + "\t" + 'frequency_min_b' + "\t" + 'frequency_ab' + "\t" + "frequency_b_in_a" + '\n')
for pair in list_frequency:
    file_ld.write(str(pair[0]))
    file_ld.write("\t")
    file_ld.write(str(pair[1]))
    file_ld.write("\t")
    file_ld.write(str(pair[2]))
    file_ld.write("\t")
    file_ld.write(str(pair[3]))
    file_ld.write("\t")
    file_ld.write(str(pair[4]))
    file_ld.write("\t")
    file_ld.write(str(pair[5]))
    file_ld.write("\n")
file_ld.close()