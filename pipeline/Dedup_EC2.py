#!/usr/bin/env python

# open the Read 1 file
Read1_file = open("/projects/bgmp/shared/2021_projects/Salish/SalishProj/Reads/Read1_40_filtered_cut.fastq", "r") # opens the filtered Read1 file for reading
Read2_file = open("/projects/bgmp/shared/2021_projects/Salish/SalishProj/Reads/Read2_40_filtered_cut.fastq", "r")  # opens the filtered Read2 file for reading
#Read1_file = open("DDP_test1.fastq", "r")
#Read2_file = open("DDP_test2.fastq", "r")
#Dedup_file_1 = open("Read1_deduped_UMI_Probe.fastq", "wt") # opens a file to write deduplicated Reads to
#Dedup_file_2 = open("Read2_deduped_UMI_Probe.fastq", "wt")
Dedup_file_1=open("Dedup_UMI-Probe_EC_R1_118.fastq","wt")
#open("TESTDedup_UMI-Probe_EC_R1.fastq","wt")
Dedup_file_2=open("Dedup_UMI-Probe_EC_R2_118.fastq","wt")
#open("TESTDedup_UMI-Probe_EC_R2.fastq","wt")

num_lines = 0  # initialize a counter
for line in Read1_file:
    num_lines +=1 # count the number of lines in the file
Read1_file.seek(0) # point back to the beginning of the file

R1_four = []    # [header, sequence, +, qscore_line]
R2_four = []    # [header, sequence, +, qscore_line]

readline_counter = 0
Dedup_dict_1 = {}
Dedup_dict_2 = {}
while readline_counter < num_lines: # for every line in the file
    R1_four = [] # create an array to hold the four lines of a read
    R2_four = []   # clear the four line array before moving on to the next record
    for j in range(4): # do the following for four lines
        Read1_line = Read1_file.readline().rstrip("\n") # temporarily stores the current line of the read 1 file
        Read2_line = Read2_file.readline().rstrip("\n") # temporarily stores the current line of the read 2 file
        R1_four.append(Read1_line) # adds the line to the R1_four array
        R2_four.append(Read2_line) # adds the line to the R2_four array
    readline_counter += 4    # increment by four to start at the next line of the file
    umi = R1_four[1][:25]    # store the first 25 NT of read 1 as the UMI
    probe = R2_four[1][:45]  # store the first 45 NT of read 2 as the probe
    umi_probe = umi + "_" + probe # create a string that concatenates the UMI and Probe. This will serve as the key in the dictionaries. 
    if umi_probe in Dedup_dict_1 and Dedup_dict_2: 
        #{'UMI-Probe: [[name, sequence, +, qualityscore],[name, sequence, +, qualityscore],[name, sequence, +, qualityscore],[name, sequence, +, qualityscore]] '}
        Dedup_dict_1[umi_probe].append(R1_four) # If UMI-Probe already in the dictionary, add the read to the array of reads already present (add to the group of duplicates)
        Dedup_dict_2[umi_probe].append(R2_four)
    else: # otherwise
        Dedup_dict_1[umi_probe] = [] # add the UMI-Probe as a new key to the dictionary and create a new empty array 
        Dedup_dict_1[umi_probe].append(R1_four)
        Dedup_dict_2[umi_probe] = []
        Dedup_dict_2[umi_probe].append(R2_four)
    
# Go through each quadruplet and figure out what the length of the sequence is 
for umi_probe in Dedup_dict_1.keys():
    length_count_dict = {}
    lengths = []
    for read_array in Dedup_dict_1[umi_probe]:
        seq_len = len(read_array[1])   
        lengths.append(seq_len)
    min_len = min(lengths)

    for read_array in Dedup_dict_1[umi_probe]:
        if len(read_array[1]) != min_len: # if length of one read is equal to the best length
            new_seq = read_array[1][:min_len] 
            new_QS = read_array[3][:min_len]
            #print(new_seq)
            read_array[1] = new_seq
            read_array[3] = new_QS

