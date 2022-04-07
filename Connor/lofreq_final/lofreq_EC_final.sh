#!/bin/bash 
#SBATCH --account=bgmp 
#SBATCH --partition=bgmp 
#SBATCH --job-name=lofreq_EC
#SBATCH --output=lofreq_EC_%j.out 
#SBATCH --nodes=1 
#SBATCH --ntasks-per-node=8 
#SBATCH --time=3:00:00 
#SBATCH --cpus-per-task=1

# Make a bam file
#/usr/bin/time -v lofreq indelqual UMI_Probe_Deduped_EC_1_19.sorted.bam --dindel -f /projects/bgmp/shared/2021_projects/Salish/alignment/bwa/ref_genome.fasta -o lofreq_EC_deduped_1_19.bam

# Need to sort and index the bam file

# Take that new bam and make an unfiltered VCF
/usr/bin/time -v lofreq call-parallel --pp-threads 2 \
			--verbose --call-indels --no-default-filter -B \
			--ref /projects/bgmp/shared/2021_projects/Salish/alignment/bwa/ref_genome.fasta \
			-o lofreq_unfiltered_EC.vcf \
			lofreq_EC_deduped_1_19.sorted.bam


# # # Take the unfiltered VCF and filter it 
/usr/bin/time -v lofreq filter \
			-i lofreq_unfiltered_EC.vcf -o lofreq_filtered_EC.vcf \
			--af-min 0.001 --cov-min 2 \
			--sb-no-compound --no-defaults --verbose