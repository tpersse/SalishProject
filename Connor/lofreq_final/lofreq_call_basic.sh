#!/bin/bash 
#SBATCH --account=bgmp 
#SBATCH --partition=bgmp 
#SBATCH --job-name=lofreq
#SBATCH --output=lofreq_%j.out 
#SBATCH --nodes=1 
#SBATCH --ntasks-per-node=8 
#SBATCH --time=3:00:00 
#SBATCH --cpus-per-task=1

# Make a bam file
#/usr/bin/time -v lofreq indelqual /projects/bgmp/shared/2021_projects/Salish/SalishProj/Connor/lofreq_final/filter_trimmed_not_deduped.sorted.bam --dindel -f /projects/bgmp/shared/2021_projects/Salish/alignment/bwa/ref_genome.fasta -o lofreq_filtered_trimmed_not_deduped.bam

# Need to index the bam file

# Take that new bam and make an unfiltered VCF


#lofreq call --no-default-filter -A -B -a 1 -b 1 -r 7:55019017-55211628 -f /projects/bgmp/shared/2021_projects/Salish/alignment/bwa/ref_genome.fasta /projects/bgmp/shared/2021_projects/Salish/SalishProj/Connor/lofreq_final/filter_trimmed_not_deduped.sorted.bam -o lofreq_call_basic_EGFR.vcf
lofreq call -f /projects/bgmp/shared/2021_projects/Salish/alignment/bwa/ref_genome.fasta -l EGFR_TP53.bed -o lofreq_call_basic_EGFR.vcf /projects/bgmp/shared/2021_projects/Salish/SalishProj/Connor/lofreq_final/filter_trimmed_not_deduped.sorted.bam