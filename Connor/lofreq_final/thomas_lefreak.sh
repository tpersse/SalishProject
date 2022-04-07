#!/bin/bash 
#SBATCH --account=bgmp
#SBATCH --partition=bgmp
#SBATCH --job-name=lakfreak
#SBATCH --output=lafreak_%j.out
#SBATCH --error=lafreak%j.err
#SBATCH --nodes=1
#SBATCH --time=3:00:00
#SBATCH --cpus-per-task=40

# Make a bam file
#/usr/bin/time -v lofreq indelqual /projects/bgmp/shared/2021_projects/Salish/SalishProj/Connor/lofreq_final/filter_trimmed_not_deduped.sorted.bam --dindel -f /projects/bgmp/shared/2021_projects/Salish/alignment/bwa/ref_genome.fasta -o lofreq_filtered_trimmed_not_deduped.bam

# Need to index the bam file

# Take that new bam and make an unfiltered VCF
/usr/bin/time -v lofreq call \
			--verbose --call-indels --no-default-filter -B \
			--ref /projects/bgmp/shared/2021_projects/Salish/alignment/bwa/ref_genome.fasta \
			-o lofreq_unfiltered_trimmed_not_deduped.vcf \
			/projects/bgmp/shared/2021_projects/Salish/SalishProj/Connor/lofreq_final/lofreq_filtered_trimmed_not_deduped.bam


# Take the unfiltered VCF and filter it 
/usr/bin/time -v lofreq filter \
			-i lofreq_unfiltered_trimmed_not_deduped.vcf -o lofreq_filtered_trimmed_not_deduped.vcf \
			--af-min 0.01 --cov-min 2 \
			--sb-no-compound --no-defaults --verbose

#!/bin/bash 
#SBATCH --account=bgmp 
#SBATCH --partition=bgmp 
#SBATCH --job-name=lofreq_EC
#SBATCH --output=lofreq_EC_%j.out 
#SBATCH --nodes=1 
#SBATCH --ntasks-per-node=8 
#SBATCH --time=3:00:00 
#SBATCH --cpus-per-task=1

