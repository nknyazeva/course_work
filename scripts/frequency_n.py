import os
import json

# direct = "/Users/anastasia/PycharmProjects/course_work/data/testData/"
# out_file = "/Users/anastasia/PycharmProjects/course_work/output/stop_codon_relative_coordinate.txt"
# out_file_before = "/Users/anastasia/PycharmProjects/course_work/output/list_stop_codon_before.txt"
# out_file_after = "/Users/anastasia/PycharmProjects/course_work/output/list_stop_codon_after.txt"



direct = "/mnt/lustre/potapova/200_flies/all_genes/"
out_file = "/mnt/lustre/nknyazeva/courseWork4/scripts/output/stop_codon_relative_coordinate.txt"
out_file_before = "/mnt/lustre/nknyazeva/courseWork4/scripts/output/list_stop_codon_before.txt"
out_file_after = "/mnt/lustre/nknyazeva/courseWork4/scripts/output/list_stop_codon_after.txt"


for folders, subfolders, files in os.walk(direct):
    file_list = files

f2 = open(out_file, "w")

result = []

for file in file_list:
    tmp = True
    f1 = open(os.path.join(direct, file), "r")
    for line in f1:
        if line[0] != ">":
            string = line[:-4]
            index = 0
            for codon in range(0, len(string), 3):
                current_codon = string[codon:codon + 3]
                index = index + 3
                if current_codon == 'TAA' or current_codon == 'TAG' or current_codon == 'TGA':
                    data = {}
                    data["file_name"] = file
                    data["current_codon"] = current_codon
                    data["coord"] = index - 3
                    data["number_n"] = 0
                    result.append(data)
                    tmp = False
                    break
        if tmp == False:
            break
    f1.close()

f2.write(json.dumps(result, sort_keys=True,
                      indent=4, separators=(',', ': ')))
f2.close()

for data in result:
    f1 = open(os.path.join(direct, data["file_name"]), "r")
    for line in f1:
        if line[0] != ">":
            if line[data["coord"]] == 'N' or line[data["coord"] + 1] == 'N' or line[data["coord"] + 2] == 'N':
                data["number_n"] = data["number_n"] + 1

f3 = open(out_file_before, "w")
f4 = open(out_file_after, "w")
for data in result:
    f3.write(data["file_name"] + "\n")
    if data["number_n"] == 0:
        f4.write(data["file_name"] + "\n")

f3.close()
f4.close()

# import json
#
# class Codon(object):
#     def __init__(self, name, coords, index):
#         self.name = name
#         self.coords = coords
#         self.index = index
#
#
# def codon_decoder(obj):
#     return Codon(
#         obj['name'],
#         obj['coords'],
#         obj['index'])
#
#
# codons = json.loads(out_file, object_hook=object_decoder)
#
# f2.write(json.dumps(codons))
