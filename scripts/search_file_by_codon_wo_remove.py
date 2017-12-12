import os

# direct = "/Users/anastasia/PycharmProjects/course_work/data/testData/"
# out_file = "/Users/anastasia/PycharmProjects/course_work/output/files_with_stop_codon_wo_remove.txt"

direct = "/mnt/lustre/potapova/200_flies/all_genes/"
out_file = "/mnt/lustre/nknyazeva/courseWork4/scripts/output/files_with_stop_codon_wo_remove.txt"

for folders, subfolders, files in os.walk(direct):
    file_list = files

f2 = open(out_file, "w")

for file in file_list:
    tmp = True
    f1 = open(os.path.join(direct, file), "r")
    for line in f1:
        if line[0] != ">":
            str = line[:-4]
            for codon in range(0, len(str), 3):
                current_codon = str[codon:codon + 3]
                if current_codon == 'TAA' or current_codon == 'TAG' or current_codon == 'TGA':
                    f2.write(file + "\n")
                    # print(file)
                    tmp = False
                    break
        if tmp == False:
            break
    f1.close()

f2.close()
