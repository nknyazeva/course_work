import os

# direct = "/Users/anastasia/PycharmProjects/course_work/testData/"
# in_file = "/Users/anastasia/PycharmProjects/course_work/files_with_stop_codon.txt"
# out_file = "/Users/anastasia/PycharmProjects/course_work/files_wo_stop_codons.txt"

direct = "/mnt/lustre/potapova/200_flies/all_genes/"
in_file = "/mnt/lustre/nknyazeva/courseWork4/repository/output/files_with_stop_codon.txt"
out_file = "/mnt/lustre/nknyazeva/courseWork4/repository/output/files_wo_stop_codons.txt"



file_stop = open(in_file, "r")
list_file_stop = []
for line in file_stop:
    file = line.strip()
    list_file_stop.append(file)
file_stop.close()

file_w = open(out_file, "w")
files = os.walk(direct)
for i in files:
    list_files = i[2]
    for file in list_files:
        if file in list_file_stop:
            continue
        else:
            file_w.write(file + "\n")
file_w.close()


