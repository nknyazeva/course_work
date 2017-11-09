import os

direct = "/Users/anastasia/PycharmProjects/course_work/testData/"
out_file = "/Users/anastasia/PycharmProjects/course_work/files_with_stop_codon.txt"

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
                    tmp = False
                    break
        if tmp == False:
            break
    f1.close()

f2.close()
