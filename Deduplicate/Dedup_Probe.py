#!/usr/bin/env python


# open the Read 1 file
#Read1_file = open("/projects/bgmp/shared/2021_projects/Salish/SalishProj/Reads/R1_filtered_cut.fastq", "r") # opens the filtered Read1 file for reading
#Read2_file = open("/projects/bgmp/shared/2021_projects/Salish/SalishProj/Reads/R2_filtered_cut.fastq", "r")  # opens the filtered Read2 file for reading
Read1_file = open("DDP_test1.fastq", "r") 
Read2_file = open("DDP_test2.fastq", "r")
#Dedup_file_1 = open("Read1_deduped_UMI_Probe.fastq", "wt") # opens a file to write deduplicated Reads to
#Dedup_file_2 = open("Read2_deduped_UMI_Probe.fastq", "wt")
Dedup_file_1=open("Dedup_test1.fastq","wt")
Dedup_file_2=open("Dedup_test2.fastq","wt")

num_lines = 0  # initialize a counter
for line in Read1_file: 
    num_lines +=1 # count the number of lines in the file
Read1_file.seek(0)

R1_four = []    # [header, sequence, +, qscore_line]
R2_four = []    # [header, sequence, +, qscore_line]

readline_counter = 0
Dedup_dict_1 = {}
Dedup_dict_2 = {}
while readline_counter < num_lines: # for every line in the file
    R1_four = [] 
    R2_four = []   # clear the four line array before moving on to the next record
    for j in range(4): # do the following for for lines
        Read1_line = Read1_file.readline().rstrip("\n") # temporarily stores the current line
        Read2_line = Read2_file.readline().rstrip("\n")
        R1_four.append(Read1_line) # adds the line to the R1_four array
        R2_four.append(Read2_line)
    readline_counter += 4    # increment by four to start at the next line of the file
    umi = R1_four[1][:25]
    probe = R2_four[1][:45]
    umi_probe = umi + "_" + probe
    if umi_probe in Dedup_dict_1 and Dedup_dict_2:
        continue
    else:
        Dedup_dict_1[umi_probe] = R1_four
        Dedup_dict_2[umi_probe] = R2_four

for value in Dedup_dict_1.values(): # when you get through the last entry of the last chromosome, empty the contents of the dictionary 
    for item in value:
        Dedup_file_1.write(item + "\n")


for value in Dedup_dict_2.values(): # when you get through the last entry of the last chromosome, empty the contents of the dictionary 
    for item in value:
        Dedup_file_2.write(item + "\n")