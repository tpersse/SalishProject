#!/bin/bash
#SBATCH --account=bgmp
#SBATCH --partition=bgmp
#SBATCH --cpus-per-task=8
#SBATCH --nodes=1
#SBATCH --time=10:00:00
#SBATCH --output=../../cover%j.out
#SBATCH --error=../../cover%j.err
#SBATCH --mail-user='tpersse@uoregon.edu'
#SBATCH --mail-type=END,FAIL

### SETTING CONDA ENVIRONMENT ###

conda activate Salish

### SET VARIABLES ###

LINDA = #/path/to/linda/file

PRB = #/path/to/probe/file

FQ1 = #/path/to/fastq/read1

FQ2 = #/path/to/fastq/read2

HRG = #/path/to/ref/genome/fasta

### DATACLEAN ###

/usr/bin/time -v python filter_2_csv.py --linda $LINDA --probe $PRB --read1 $FQ1 --read2 $FQ2



### FASTQC ###
#  module load fastqc/0.11.5 DONT KNOW IF WE NEED THIS
#  quite optional

/usr/bin/time -v cat Read1Filtered.fastq | fastqc stdin -o R1_Fastqc 

/usr/bin/time -v cat Read2Filtered.fastq | fastqc stdin -o R2_Fastqc



### CUTADAPT ###
/usr/bin/time -v /usr/bin/time -v cutadapt -a AGATCGGAAGAGCACACGTCTGAACTCCAGTCA -A AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGT -j 0 -o Read1_filtered_cut.fastq -p Read2_filtered_cut.fastq Read1Filtered.fastq Read2Filtered.fastq



### FASTQC 2 ###
# quite optional
/usr/bin/time -v cat Read1_filtered_cut.fastq | fastqc stdin -o R1_cut_Fastqc 

/usr/bin/time -v cat Read2Filtered.fastq | fastqc stdin -o R2_cut_Fastqc



### DEDUPLICATION ###

## For variant calling:
/usr/bin/time -v #connor stuff here, for lofreq... should look into this more

## For alignment, coverage stats
/usr/bin/time -v # aligned stuff here, our script

### ALIGNMENT ###

#building index
bwa index -a bwtsw $HRG -p bwa_index_prefix

#aligning index
bwa mem bwa_index_prefix /projects/bgmp/shared/2021_projects/Salish/fastqc/Read1Filtered.fastq  /projects/bgmp/shared/2021_projects/Salish/fastqc/Read2Filtered.fastq -t 8 > bwa_mem_alignments.sam

#Flag Stats output: alignment %
samtools flagstat -O tsv /projects/bgmp/shared/2021_projects/Salish/alignment/bwa/bwa_mem_alignments.sam > bwa_flagstats

#stats output: general stats
samtools stats /projects/bgmp/shared/2021_projects/Salish/alignment/bwa/bwa_mem_alignments.sam > bwa_stats

### COVERAGE ###

#bedtools script

### CALLING VARIANTS ###

/usr/bin/time -v /projects/bgmp/shared/2021_projects/Salish/SalishProj/Connor/lofreq_final/lofreq_EC_final.sh

#lofreq script