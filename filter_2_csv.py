# WORK IN PROGRESS
# this is a first stab at the creation of a filtering algorithm that performs following funciton:
# 1: Filter by LINDA (perfect match)
# 2: filter by probe (perfect match)
# 3: determine the percent of reads on target

import argparse
import csv

######### ARGPARSE SETUP #########

def getArgs(): 
	parser=argparse.ArgumentParser()
	parser.add_argument(
		"--linda", "-l", help="Path to file containing linda sequences", type=str, required=True
	)
	parser.add_argument(
		"--read1", help="Path to read 1 fastq file", type=str, required=True
	)
	parser.add_argument(
		"--read2", help="Path to read 2 fastq file", type=str, required=True
	)
	parser.add_argument(
		"--probe", "-p", help="Path to file containing probe oligos", type=str, required=True
	)

	return parser.parse_args()

args = getArgs()
l = args.linda
r1 = args.read1
r2 = args.read2
p = args.probe

######### ESTABLISHING GLOBAL VARIABLES #########

linda_ct = 0 # a value that will track how many reads have perfect lindas
probe_ct = 0 # a value that will track how many reads have perfect probes

lindas_dict = {} # a dictionary to hold linda counts, with the linda sequence as key, and values of the count and name of the linda sequences.
probes_dict = {} # not sure if this is needed, would hold probe counts (probe sequence as key, count as value), but if sorting done well, redundant based off of lindas dictionary
tocheck_dict = {} # a dictionary that will have two keys: lindas, and probes, with values being a list of all sequences given for each of these

######### READING LINDA AND PROBE FILES, FILLING DICTIONARIES #########
with open(l, 'r') as linda, open(p, 'r') as probe:
	first = True
	# looping through the linda file, which contains the name of the linda sequence and the sequence itself. Stores in two dictionaries, for later use
	for line in linda:
		line=line.strip().split()
		name = line[0]
		seq = line[1]
		lindas_dict[seq] = [0, name] # adds lindas to a lindas_dict
		if first==True:
			tocheck_dict['lindas'] = [seq]
			first = False
		else:
			tocheck_dict['lindas'] += [seq]

	first = True
	# looping through the probes file, which was adapted from excel file. This version only has the 45 nt. segements, since these are more stringent and required for verification
	for line in probe:
		line = line.strip().upper() # some of these sequences were lowercase, required the use of upper
		probes_dict[line[:40]] = 0
		if first == True:
			tocheck_dict['probes'] = [line[:40]]
			first=False
		else:
			tocheck_dict['probes'] += [line[:40]]

######### READING FASTQ FILES, FILTERING READS #########

i = 0 # counts total number of reads covered
on_target = 0 # counts the number of reads that are on target

# for this section, need to determine the locations of the LINDA and targeting oligos (probes), so string slicing will work 
first=True
with open(r1, 'r') as read1, open(r2, 'r') as read2, open('Read1Filtered.fastq', 'w') as out1, open('Read2Filtered.fastq', 'w') as out2,  open('Report.csv', 'w', newline='') as rep:
	while True:
		# reads in header lines from both files and stores for later reprinting
		header1 = read1.readline().strip()
		header2 = read2.readline().strip()
		if header1 == '':
			break

		# reads in sequence lines from both files and stores for later reprinting
		sequence1 = read1.readline().strip()
		linda_r1 = sequence1[8:18]
		sequence2 =  read2.readline().strip()
		probe_r2 = sequence2[0:40]
		# determine number of reads with perfect probe, can't do later because script checks probes after lindas
		if probe_r2 in tocheck_dict['probes']:
			probe_ct += 1

		# reads in the plus line from each file, only stores one (expect no difference between the two)
		extra = read1.readline().strip()
		read2.readline()

		# reads in quality score line from each file, stores for later reprinting
		qual1 = read1.readline().strip()
		qual2 = read2.readline().strip()

		# determine number of reads with perfect probe, can't do later because script checks probes after lindas

		# first if statement compares the linda sequence in the read1 file to the list of linda sequences
		if linda_r1 in tocheck_dict['lindas']:
			linda_ct += 1
			if probe_r2 in tocheck_dict['probes']:
				if first==True:
					out1.write(header1 + '\n' + sequence1 + '\n' +  extra + '\n' +  qual1)
					out2.write(header2 + '\n' +  sequence2 + '\n' +  extra + '\n' +  qual2)
					lindas_dict[linda_r1][0] += 1
					probes_dict[probe_r2] += 1
					on_target += 1
					first=False
				else:
					out1.write('\n' + header1 + '\n' + sequence1 + '\n' +  extra + '\n' +  qual1)
					out2.write('\n' + header2 + '\n' +  sequence2 + '\n' +  extra + '\n' +  qual2)
					lindas_dict[linda_r1][0] += 1
					probes_dict[probe_r2] += 1
					on_target += 1
		i += 1

	csv_w = csv.writer(rep)
	
	file_head = (str(round(100 * (on_target / i), 2)) + ' percent of reads were on target (perfect match of LINDA in R1 and probe sequence in R2)')
	csv_w.writerow([file_head])
	csv_w.writerow([])
	csv_w.writerow(['Percent reads with perfect LINDAs', 'Percent reads with perfect probes'])
	csv_w.writerow([str(round(100 * (linda_ct / i), 2)), str(round(100*(probe_ct / i), 2))])
	csv_w.writerow([])
	csv_w.writerow(['LINDA','Count','Percentage of on-target reads'])
	for linda in lindas_dict.keys():
		data = [lindas_dict[linda][1], str(lindas_dict[linda][0]), str(round(100*(lindas_dict[linda][0])/on_target, 2))]
		csv_w.writerow(data)
	csv_w.writerow([])
	csv_w.writerow(['Probe sequence', 'Count', 'Percentage of on-target reads'])
	for probe in probes_dict.keys():
		data = [probe, str(probes_dict[probe]), str(round(100*(probes_dict[probe]/on_target), 2))]
		csv_w.writerow(data)