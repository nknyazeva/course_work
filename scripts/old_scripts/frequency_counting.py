import re

in_file = "/Users/anastasia/PycharmProjects/course_work/testCodon.txt"
in_file_one = "/Users/anastasia/PycharmProjects/course_work/testCodon_one.txt"
out_file_frequency_codon = "/Users/anastasia/PycharmProjects/course_work/frequencyCodon.txt"

global number_individual
number_individual = float(197)

def write_frequency(in_file, out_file):

    for line in in_file:
        number_stop = float((re.search(r'(\d+)\n', line).group(1)))
        frequency_stop = number_stop / number_individual
        out_file.write(line.strip() + "\t" + str(frequency_stop) + "\n")

    in_file.close()

file = open(in_file, "r")
file_one = open(in_file_one, "r")
outfile_frequency = open(out_file_frequency_codon, "w")
write_frequency(file, outfile_frequency)
write_frequency(file_one, outfile_frequency)
outfile_frequency.close()



