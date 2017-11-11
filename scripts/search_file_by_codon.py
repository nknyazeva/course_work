import os, math

# direct = "/Users/anastasia/PycharmProjects/course_work/data/testData/"
# out_file = "/Users/anastasia/PycharmProjects/course_work/output/files_with_stop_codon.txt"

direct = "/mnt/lustre/potapova/200_flies/all_genes/"
out_file = "/mnt/lustre/nknyazeva/courseWork4/repository/output/files_with_stop_codon.txt"

border_amount = 0.05

for folders, subfolders, files in os.walk(direct):
    file_list = files

f2 = open(out_file, "w")

for file in file_list:
    tmp = True
    f1 = open(os.path.join(direct, file), "r")
    for line in f1:
        if line[0] != ">":
            str = line[:-4]
            #remove border_amount% of the gene at the beginning and at the end
            removal_length = int(math.floor(len(str) * border_amount))
            remainder_of_division = removal_length % 3
            if remainder_of_division == 1:
                removal_length = removal_length - 1
            if remainder_of_division == 2:
                removal_length = removal_length - 2
            str_wo_border = str[removal_length: - removal_length]
            for codon in range(0, len(str_wo_border), 3):
                current_codon = str_wo_border[codon:codon + 3]
                if current_codon == 'TAA' or current_codon == 'TAG' or current_codon == 'TGA':
                    f2.write(file + "\n")
                    tmp = False
                    break
        if tmp == False:
            break
    f1.close()

f2.close()