for umi_probe in Dedup_dict_2.keys():
    length_count_dict = {}
    lengths = []
    for read_array in Dedup_dict_2[umi_probe]:
        seq_len = len(read_array[1])   
        lengths.append(seq_len)
    min_len = min(lengths)

    for read_array in Dedup_dict_2[umi_probe]:
        if len(read_array[1]) != min_len: # if length of one read is equal to the best length
            new_seq = read_array[1][:min_len] 
            new_QS = read_array[3][:min_len]
            #print(new_seq)
            read_array[1] = new_seq 
            read_array[3] = new_QS

for umi_probe in Dedup_dict_1.keys():
    Duplicate_group_array = Dedup_dict_1[umi_probe]
    Duplicate_group_array_2 = Dedup_dict_2[umi_probe]
    if len(Duplicate_group_array)==1 or len(Duplicate_group_array_2)==1: # if the read is a singleton, throw it out
        #print("singleton found: " + str(Duplicate_group_array))
        #print("singleton found: " + str(Duplicate_group_array_2))
        continue
    else:
        # error correction
        nt_counts_dict = {} # create a dictionary which has the position in the sequence and the NTs at that position across all duplicates in a group {0:[T,T,T,T,T], 1:[A,A,C,A,A]}
        numbers = [number for number in range(len(Duplicate_group_array[0][1]))]
        for i in numbers: 
            nt_counts_dict[i] = [] # create a dictionary where each key is a position (number) in the sequence
        for inner_array in Duplicate_group_array: # for each of the entries in a group of duplicates
            sequence = inner_array[1] # the sequence is the 1st (0-based) position in the array
            for i in range(len(sequence)): 
                nt_counts_dict[i].append(sequence[i])
            array_of_dicts = []
            for array_of_letters in nt_counts_dict.values():
                position_dict = {}
                array_of_dicts.append(position_dict)
                nucleotides = ["A","T","C","G"]
                for i in nucleotides:
                    position_dict[i] = 0
                for letter in array_of_letters:
                    position_dict[letter] += 1
        consensus = ''
        for dict in array_of_dicts:
            max_key = max(dict, key=dict.get)
            #print("max key:" + max_key)
            consensus = consensus + max_key
        Dedup_file_1.write(Duplicate_group_array[0][0] + "\n")
        Dedup_file_1.write(consensus + "\n")
        Dedup_file_1.write("+" + "\n")
        Dedup_file_1.write(Duplicate_group_array[0][3] + "\n")

for umi_probe in Dedup_dict_2.keys():
    Duplicate_group_array = Dedup_dict_2[umi_probe]
    Duplicate_group_array_1 = Dedup_dict_1[umi_probe]
    if len(Duplicate_group_array)==1 or len(Duplicate_group_array_1)==1: # if the read is a singleton, throw it out
        continue
    else:
        # error correction
        consensus = ''
        nt_counts_dict = {}
        numbers = [number for number in range(len(Duplicate_group_array[0][1]))]
        for i in numbers:
            nt_counts_dict[i] = []
        for inner_array in Duplicate_group_array:
            sequence = inner_array[1]
            for i in range(len(sequence)):
                nt_counts_dict[i].append(sequence[i])
            array_of_dicts = []
            for array_of_letters in nt_counts_dict.values():
                position_dict = {}
                array_of_dicts.append(position_dict)
                nucleotides = ["A", "T", "C", "G"]
                for i in nucleotides:
                    position_dict[i] = 0
                for letter in array_of_letters: 
                    position_dict[letter] += 1
        for dict in array_of_dicts:
            max_key = max(dict, key=dict.get)
            consensus = consensus + max_key
        Dedup_file_2.write(Duplicate_group_array[0][0] + "\n")
        Dedup_file_2.write(consensus + "\n")
        Dedup_file_2.write("+" + "\n")
        Dedup_file_2.write(Duplicate_group_array[0][3] + "\n")

