#!/bin/bash
#SBATCH --account=bgmp
#SBATCH --partition=bgmp
#SBATCH --cpus-per-task=8
#SBATCH --nodes=1
#SBATCH --time=10:00:00
#SBATCH --output=bwa_12_27%j.out
#SBATCH --error=bwa_12_27%j.err
#SBATCH --mail-user='tpersse@uoregon.edu'
#SBATCH --mail-type=END,FAIL

#building index
/usr/bin/time -v bwa index -a bwtsw /projects/bgmp/shared/2021_projects/Salish/alignment/bwa/ref_genome.fasta -p bwa_index_prefix_1_10

#aligning index
/usr/bin/time -v bwa mem bwa_index_prefix_1_10 /projects/bgmp/shared/2021_projects/Salish/SalishProj/Deduplicate/Read1_deduped_UMI_Probe.fastq /projects/bgmp/shared/2021_projects/Salish/SalishProj/Deduplicate/Read2_deduped_UMI_Probe.fastq > UMI_Probe_Deduped_1_10.sam

#Flag Stats output: alignment %
#/usr/bin/time -v samtools flagstat -O tsv /projects/bgmp/shared/2021_projects/Salish/alignment/bwa/bwa_mem_r1r2.sam > bwa_flagstats_r1r2

#stats output: general stats
#/usr/bin/time -v samtools stats /projects/bgmp/shared/2021_projects/Salish/alignment/bwa/bwa_mem_r1r2.sam > bwa_stats_r1r2