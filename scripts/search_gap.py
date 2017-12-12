import os, math

# direct = "/Users/anastasia/PycharmProjects/course_work/data/testData/"
# out_file = "/Users/anastasia/PycharmProjects/course_work/output/files_with_gap.txt"

direct = "/mnt/lustre/potapova/200_flies/all_genes/"
out_file = "/mnt/lustre/nknyazeva/courseWork4/repository/output/files_with_gap.txt"

for folders, subfolders, files in os.walk(direct):
    file_list = files

f2 = open(out_file, "w")

for file in file_list:
    f1 = open(os.path.join(direct, file), "r")
    for line in f1:
        if line[0] != ">":
            for i in range(len(line)):
                if line[i] == '-':
                    f2.write(file + "\n")
    f1.close()

f2.close()