# WORK IN PROGRESS
# this is a first stab at the creation of a filtering algorithm that performs following funciton:
# 1: Filter by LINDA (perfect match)
# 2: filter by probe (perfect match)
# 3: determine the percent of reads on target

import argparse

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
l = args.l
r1 = args.read1
r2 = args.read2
p = args.p

######### ESTABLISHING GLOBAL VARIABLES #########

lindas_dict = {} # a dictionary to hold linda counts, with the linda sequence as key, and values of the count and name of the linda sequences.
probes_dict = {} # not sure if this is needed, would hold probe counts (probe sequence as key, count as value), but if sorting done well, redundant based off of lindas dictionary
tocheck_dict = {} # a dictionary that will have two keys: lindas, and probes, with values being a list of all sequences given for each of these

######### READING LINDA AND PROBE FILES, FILLING DICTIONARIES #########

with open(l, 'r') as linda, open(p, 'r') as probe:
	# looping through the linda file, which contains the name of the linda sequence and the sequence itself. Stores in two dictionaries, for later use
	for line in linda:
		line=line.strip().split()
		name = line[0]
		seq = line[1]
		lindas_dict[seq] = [0, name] # adds lindas to a lindas_dict
		tocheck_dict['lindas'] += seq

	# looping through the probes file, which was adapted from excel file. This version only has the 45 nt. segements, since these are more stringent and required for verification
	for line in probe:
		line = line.strip().upper()
		tocheck_dict['probes'] += line

######### READING FASTQ FILES, FILTERING READS #########

keepersr1 = []
keepersr2 = []

with open(r1, 'r') as read1, open(r2, 'r') as read2:
	while True:
		# reads in header lines from both files and stores for later reprinting
		header1 = read1.readline().strip()
		header2 = read2.readline().strip()

		# reads in sequence lines from both files and stores for later reprinting
		sequence1 = read1.readline().strip()
		linda_r1 = sequence1[:]
		sequence2 =  read2.readline().strip()
		linda_r2 = sequence2[:]

		# reads in the plus line from each file, only stores one (expect no difference between the two)
		extra = read1.readline().strip()
		read2.readline()

		# reads in quality score line from each file, stores for later reprinting
		qual1 = read1.readline().strip()
		qual2 = read2.readline().strip()

		# first if statement compares the linda sequence in the read1 file to the list of linda sequences
		if linda_r1 in tocheck_dict['lindas']:
			if sequence2[:] in tocheck_dict['probes']:
				keepersr1 += [header1, sequence1, extra, qual1]
				keepersr2 += [header2, sequence2, extra, qual2]
				lindas_dict[linda_r1][0] += 1
				on_target += 1
		
		i += 1

######### GENERATION OF OUTPUT FILES #########

# writes to a new fastq that contains only on-target reads in read1 file... might not be necessary later, but for now, nice way of keeping track of what was a hit
with open('Read1Filtered.fastq', 'w') as out1:
	for entry in keepersr1:
		for segment in entry: 
			out1.write(segment + '\n')

# same idea as above, but for read 2
with open('Read2Filtered.fastq', 'w') as out2:
	for entry in keepersr2:
		for segment in entry:
			out2.write(segment + '\n')

# generates a markdown file denoting what percentage of reads were on target, while also telling how many reads were on target per linda
with open('Report.md', 'w') as rep:
	rep.write('The percent of reads that were on target was' + (100 * (on_target / i)) + '%' + '\n')
	for linda in lindas_dict.keys():
		rep.write('The number of reads on target for ' + lindas_dict[linda][1] + 'was ' + lindas_dict[linda][0] + '\n')



