#!/bin/bash
#SBATCH --account=bgmp
#SBATCH --partition=bgmp
#SBATCH --cpus-per-task=8
#SBATCH --nodes=1
#SBATCH --time=10:00:00
#SBATCH --output=../filter%j.out
#SBATCH --error=../filter%j.err
#SBATCH --mail-user='tpersse@uoregon.edu'
#SBATCH --mail-type=END,FAIL

conda activate bgmp_py39

/usr/bin/time -v python filter_2_csv.py --linda ./../lindas.txt --probe ./../target_oligs.txt --read1 ./../Project-35_S1_L001_R1_001.fastq --read2 ./../Project-35_S1_L001_R2_001.fastq